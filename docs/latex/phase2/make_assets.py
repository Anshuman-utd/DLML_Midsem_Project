"""Build the tables and figures of the Phase 2 report from frozen evidence.

Nothing is trained, tuned or re-scored here. Every number is read from the
small evidence files committed under ``verification/``:

- verification/phase2-20261112/                 forecasting metrics and selection records
- verification/phase2-final-20261116/control/   synthetic control metrics

Usage (from the repository root):

    python docs/latex/phase2/make_assets.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FORECAST = ROOT / "verification/phase2-20261112"
CONTROL = ROOT / "verification/phase2-final-20261116/control"
FIG = HERE / "figures"
GEN = HERE / "generated"

# One fixed colour per method, reused in every figure and in the slides.
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C = {
    "graph": "#2a78d6",
    "temporal": "#eb6834",
    "xgb": "#1baf7a",
    "rf": "#eda100",
    "context": "#8a8984",
    "responsive": "#6250d6",
}
ONE_COL = 3.45

MAIN = [
    ("M0_persistence", "Persistence"),
    ("M1_ha", "Historical average"),
    ("M3_rf", "Random Forest"),
    ("M4_xgb", "XGBoost"),
    ("temporal", "Temporal GRU"),
    ("graph", "GRU + GAT"),
]
VARIANTS = [
    ("graph", "GRU + GAT (full model)"),
    ("self", "Self-loop only"),
    ("uniform", "Uniform neighbours"),
    ("no_dropout", "No dropout"),
]
SCENARIOS = [
    ("balanced", "Balanced"),
    ("arterial_peak", "Arterial peak"),
    ("side_peak", "Side-road peak"),
    ("downstream_restriction", "Downstream limit"),
]


def style():
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 7.5,
            "axes.labelsize": 7.5,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.5,
            "axes.axisbelow": True,
            "legend.frameon": False,
            "pdf.fonttype": 42,
        }
    )


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("figure", name)


def write(name, lines):
    GEN.mkdir(parents=True, exist_ok=True)
    (GEN / name).write_text("\n".join(lines) + "\n")
    print("table ", name)


def seed_stats(frame, mode, metric, minutes, part="all"):
    """Mean and sample standard deviation over seeds (one value for the Phase 1 references)."""
    rows = frame[
        (frame["mode"] == mode)
        & (frame["split"] == "test")
        & (frame["slice"] == part)
        & (frame["minutes"] == minutes)
    ]
    values = rows[metric].to_numpy(float)
    if not len(values):
        raise KeyError((mode, metric, minutes, part))
    return values.mean(), (values.std(ddof=1) if len(values) > 1 else None)


def at_seed(frame, mode, minutes, seed=42):
    rows = frame[
        (frame["mode"] == mode)
        & (frame["split"] == "test")
        & (frame["slice"] == "all")
        & (frame["minutes"] == minutes)
        & (frame["seed"] == seed)
    ]
    if len(rows) != 1:
        raise KeyError((mode, minutes, seed))
    return float(rows["MAE"].iloc[0])


def cell(mean, std):
    return f"{mean:.3f}" if std is None else f"{mean:.3f}\\,$\\pm$\\,{std:.3f}"


def table_main(frame, numbers):
    best = {
        (metric, minutes): min(seed_stats(frame, mode, metric, minutes)[0] for mode, _ in MAIN)
        for metric in ("MAE", "RMSE")
        for minutes in (15, 30, 60)
    }
    lines = []
    numbers["main"] = {}
    for mode, label in MAIN:
        cells = []
        numbers["main"][label] = {}
        for metric in ("MAE", "RMSE"):
            for minutes in (15, 30, 60):
                mean, std = seed_stats(frame, mode, metric, minutes)
                is_best = abs(mean - best[metric, minutes]) < 1e-12
                cells.append(f"\\textbf{{{mean:.3f}}}" if is_best else cell(mean, std))
                numbers["main"][label][f"{metric}{minutes}"] = mean
        if mode == "temporal":
            lines.append("\\midrule")
        lines.append(f"{label} & " + " & ".join(cells) + "\\\\")
    write("table_main.tex", lines)


def table_ablation(frame, numbers):
    full = at_seed(frame, "graph", 60)
    lines = []
    numbers["ablation_seed42"] = {}
    for mode, label in VARIANTS:
        values = [at_seed(frame, mode, m) for m in (15, 30, 60)]
        change = "---" if mode == "graph" else f"{values[2] - full:+.3f}"
        lines.append(f"{label} & " + " & ".join(f"{v:.3f}" for v in values) + f" & {change}\\\\")
        numbers["ablation_seed42"][label] = values
    lines.append("\\midrule")
    lines.append("\\multicolumn{5}{@{}l}{\\emph{Mean over seeds 42, 43, 44}}\\\\")
    full_mean = seed_stats(frame, "graph", "MAE", 60)[0]
    numbers["three_seed"] = {}
    for mode, label in [VARIANTS[0], VARIANTS[1], ("temporal", "Temporal GRU")]:
        stats = [seed_stats(frame, mode, "MAE", m) for m in (15, 30, 60)]
        change = "---" if mode == "graph" else f"{stats[2][0] - full_mean:+.3f}"
        lines.append(f"{label} & " + " & ".join(f"{a:.3f}" for a, _ in stats) + f" & {change}\\\\")
        numbers["three_seed"][label] = [[a, b] for a, b in stats]
    write("table_ablation.tex", lines)


def table_hybrid(frame, numbers):
    hybrid = json.loads((FORECAST / "hybrid_selection.json").read_text())
    picked = hybrid["selected"]["alpha_xgb"]
    lines = []
    for row in hybrid["candidates"]:
        mark = "$\\checkmark$" if row["alpha_xgb"] == picked else ""
        lines.append(
            f"{row['alpha_xgb']:.2f} & {1 - row['alpha_xgb']:.2f} & "
            f"{row['val_stack_headline_mae']:.4f} & {mark}\\\\"
        )
    write("table_hybrid.tex", lines)
    numbers["hybrid"] = hybrid
    numbers["hybrid_test_mae"] = {
        "XGBoost": [seed_stats(frame, "M4_xgb", "MAE", m)[0] for m in (15, 30, 60)],
        "Selected blend": [at_seed(frame, "hybrid", m) for m in (15, 30, 60)],
    }


def table_control(numbers):
    metrics = pd.read_csv(CONTROL / "metrics.csv")
    paired = pd.read_csv(CONTROL / "paired_system_time.csv")
    mean = metrics.groupby(["scenario", "policy"]).mean(numeric_only=True)
    lines = []
    numbers["control"] = {}
    for key, label in SCENARIOS:
        fixed, responsive = mean.loc[(key, "fixed")], mean.loc[(key, "responsive")]
        reduction = paired.loc[paired["scenario"] == key, "reduction_percent"]
        line = (
            f"{label} & {fixed['system_vehicle_minutes']:,.0f} & "
            f"{responsive['system_vehicle_minutes']:,.0f} & {reduction.mean():.0f} & "
            f"{fixed['boundary_wait_vehicle_minutes']:,.1f} & "
            f"{responsive['boundary_wait_vehicle_minutes']:,.1f}\\\\"
        )
        lines.append(line.replace(",", "{,}"))
        numbers["control"][label] = {
            "fixed_system": float(fixed["system_vehicle_minutes"]),
            "responsive_system": float(responsive["system_vehicle_minutes"]),
            "reduction_percent": float(reduction.mean()),
            "fixed_wait": float(fixed["boundary_wait_vehicle_minutes"]),
            "responsive_wait": float(responsive["boundary_wait_vehicle_minutes"]),
            "fixed_residual": float(fixed["residual_vehicles"]),
        }
    numbers["control_checks"] = {
        "runs": int(len(metrics)),
        "max_conservation_error": float(metrics["max_conservation_error_vehicles"].max()),
        "max_density": float(metrics["max_cell_density_veh_km"].max()),
        "pairs_improved": int((paired["reduction_percent"] > 0).sum()),
        "pairs": int(len(paired)),
    }
    write("table_control.tex", lines)


def fig_horizons(frame, numbers):
    minutes = list(range(5, 65, 5))
    looks = {
        "M0_persistence": (C["context"], (0, (4, 2)), 1.2),
        "M1_ha": (C["context"], (0, (1, 1.6)), 1.2),
        "M3_rf": (C["rf"], "-", 1.6),
        "M4_xgb": (C["xgb"], "-", 1.6),
        "temporal": (C["temporal"], "-", 1.6),
        "graph": (C["graph"], "-", 1.6),
    }
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.6))
    numbers["mae_by_horizon"] = {"minutes": minutes}
    for mode, label in MAIN:
        curve = [seed_stats(frame, mode, "MAE", m)[0] for m in minutes]
        colour, dash, width = looks[mode]
        ax.plot(minutes, curve, color=colour, ls=dash, lw=width, label=label)
        numbers["mae_by_horizon"][label] = curve
    ax.set(xlabel="Forecast horizon (minutes)", ylabel="Test MAE (mph)", xlim=(5, 60))
    ax.set_xticks([5, 15, 30, 45, 60])
    ax.set_ylim(1.4, 6.9)
    ax.legend(loc="upper left", ncol=2, handlelength=2.2, columnspacing=1.0, borderaxespad=0.2)
    ax.text(
        59.3,
        1.62,
        "Overlapping: GRU with GRU + GAT; RF with XGBoost",
        ha="right",
        va="center",
        color=MUTED,
        fontsize=6.5,
    )
    save(fig, "horizons")


def fig_ablation(frame):
    rows = [
        ("temporal", "Temporal GRU\n(no graph layer)"),
        ("self", "Self-loop only\n(no neighbours)"),
        ("uniform", "Uniform neighbours\n(no learned weights)"),
        ("graph", "GRU + GAT (full)"),
        ("no_dropout", "No dropout"),
    ]
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.35))
    for y, (mode, _) in enumerate(rows):
        seeds = frame[(frame["mode"] == mode) & (frame["split"] == "test")]["seed"].dropna()
        for seed in sorted(seeds.unique()):
            filled = seed == 42
            ax.plot(
                at_seed(frame, mode, 60, int(seed)),
                y,
                "o",
                ms=5.5,
                mfc=C["graph"] if filled else "white",
                mec=C["graph"],
                mew=1.1,
                zorder=3 if filled else 2,
            )
        value = at_seed(frame, mode, 60)
        ax.annotate(
            f"{value:.3f}",
            (value, y),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=6.5,
        )
    ax.axvline(at_seed(frame, "graph", 60), color=C["graph"], lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.set_yticks(range(len(rows)), [label for _, label in rows])
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.invert_yaxis()
    ax.set_xlabel("60-minute test MAE (mph); lower is better")
    ax.grid(axis="y", visible=False)
    marks = [
        plt.Line2D([], [], marker="o", ls="", ms=5.5, mfc=C["graph"], mec=C["graph"]),
        plt.Line2D([], [], marker="o", ls="", ms=5.5, mfc="white", mec=C["graph"]),
    ]
    ax.legend(
        marks,
        ["Seed 42", "Seeds 43, 44"],
        loc="lower left",
        bbox_to_anchor=(0, 1.0),
        ncol=2,
        borderaxespad=0.1,
    )
    save(fig, "ablation")


def fig_control_bars():
    metrics = pd.read_csv(CONTROL / "metrics.csv")
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.45))
    width = 0.38
    policies = [
        (-width / 2 - 0.02, "fixed", C["context"], "Fixed time (equal green)"),
        (width / 2 + 0.02, "responsive", C["responsive"], "Responsive rule"),
    ]
    for offset, policy, colour, label in policies:
        for x, (key, _) in enumerate(SCENARIOS):
            runs = metrics[(metrics["scenario"] == key) & (metrics["policy"] == policy)]
            values = runs["system_vehicle_minutes"].to_numpy() / 1000
            ax.bar(x + offset, values.mean(), width, color=colour, label=label if x == 0 else None)
            ax.plot(
                np.full(len(values), x + offset),
                values,
                "o",
                ms=2.6,
                mfc="white",
                mec=INK,
                mew=0.5,
                zorder=3,
            )
            ax.annotate(
                f"{values.mean():.1f}",
                (x + offset, values.max()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=6.5,
            )
    ax.set_xticks(range(len(SCENARIOS)), [label.replace(" ", "\n", 1) for _, label in SCENARIOS])
    ax.set_ylabel("System time (thousand vehicle-minutes)")
    ax.grid(axis="x", visible=False)
    ax.set_ylim(0, 17.5)
    ax.legend(loc="upper left", borderaxespad=0.1)
    save(fig, "control_bars")


def extra_numbers(frame, numbers):
    """Values quoted in the text and the slides but not shown in a table."""
    summary = json.loads((FORECAST / "summary.json").read_text())
    numbers["headline_valid_counts"] = summary["headline_valid_counts"]
    numbers["sensors_improved_seed42"] = {
        "improved": summary["sensor_graph_improved_seed42"],
        "total": summary["total_sensors"],
    }
    numbers["tuning"] = json.loads((FORECAST / "tuning.json").read_text())
    numbers["gain_vs_self_by_horizon"] = {
        m: float(
            np.mean(
                [at_seed(frame, "self", m, s) - at_seed(frame, "graph", m, s) for s in (42, 43, 44)]
            )
        )
        for m in range(5, 65, 5)
    }
    numbers["peak_offpeak_mae60"] = {
        label: {
            part: seed_stats(frame, mode, "MAE", 60, part=part)[0] for part in ("peak", "off_peak")
        }
        for mode, label in MAIN[2:]
    }
    runs = pd.DataFrame(json.loads((FORECAST / "experiments.json").read_text()))
    runs["parameters"] = pd.to_numeric(runs["parameters"])
    numbers["parameters"] = {
        mode: int(runs.loc[runs["mode"] == mode, "parameters"].iloc[0])
        for mode in ("temporal", "graph")
    }


def main():
    style()
    frame = pd.read_csv(FORECAST / "all_metrics.csv")
    frame["seed"] = frame["seed"].astype("Int64")
    numbers = {"sources": [str(FORECAST.relative_to(ROOT)), str(CONTROL.relative_to(ROOT))]}
    table_main(frame, numbers)
    table_ablation(frame, numbers)
    table_hybrid(frame, numbers)
    table_control(numbers)
    fig_horizons(frame, numbers)
    fig_ablation(frame)
    fig_control_bars()
    extra_numbers(frame, numbers)
    (GEN / "numbers.json").write_text(json.dumps(numbers, indent=2) + "\n")
    print("wrote ", GEN / "numbers.json")


if __name__ == "__main__":
    main()
