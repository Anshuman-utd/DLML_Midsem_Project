"""Evaluate frozen checkpoints, select a validation-only blend and export evidence."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from _common import ROOT, load_config, load_series
from run_phase2 import build_model, sha, tensors, write_json

from trafficml.data.neural import NeuralWindows
from trafficml.eval.metrics import horizon_metrics
from trafficml.eval.predictions import load_predictions, load_targets
from trafficml.eval.slices import time_slices


@torch.no_grad()
def predict(model, data, anchors, batch_size, device):
    model.eval()
    blocks = []
    for start in range(0, len(anchors), batch_size):
        x, calendar, _ = tensors(data, anchors[start : start + batch_size], device)
        blocks.append(model(x, calendar).cpu().numpy() * data.scale + data.mean)
    pred = np.concatenate(blocks)
    if not np.isfinite(pred).all():
        raise ValueError("nonfinite forecasts")
    return pred


def score(pred, true, index, anchors, name, split, mode=None, seed=None):
    frames = []
    for label, mask in time_slices(index, anchors, 12).items():
        masked = np.where(mask, true, np.nan)
        frame = horizon_metrics(masked, pred)
        frame["model"], frame["slice"], frame["split"] = name, label, split
        frame["mode"], frame["seed"] = mode or name, seed
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--baseline-dir", type=Path, default=ROOT / "results/runs/phase1-full-v1")
    args = parser.parse_args()
    manifest = json.loads((args.run_dir / "manifest.json").read_text())
    for path, expected in manifest["source_hashes"].items():
        if sha(ROOT / path) != expected:
            raise ValueError("training source/config changed since run: " + path)
    settings = manifest["settings"]
    if (args.run_dir / "lineage.json").exists():
        lineage = json.loads((args.run_dir / "lineage.json").read_text())
        evidence = ROOT / "verification/phase2-20261112"
        parent_file = evidence / "source_snapshot_v1/manifest.json"
        parent = json.loads(parent_file.read_text())
        proof = json.loads((evidence / "memory_equivalence.json").read_text())
        if (
            not proof["features_bitwise_equal"]
            or not proof["normalization_exact"]
            or proof["new_preprocessor_sha256"] != sha(ROOT / "src/trafficml/data/neural.py")
            or proof["old_preprocessor_sha256"]
            != sha(evidence / "source_snapshot_v1/data_neural.py.txt")
            or parent["settings"] != settings
            or parent["data_hashes"] != manifest["data_hashes"]
            or parent["normalization"] != manifest["normalization"]
            or parent["source_hashes"]["src/trafficml/models/neural.py"]
            != manifest["source_hashes"]["src/trafficml/models/neural.py"]
        ):
            raise ValueError("inherited-fit equivalence or parent identity is inconsistent")
        for path, expected_hash in parent["source_hashes"].items():
            if path != "src/trafficml/data/neural.py":
                if manifest["source_hashes"].get(path) != expected_hash:
                    raise ValueError("inheritance changed more than feature storage: " + path)
        for folder, origin in lineage["inherited_fits"].items():
            if origin["parent_manifest_sha256"] != sha(parent_file) or origin[
                "checkpoint_sha256"
            ] != sha(args.run_dir / folder / "best.pt"):
                raise ValueError("inherited checkpoint lineage hash differs")
    baseline_manifest = json.loads((args.baseline_dir / "manifest.json").read_text())
    # Added Phase 2 modules do not alter the old source snapshot. Every file that
    # actually produced the frozen baselines must still have identical bytes.
    for path, expected in baseline_manifest["identity"]["source_sha256"].items():
        if sha(ROOT / path) != expected:
            raise ValueError("historical baseline source changed: " + path)
    for path, expected in baseline_manifest["identity"]["data_sha256"].items():
        if sha(ROOT / path) != expected:
            raise ValueError("baseline data identity differs from current files: " + path)
    torch.set_num_threads(settings["threads"])
    cfg = load_config()
    for name, expected in manifest["data_hashes"].items():
        if sha(cfg["paths"][name]) != expected:
            raise ValueError("data changed since training: " + name)
    speed, values, ids, splits = load_series(cfg)
    if ids != manifest["sensor_ids"]:
        raise ValueError("sensor order changed")
    data = NeuralWindows(values, speed.index, int(splits.train[-1] + 13))
    if data.state() != manifest["normalization"]:
        raise ValueError("normalization changed")
    out = args.run_dir / "evaluation"
    out.mkdir(exist_ok=True)
    records = json.loads((args.run_dir / "experiments.json").read_text())
    expected = {
        (mode, seed) for mode in ["temporal", "graph", "self"] for seed in settings["seeds"]
    } | {("uniform", 42), ("no_dropout", 42)}
    if len(records) != len(expected) or {(r["mode"], r["seed"]) for r in records} != expected:
        raise ValueError("training is incomplete or experiment coverage differs from protocol")
    frames, details = [], []
    neural, baselines, targets = {}, {}, {}
    for split in ["val_tune", "val_stack", "test"]:
        anchors = getattr(splits, split)
        target = values[anchors[:, None] + np.arange(1, 13)]
        old = load_targets(split, args.baseline_dir / "preds")
        np.testing.assert_array_equal(old["anchors"], anchors)
        np.testing.assert_array_equal(old["sensor_ids"], ids)
        np.testing.assert_allclose(old["y_true"], target, rtol=0, atol=0, equal_nan=True)
        targets[split] = target
        for name in ["M0_persistence", "M1_ha", "M3_rf", "M4_xgb"]:
            pred = load_predictions(name, split, args.baseline_dir / "preds")
            baselines[(name, split)] = pred
            frames.append(score(pred, target, speed.index, anchors, name, split))
    baseline_hashes = {
        path.name: sha(path) for path in sorted((args.baseline_dir / "preds").glob("*.npz"))
    }
    frozen = ROOT / "verification/full-phase1-20261026"
    frozen_manifest = json.loads((frozen / "manifest.json").read_text())
    historical_metrics_match = False
    if baseline_manifest["identity"] == frozen_manifest["identity"]:
        # Reconfirm that reused bundles reproduce the preserved historical scores.
        keys = ["model", "split", "slice", "minutes"]
        actual_baselines = pd.concat(frames).set_index(keys).sort_index()
        saved_baselines = pd.read_csv(frozen / "analysis/all_metrics.csv")
        saved_baselines = saved_baselines.set_index(keys).sort_index()
        columns = ["n_valid", "MAE", "RMSE", "MAPE"]
        if not actual_baselines.index.equals(saved_baselines.index):
            raise ValueError("historical baseline metric coverage differs")
        np.testing.assert_allclose(
            actual_baselines[columns], saved_baselines[columns], rtol=1e-9, atol=1e-9
        )
        historical_metrics_match = True
    for record in records:
        folder = args.run_dir / record["folder"]
        if sha(folder / "best.pt") != record["checkpoint_sha256"]:
            raise ValueError("checkpoint checksum mismatch")
        checkpoint = torch.load(folder / "best.pt", map_location="cpu", weights_only=True)
        if (
            checkpoint["settings"] != settings
            or checkpoint["normalization"] != data.state()
            or checkpoint["mode"] != record["mode"]
            or checkpoint["seed"] != record["seed"]
            or checkpoint["learning_rate"] != record["learning_rate"]
        ):
            raise ValueError("checkpoint training metadata differs from experiment identity")
        mask = checkpoint["model"].get("graph.mask", torch.eye(len(ids), dtype=torch.bool))
        model = build_model(settings, len(ids), mask, record["mode"], "cpu")
        model.load_state_dict(checkpoint["model"])
        name = f"{record['mode']}_seed{record['seed']}"
        began = time.perf_counter()
        negative_count = 0
        for split in ["val_tune", "val_stack", "test"]:
            anchors = getattr(splits, split)
            pred = predict(model, data, anchors, settings["batch_size"], "cpu")
            np.save(out / f"{name}_{split}.npy", pred)
            frames.append(
                score(
                    pred,
                    targets[split],
                    speed.index,
                    anchors,
                    name,
                    split,
                    record["mode"],
                    record["seed"],
                )
            )
            if record["seed"] == 42 and record["mode"] == "graph":
                neural[split] = pred
            if split == "test":
                negative_count = int((pred < 0).sum())
                error = np.nanmean(np.abs(pred[:, 11] - targets[split][:, 11]), axis=0)
                details.extend(
                    {"model": name, "sensor_id": sensor, "mae_60": float(e)}
                    for sensor, e in zip(ids, error, strict=True)
                )
                # Deterministic checkpoint-reload inference verification on real inputs.
                restored = build_model(settings, len(ids), mask, record["mode"], "cpu")
                restored.load_state_dict(torch.load(folder / "best.pt", weights_only=True)["model"])
                restored.eval()
                expected = predict(model, data, anchors[:4], 4, "cpu")
                actual = predict(restored, data, anchors[:4], 4, "cpu")
                np.testing.assert_allclose(actual, expected, rtol=0, atol=0)
        write_json(
            folder / "inference_check.json",
            {
                "exact_reload_reproduction": True,
                "test_negative_predictions": negative_count,
                "all_split_inference_seconds": time.perf_counter() - began,
            },
        )
        print("Evaluated", name, flush=True)
    hybrid_scores = []
    true = targets["val_stack"][:, [2, 5, 11]]
    for alpha in settings["hybrid_weights"]:
        p = (alpha * baselines[("M4_xgb", "val_stack")] + (1 - alpha) * neural["val_stack"])[
            :, [2, 5, 11]
        ]
        hybrid_scores.append(
            {"alpha_xgb": alpha, "val_stack_headline_mae": float(np.nanmean(np.abs(p - true)))}
        )
    selected = min(hybrid_scores, key=lambda x: x["val_stack_headline_mae"])
    write_json(out / "hybrid_selection.json", {"candidates": hybrid_scores, "selected": selected})
    alpha = selected["alpha_xgb"]
    for split in ["val_stack", "test"]:
        pred = alpha * baselines[("M4_xgb", split)] + (1 - alpha) * neural[split]
        np.save(out / f"hybrid_{split}.npy", pred)
        frames.append(
            score(
                pred,
                targets[split],
                speed.index,
                getattr(splits, split),
                "hybrid_seed42",
                split,
                "hybrid",
                42,
            )
        )
    all_metrics = pd.concat(frames, ignore_index=True)
    all_metrics.to_csv(out / "all_metrics.csv", index=False)
    pd.DataFrame(details).to_csv(out / "per_sensor_mae_60.csv", index=False)
    main = all_metrics[all_metrics["mode"].isin(["temporal", "graph", "self"])]
    summary = main.groupby(["mode", "split", "slice", "minutes"])[["MAE", "RMSE", "MAPE"]].agg(
        ["mean", "std", "count"]
    )
    summary.to_csv(out / "seed_summary.csv")
    write_json(
        out / "verification.json",
        {
            "baseline_targets_exact": True,
            "historical_baseline_metrics_match": historical_metrics_match,
            "baseline_bundle_sha256": baseline_hashes,
            "checkpoint_reload_exact": True,
            "experiments_evaluated": len(records),
            "test_status": manifest["test_status"],
            "metrics_sha256": sha(out / "all_metrics.csv"),
            "effective_hybrid": "blend"
            if 0 < alpha < 1
            else "pure endpoint; no blend benefit selected",
        },
    )
    print("Saved evaluation:", out, flush=True)


if __name__ == "__main__":
    main()
