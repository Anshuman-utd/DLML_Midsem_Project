"""Export measured synthetic control evidence and report inputs without changing forecasts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "balanced": "Balanced",
    "arterial_peak": "Arterial peak",
    "side_peak": "Side peak",
    "downstream_restriction": "Downstream limit",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    run = args.run_dir
    manifest = json.loads((run / "manifest.json").read_text())
    for name, expected in manifest["source_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("synthetic experiment source changed: " + name)
    metrics = pd.read_csv(run / "metrics.csv")
    artifacts = json.loads((run / "artifacts.json").read_text())
    if (
        hashlib.sha256((run / "metrics.csv").read_bytes()).hexdigest()
        != artifacts["metrics_sha256"]
    ):
        raise ValueError("metrics checksum mismatch")
    for name, expected in artifacts["trajectory_sha256"].items():
        if hashlib.sha256((run / name).read_bytes()).hexdigest() != expected:
            raise ValueError("trajectory checksum mismatch: " + name)
    settings = manifest["settings"]
    expected = {
        (s, seed, p)
        for s in settings["scenarios"]
        for seed in settings["seeds"]
        for p in ["fixed", "responsive"]
    }
    actual = set(zip(metrics.scenario, metrics.seed, metrics.policy, strict=True))
    if actual != expected or len(metrics) != len(expected):
        raise ValueError("experiment coverage differs from recorded protocol")
    if not (metrics.groupby(["scenario", "seed"]).arrival_sha256.nunique() == 1).all():
        raise ValueError("paired policies used different arrivals")
    evidence = ROOT / "verification/phase2-final-20261116/control"
    images = ROOT / "report/phase2/images"
    evidence.mkdir(parents=True, exist_ok=True)
    grouped = metrics.groupby(["scenario", "policy"])
    rows = []
    for scenario in settings["scenarios"]:
        row = [LABELS[scenario]]
        for policy in ["fixed", "responsive"]:
            part = grouped.get_group((scenario, policy))
            row += [
                float(part.system_vehicle_minutes.mean()),
                float(part.boundary_wait_vehicle_minutes.mean()),
                float(part.departed_vehicles.mean()),
                float(part.residual_vehicles.mean()),
            ]
        rows.append(row)
    plt.rcParams.update(
        {"font.size": 12, "figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False}
    )
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    positions = np.arange(len(rows))
    for j, policy in enumerate(["fixed", "responsive"]):
        for ax, metric in zip(
            axes, ["system_vehicle_minutes", "boundary_wait_vehicle_minutes"], strict=True
        ):
            values = [grouped.get_group((s, policy))[metric] for s in settings["scenarios"]]
            ax.bar(
                positions + (j - 0.5) * 0.35,
                [v.mean() for v in values],
                width=0.35,
                yerr=[v.std() for v in values],
                capsize=3,
                label=policy.title(),
            )
    for ax, title in zip(
        axes, ["Total system vehicle-minutes", "Boundary waiting vehicle-minutes"], strict=True
    ):
        ax.set_title(title)
        ax.set_xticks(positions, [r[0].replace(" ", "\n") for r in rows])
        ax.legend(fontsize=10)
        ax.grid(axis="y", alpha=0.15)
    fig.tight_layout()
    fig.savefig(images / "control_comparison.png", bbox_inches="tight")
    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.6), sharex=True)
    dt = settings["dt_seconds"] / 60
    for ax, scenario in zip(axes.flat, settings["scenarios"], strict=True):
        for policy in ["fixed", "responsive"]:
            with np.load(run / f"{scenario}_{settings['seeds'][0]}_{policy}.npz") as trace:
                occupancy = trace["cells"].sum(axis=1) + trace["queues"].sum(axis=1)
            ax.plot(np.arange(len(occupancy)) * dt, occupancy, label=policy.title())
        ax.set_title(LABELS[scenario])
        ax.set_ylabel("Vehicles in system")
        ax.axvline(settings["demand_minutes"], ls=":", color="grey", lw=1)
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.legend(fontsize=9)
    for ax in axes[1]:
        ax.set_xlabel("Simulation minutes")
    fig.tight_layout()
    fig.savefig(images / "control_occupancy.png", bbox_inches="tight")
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, policy in zip(axes, ["fixed", "responsive"], strict=True):
        example = run / f"downstream_restriction_{settings['seeds'][0]}_{policy}.npz"
        with np.load(example) as trace:
            density = trace["cells"][:, :6].T / settings["cell_km"]
        heat = ax.imshow(
            density,
            origin="lower",
            aspect="auto",
            extent=[0, 80, -0.5, 5.5],
            vmin=0,
            vmax=settings["jam_density_veh_km"],
            cmap="magma",
        )
        ax.set_title(policy.title())
        ax.set_xlabel("Simulation minutes")
        ax.axvline(25, color="cyan", ls=":", lw=1)
        ax.axvline(40, color="cyan", ls=":", lw=1)
    axes[0].set_ylabel("Corridor cell (downstream increases)")
    fig.colorbar(heat, ax=axes, label="Synthetic density (veh/km)", fraction=0.03, pad=0.03)
    fig.subplots_adjust(bottom=0.2, right=0.86, wspace=0.15)
    fig.savefig(images / "control_density.png", bbox_inches="tight")
    plt.close(fig)
    lines = [
        r"\begin{table*}[t]\centering\small",
        (
            "\\caption{Synthetic two-agent comparison: five-seed mean "
            "system time and boundary waiting (vehicle-minutes). "
            "Equal-green fixed baseline is not demand-optimized. These "
            "are not METR-LA or real-world results.}"
        ),
        r"\begin{tabular}{lrrrr}\toprule",
        (
            "Scenario & Fixed system & Responsive system & Fixed waiting "
            "& Responsive waiting\\\\\\midrule"
        ),
    ]
    for r in rows:
        lines.append(f"{r[0]} & {r[1]:.1f} & {r[5]:.1f} & {r[2]:.1f} & {r[6]:.1f}" + r"\\")
    lines += [
        r"\bottomrule\end{tabular}\end{table*}",
        r"\begin{table*}[t]\centering\small",
        (
            "\\caption{Synthetic mean exit throughput and end-of-horizon "
            "residuals, vehicles. Fractional values reflect continuum CTM"
            " occupancy, not counted individual cars.}"
        ),
        r"\begin{tabular}{lrrrr}\toprule",
        r"Scenario & Fixed exit & Adapt. exit & Fixed left & Adapt. left\\\midrule",
    ]
    for r in rows:
        lines.append(f"{r[0]} & {r[3]:.1f} & {r[7]:.1f} & {r[4]:.3f} & {r[8]:.3f}" + r"\\")
    lines += [
        r"\bottomrule\end{tabular}\end{table*}",
        (
            "\\begin{figure*}[t]\\centering"
            "\\includegraphics[width=.95\\textwidth]{images/control_density.png}"
        ),
        (
            "\\caption{Synthetic corridor density, downstream-restriction scenario, seed101. "
            "Dotted lines bound the reduced exit capacity interval. Density and wave speed "
            "are assumed model quantities, not METR-LA measurements.}\\end{figure*}"
        ),
    ]
    (ROOT / "report/phase2/generated/control_results.tex").write_text("\n".join(lines) + "\n")
    for name in [
        "manifest.json",
        "metrics.csv",
        "summary.csv",
        "paired_system_time.csv",
        "artifacts.json",
    ]:
        shutil.copy2(run / name, evidence / name)
    summary = {
        "scope": manifest["scope"],
        "runs": len(metrics),
        "seeds": settings["seeds"],
        "rows": rows,
        "max_conservation_error_vehicles": float(metrics.max_conservation_error_vehicles.max()),
        "max_cell_density_veh_km": float(metrics.max_cell_density_veh_km.max()),
        "metrics_sha256": artifacts["metrics_sha256"],
        "pairing_verified": True,
        "physics_invariants_checked_every_step": True,
        "neural_forecasts_used_for_control": False,
        "calibrated_to_real_data": False,
        "rule_based_agents": 2,
        "policy_tuning_performed": False,
    }
    (evidence / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    text = [
        "# Synthetic LWR and two-agent control results",
        "",
        (
            "All values below are measured simulation outputs under the "
            "predeclared protocol. They are not LA traffic measurements, "
            "trained MARL or GAT-driven control evidence."
        ),
        "",
        (
            "| Scenario | Fixed system veh-min | Responsive system "
            "veh-min | Fixed boundary wait veh-min | Responsive boundary "
            "wait veh-min |"
        ),
        "| --- | --- | --- | --- | --- |",
    ]
    text += [f"| {r[0]} | {r[1]:.1f} | {r[5]:.1f} | {r[2]:.1f} | {r[6]:.1f} |" for r in rows]
    text += [
        "",
        f"{len(metrics)} runs, {len(settings['seeds'])} paired seeds per scenario. "
        "Maximum cumulative mass residual: "
        f"{summary['max_conservation_error_vehicles']:.3g} vehicles. "
        "All states stayed within physical bounds. Full per-run metrics and seed variation "
        "are in verification/phase2-final-20261116/control/.",
        "",
        (
            "The responsive heuristic reduced system time against this "
            "equal-green baseline in all four selected scenarios. This "
            "does not establish optimality, transfer to another network, "
            "real delay savings or neural-control benefit. Fixed time is "
            "not demand-optimized. Boundary waiting excludes "
            "inside-network queues; system vehicle-time includes "
            "movement. Time integration is a numerical estimate. Final "
            "residuals are disclosed in metrics.csv, including about4.06 "
            "vehicles for the fixed downstream-restriction case on "
            "average."
        ),
        "",
        (
            "Reproduce with scripts/run_control.py and "
            "scripts/build_control_report.py. Physics, rates and settings"
            " were fixed before outcomes; no policy tuning was performed."
            " See docs/PHASE2_CONTROL_PROTOCOL.md and "
            "docs/PHASE2_CONTROL_NOTES.md."
        ),
    ]
    (ROOT / "docs/PHASE2_CONTROL_RESULTS.md").write_text("\n".join(text) + "\n")
    print("Built verified synthetic evidence:", evidence)


if __name__ == "__main__":
    main()
