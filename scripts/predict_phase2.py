"""Forecast from an observed CSV history without loading future data.

CSV first column: timestamp. Remaining columns: exact training sensor IDs/order.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from run_phase2 import build_model, sha


def predict_history(checkpoint, manifest, frame):
    ids = manifest["sensor_ids"]
    settings = manifest["settings"]
    if list(frame.columns) != ids:
        raise ValueError("history sensor IDs/order differ from training")
    if len(frame) < settings["history"]:
        raise ValueError("need at least 12 observed timestamps")
    frame = frame.iloc[-settings["history"] :]
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise ValueError("history index must contain parseable timestamps")
    if frame.index.hasnans or frame.index.tz is not None:
        raise ValueError("use recorded naive timestamps; timezone conversion is not established")
    if not (frame.index.to_series().diff().dropna() == pd.Timedelta(minutes=5)).all():
        raise ValueError("history must have unique ordered five-minute timestamps")
    raw = frame.to_numpy(dtype=np.float32)
    if np.isinf(raw).any() or (raw < 0).any():
        raise ValueError("invalid negative/infinite speed")
    missing = ~np.isfinite(raw) | (raw == 0)
    raw[missing] = np.nan
    state = checkpoint["normalization"]
    if state != manifest["normalization"]:
        raise ValueError("checkpoint normalization differs from manifest")
    medians = np.array(state["medians"], dtype=np.float32)
    filled = pd.DataFrame(raw).ffill().fillna(pd.Series(medians)).to_numpy(np.float32)
    x = np.stack([(filled - state["mean"]) / state["scale"], missing], -1)[None]
    t = frame.index[-1]
    day = (t.hour * 60 + t.minute) / 1440
    week = (t.dayofweek + day) / 7
    calendar = np.array(
        [
            [
                np.sin(2 * np.pi * day),
                np.cos(2 * np.pi * day),
                np.sin(2 * np.pi * week),
                np.cos(2 * np.pi * week),
                t.dayofweek >= 5,
            ]
        ],
        dtype=np.float32,
    )
    mask = checkpoint["model"].get("graph.mask", torch.eye(len(ids), dtype=torch.bool))
    model = build_model(settings, len(ids), mask, checkpoint["mode"], "cpu")
    model.load_state_dict(checkpoint["model"])
    model.eval()
    with torch.no_grad():
        result = model(torch.from_numpy(x), torch.from_numpy(calendar))[0].numpy()
    result = result * state["scale"] + state["mean"]
    if not np.isfinite(result).all():
        raise ValueError("nonfinite forecast")
    times = pd.date_range(t + pd.Timedelta(minutes=5), periods=settings["horizon"], freq="5min")
    return pd.DataFrame(result, index=times, columns=ids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--model-folder", required=True)
    parser.add_argument("--history", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((args.run_dir / "manifest.json").read_text())
    root = Path(__file__).resolve().parents[1]
    for path, expected in manifest["source_hashes"].items():
        if sha(root / path) != expected:
            raise ValueError("source/config differs from training: " + path)
    folder = (args.run_dir / args.model_folder).resolve()
    if folder.parent != args.run_dir.resolve():
        raise ValueError("model folder must be directly inside the run")
    record = json.loads((folder / "complete.json").read_text())
    if sha(folder / "best.pt") != record["checkpoint_sha256"]:
        raise ValueError("checkpoint hash mismatch")
    checkpoint = torch.load(folder / "best.pt", map_location="cpu", weights_only=True)
    frame = pd.read_csv(args.history, index_col=0, parse_dates=True)
    pred = predict_history(checkpoint, manifest, frame)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pred.to_csv(args.output, index_label="target_timestamp")
    print(f"Saved 12 horizons for {len(pred.columns)} sensors: {args.output}")


if __name__ == "__main__":
    main()
