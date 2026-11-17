"""Reproducible DL experiments. Selection sees val_tune, never test labels.

Run one command; completed checkpoints are resumable only with identical inputs.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
import yaml
from _common import ROOT, load_config, load_series

from trafficml.data.graph import build_adjacency
from trafficml.data.load import load_distances
from trafficml.data.neural import NeuralWindows
from trafficml.models.neural import TrafficGRU, masked_loss


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temp.replace(path)


def build_model(settings, nodes, mask, mode, device):
    return TrafficGRU(
        nodes,
        settings["hidden"],
        settings["horizon"],
        settings["heads"],
        mask,
        mode,
        0.0 if mode == "no_dropout" else settings["dropout"],
    ).to(device)


def tensors(data, anchors, device):
    return [torch.from_numpy(a).to(device) for a in data.batch(anchors)]


@torch.no_grad()
def validation(model, data, anchors, batch_size, device):
    model.eval()
    total, count = 0.0, 0
    for start in range(0, len(anchors), batch_size):
        x, c, y = tensors(data, anchors[start : start + batch_size], device)
        p = model(x, c)[:, [2, 5, 11]]
        y = y[:, [2, 5, 11]]
        valid = torch.isfinite(y)
        total += float((p[valid] - y[valid]).abs().sum().cpu())
        count += int(valid.sum().cpu())
    if not count:
        raise ValueError("validation has no valid labels")
    return total / count * data.scale


def train_one(folder, settings, data, splits, mask, mode, seed, lr, device):
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / "complete.json").exists():
        return json.loads((folder / "complete.json").read_text())
    random.seed(seed)
    torch.manual_seed(seed)
    model = build_model(settings, data.values.shape[1], mask, mode, device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=settings["weight_decay"])
    train = splits.train[:: settings["train_stride"]]
    generator = np.random.default_rng(seed)
    best, stale, history = float("inf"), 0, []
    began = time.perf_counter()
    for epoch in range(1, settings["max_epochs"] + 1):
        model.train()
        order = generator.permutation(train)
        total, count = 0.0, 0
        for start in range(0, len(order), settings["batch_size"]):
            x, c, y = tensors(data, order[start : start + settings["batch_size"]], device)
            optimizer.zero_grad(set_to_none=True)
            prediction = model(x, c)
            loss = masked_loss(prediction, y)
            if loss is None:
                continue
            if not bool(torch.isfinite(loss)):
                raise FloatingPointError("nonfinite training loss")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), settings["gradient_clip"])
            optimizer.step()
            valid_count = int(torch.isfinite(y).sum().cpu())
            total += float(loss.detach().cpu()) * valid_count
            count += valid_count
        score = validation(model, data, splits.val_tune, settings["batch_size"], device)
        history.append(
            {
                "epoch": epoch,
                "train_all_horizon_mae": total / count * data.scale,
                "validation_headline_mae": score,
                "elapsed_seconds": time.perf_counter() - began,
            }
        )
        if score < best:
            best, stale = score, 0
            state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            torch.save(
                {
                    "model": state,
                    "mode": mode,
                    "seed": seed,
                    "learning_rate": lr,
                    "settings": settings,
                    "normalization": data.state(),
                    "epoch": epoch,
                },
                folder / "best.pt",
            )
        else:
            stale += 1
        write_json(folder / "history.json", history)
        print(
            f"{folder.name} epoch={epoch} train={history[-1]['train_all_horizon_mae']:.4f} "
            f"val={score:.4f} best={best:.4f} seconds={time.perf_counter() - began:.0f}",
            flush=True,
        )
        if stale >= settings["patience"]:
            break
    record = {
        "mode": mode,
        "seed": seed,
        "learning_rate": lr,
        "validation_mae": best,
        "epochs": len(history),
        "parameters": sum(p.numel() for p in model.parameters()),
        "seconds": time.perf_counter() - began,
        "checkpoint_sha256": sha(folder / "best.pt"),
    }
    write_json(folder / "complete.json", record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/phase2.yaml")
    parser.add_argument("--device", choices=["cpu", "mps", "cuda"], default="cpu")
    parser.add_argument("--stage", choices=["tune", "all"], default="all")
    args = parser.parse_args()
    settings = yaml.safe_load(args.config.read_text())
    torch.set_num_threads(settings["threads"])
    cfg = load_config()
    speed, values, ids, splits = load_series(cfg)
    data = NeuralWindows(values, speed.index, int(splits.train[-1] + 13))
    adjacency = build_adjacency(load_distances(cfg["paths"]["distances"]), ids)
    mask = (adjacency.T > 0).copy()
    source_files = [
        args.config,
        ROOT / "configs/data.yaml",
        Path(__file__),
        ROOT / "src/trafficml/models/neural.py",
        ROOT / "src/trafficml/data/neural.py",
    ]
    identity = {
        "source_hashes": {str(p.relative_to(ROOT)): sha(p) for p in source_files},
        "data_hashes": {k: sha(p) for k, p in cfg["paths"].items()},
        "sensor_ids": ids,
        "split_counts": {k: len(a) for k, a in splits.items()},
        "torch": str(torch.__version__),
        "device": args.device,
        "normalization": data.state(),
        "settings": settings,
        "test_status": "Previously exposed; exploratory comparisons only",
        "message_direction": "mask[receiver,sender] = adjacency[sender,receiver] > 0",
    }
    args.run_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = args.run_dir / "manifest.json"
    if manifest_file.exists():
        if json.loads(manifest_file.read_text()) != identity:
            raise ValueError("run identity changed; choose a fresh directory")
    else:
        write_json(manifest_file, identity)
    # Tuning never evaluates val_stack/test. Each family gets the same search budget.
    selected = {}
    records = []
    for mode in ["temporal", "graph"]:
        candidates = []
        for j, lr in enumerate(settings["learning_rates"]):
            folder = args.run_dir / f"tune_{mode}_{j}"
            result = train_one(folder, settings, data, splits, mask, mode, 42, lr, args.device)
            result = {**result, "folder": folder.name}
            candidates.append(result)
            records.append(result)
        selected[mode] = min(candidates, key=lambda x: x["validation_mae"])
    write_json(args.run_dir / "tuning.json", records)
    write_json(args.run_dir / "selected.json", selected)
    if args.stage == "tune":
        return
    experiments = []
    for mode in ["temporal", "graph", "self", "uniform", "no_dropout"]:
        family = "temporal" if mode == "temporal" else "graph"
        chosen = selected[family]
        seeds = settings["seeds"] if mode in {"temporal", "graph", "self"} else [42]
        for seed in seeds:
            if seed == 42 and mode in {"temporal", "graph"}:
                result = copy.deepcopy(chosen)
            else:
                folder = args.run_dir / f"{mode}_seed{seed}"
                result = train_one(
                    folder,
                    settings,
                    data,
                    splits,
                    mask,
                    mode,
                    seed,
                    chosen["learning_rate"],
                    args.device,
                )
                result = {**result, "folder": folder.name}
            experiments.append(result)
            write_json(args.run_dir / "experiments.json", experiments)
    print("Training complete; run evaluate_phase2.py for frozen evaluation.", flush=True)


if __name__ == "__main__":
    main()
