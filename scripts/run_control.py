"""Run the predeclared synthetic LWR/control comparison; never uses METR-LA."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from trafficml.simulation.experiment import demand_schedule, simulate

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/control.yaml")
    args = parser.parse_args()
    settings = yaml.safe_load(args.config.read_text())
    sources = [Path(__file__), args.config, ROOT / "docs/PHASE2_CONTROL_PROTOCOL.md"]
    sources += sorted((ROOT / "src/trafficml/simulation").glob("*.py"))
    identity = {
        "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in sources},
        "settings": settings,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scope": "Synthetic illustration; not calibrated METR-LA, MARL or GAT-driven control",
        "pairing": "Identical arrivals/state/physics/exit constraints per scenario and seed",
    }
    args.run_dir.mkdir(parents=True, exist_ok=True)
    manifest = args.run_dir / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text()) != identity:
        raise ValueError("run identity changed; choose a new run directory")
    manifest.write_text(json.dumps(identity, indent=2) + "\n")
    records, hashes = [], {}
    for j, scenario in enumerate(settings["scenarios"]):
        rate, capacities = demand_schedule(settings, scenario)
        for seed in settings["seeds"]:
            rng = np.random.default_rng(np.random.SeedSequence([seed, j]))
            arrivals = rng.poisson(rate * settings["dt_seconds"] / 3600)
            digest = hashlib.sha256(arrivals.tobytes()).hexdigest()
            for policy in ["fixed", "responsive"]:
                result, trace = simulate(settings, arrivals, capacities, policy)
                records.append(
                    {
                        "scenario": scenario,
                        "seed": seed,
                        "policy": policy,
                        "arrival_sha256": digest,
                        **result,
                    }
                )
                dest = args.run_dir / f"{scenario}_{seed}_{policy}.npz"
                np.savez_compressed(dest, **trace)
                hashes[dest.name] = sha(dest)
            print("Compared", scenario, seed, flush=True)
    frame = pd.DataFrame(records)
    frame.to_csv(args.run_dir / "metrics.csv", index=False)
    metrics = [c for c in frame.select_dtypes(include="number").columns if c != "seed"]
    frame.groupby(["scenario", "policy"])[metrics].agg(["mean", "std"]).to_csv(
        args.run_dir / "summary.csv"
    )
    paired = frame.pivot(
        index=["scenario", "seed"], columns="policy", values="system_vehicle_minutes"
    )
    paired["reduction_percent"] = 100 * (paired["fixed"] - paired["responsive"]) / paired["fixed"]
    paired.to_csv(args.run_dir / "paired_system_time.csv")
    (args.run_dir / "artifacts.json").write_text(
        json.dumps(
            {
                "trajectory_sha256": hashes,
                "metrics_sha256": sha(args.run_dir / "metrics.csv"),
                "runs": len(frame),
                "all_scenarios_retained": True,
                "policy_tuning_performed": False,
            },
            indent=2,
        )
        + "\n"
    )
    print("Saved", len(frame), "matched synthetic runs:", args.run_dir)


if __name__ == "__main__":
    main()
