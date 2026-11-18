"""Build the tables and figures of the Phase 2 report from frozen evidence.

Nothing is trained, tuned or re-scored here. Every number is read from the
small evidence files committed under ``verification/``:

- verification/phase2-20261112/        forecasting metrics, histories, selection
- verification/phase2-final-20261116/  synthetic control metrics

Two figures need local, git-ignored inputs and are skipped when those are absent:

- the sensor map needs data/raw/sensor_graph/graph_sensor_locations.csv
- the density figure needs trajectories from ``scripts/run_control.py``
  (pass ``--control-run DIR``; the run is deterministic)

Usage (from the repository root):

    python report/phase2_report/make_assets.py [--control-run DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FORECAST = ROOT / "verification/phase2-20261112"
CONTROL = ROOT / "verification/phase2-final-20261116/control"
FIG = HERE / "figures"
GEN = HERE / "generated"

# Fixed colour per entity, reused in every figure and in the slides.
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C = {
    "graph": "#2a78d6",  # GRU + GAT
    "temporal": "#eb6834",  # temporal GRU
    "xgb": "#1baf7a",
    "rf": "#eda100",
    "context": "#8a8984",  # naive references and the fixed-time baseline
    "responsive": "#6250d6",
}
SEQ = LinearSegmentedColormap.from_list(
    "seq_blue", ["#f4f8fe", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
)
DIV = LinearSegmentedColormap.from_list(
    "div_red_blue", ["#b3261e", "#e34948", "#f0efec", "#2a78d6", "#104281"]
)
ONE_COL, TWO_COL = 3.45, 7.1

MAIN = [
    ("M0_persistence", "Persistence"),
    ("M1_ha", "Historical average"),
    ("M3_rf", "Random Forest"),
    ("M4_xgb", "XGBoost"),
    ("temporal", "Temporal GRU"),
    ("graph", "GRU + GAT"),
]
VARIANTS = [
    ("graph", "GRU + GAT (full)"),
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
NEURAL = {"temporal", "graph", "self", "uniform", "no_dropout"}


def style():
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 7.5,
            "axes.titlesize": 8,
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
            "savefig.dpi": 300,
        }
    )


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", pad_inches=0.04, dpi=300)
    plt.close(fig)
    print("figure", name)


def write(name, text):
    GEN.mkdir(parents=True, exist_ok=True)
    (GEN / name).write_text(text.rstrip() + "\n")
    print("table ", name)


# --------------------------------------------------------------------------- data


def load_forecast():
    frame = pd.read_csv(FORECAST / "all_metrics.csv")
    frame["seed"] = frame["seed"].astype("Int64")
    return frame


def seed_stats(frame, mode, metric, minutes, split="test", part="all"):
    """Mean and sample standard deviation over seeds (single value for references)."""
    rows = frame[
        (frame["mode"] == mode)
        & (frame["split"] == split)
        & (frame["slice"] == part)
        & (frame["minutes"] == minutes)
    ]
    values = rows[metric].to_numpy(float)
    if not len(values):
        raise KeyError((mode, metric, minutes, split, part))
    return values.mean(), (values.std(ddof=1) if len(values) > 1 else None), len(values)


def at_seed(frame, mode, metric, minutes, seed=42):
    rows = frame[
        (frame["mode"] == mode)
        & (frame["split"] == "test")
        & (frame["slice"] == "all")
        & (frame["minutes"] == minutes)
        & (frame["seed"] == seed)
    ]
    if len(rows) != 1:
        raise KeyError((mode, metric, minutes, seed))
    return float(rows[metric].iloc[0])


def cell(mean, std):
    return f"{mean:.3f}" if std is None else f"{mean:.3f}\\,$\\pm$\\,{std:.3f}"


# ------------------------------------------------------------------------- tables


def table_main(frame, numbers):
    lines, best = [], {}
    for metric in ("MAE", "RMSE"):
        for minutes in (15, 30, 60):
            best[metric, minutes] = min(
                seed_stats(frame, mode, metric, minutes)[0] for mode, _ in MAIN
            )
    for mode, label in MAIN:
        cells = []
        for metric in ("MAE", "RMSE"):
            for minutes in (15, 30, 60):
                mean, std, _ = seed_stats(frame, mode, metric, minutes)
                text = cell(mean, std)
                if abs(mean - best[metric, minutes]) < 1e-12:
                    text = f"\\textbf{{{mean:.3f}}}"
                cells.append(text)
                numbers.setdefault("main", {}).setdefault(label, {})[f"{metric}{minutes}"] = mean
        if mode == "temporal":
            lines.append("\\midrule")
        lines.append(f"{label} & " + " & ".join(cells) + "\\\\")
    write("table_main.tex", "\n".join(lines))


def table_tuning(numbers):
    tuning = json.loads((FORECAST / "tuning.json").read_text())
    selected = json.loads((FORECAST / "selected.json").read_text())
    chosen = {(k, v["learning_rate"]) for k, v in selected.items()}
    names = {"temporal": "Temporal GRU", "graph": "GRU + GAT"}
    lines = []
    for row in tuning:
        mark = "$\\checkmark$" if (row["mode"], row["learning_rate"]) in chosen else ""
        lines.append(
            f"{names[row['mode']]} & {row['learning_rate']:g} & {row['validation_mae']:.4f} & "
            f"{row['epochs']} & {mark}\\\\"
        )
    numbers["tuning"] = [
        {k: row[k] for k in ("mode", "learning_rate", "validation_mae", "epochs")} for row in tuning
    ]
    write("table_tuning.tex", "\n".join(lines))


def table_ablation(frame, numbers):
    lines = []
    full42 = at_seed(frame, "graph", "MAE", 60)
    numbers["ablation_seed42"] = {}
    for mode, label in VARIANTS:
        values = [at_seed(frame, mode, "MAE", m) for m in (15, 30, 60)]
        delta = values[2] - full42
        change = "---" if mode == "graph" else f"{delta:+.3f}"
        lines.append(f"{label} & " + " & ".join(f"{v:.3f}" for v in values) + f" & {change}\\\\")
        numbers["ablation_seed42"][label] = values
    lines.append("\\midrule")
    lines.append("\\multicolumn{5}{@{}l}{\\emph{Mean over seeds 42, 43, 44}}\\\\")
    numbers["three_seed"] = {}
    for mode, label in [
        ("graph", "GRU + GAT (full)"),
        ("self", "Self-loop only"),
        ("temporal", "Temporal GRU"),
    ]:
        stats = [seed_stats(frame, mode, "MAE", m) for m in (15, 30, 60)]
        full = seed_stats(frame, "graph", "MAE", 60)[0]
        change = "---" if mode == "graph" else f"{stats[2][0] - full:+.3f}"
        lines.append(
            f"{label} & " + " & ".join(f"{a:.3f}" for a, _, _ in stats) + f" & {change}\\\\"
        )
        numbers["three_seed"][label] = [[a, b] for a, b, _ in stats]
    write("table_ablation.tex", "\n".join(lines))


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
    write("table_hybrid.tex", "\n".join(lines))
    numbers["hybrid"] = hybrid
    numbers["hybrid_test"] = {
        "XGBoost": [seed_stats(frame, "M4_xgb", "MAE", m)[0] for m in (15, 30, 60)],
        "Graph seed 42": [at_seed(frame, "graph", "MAE", m) for m in (15, 30, 60)],
        "Selected blend": [at_seed(frame, "hybrid", "MAE", m) for m in (15, 30, 60)],
    }


def table_slices(frame, numbers):
    lines = []
    numbers["slices"] = {}
    for mode, label in MAIN[2:]:
        values = [
            seed_stats(frame, mode, "MAE", 60, part=p)[0]
            for p in ("peak", "off_peak", "weekday", "weekend")
        ]
        lines.append(f"{label} & " + " & ".join(f"{v:.3f}" for v in values) + "\\\\")
        numbers["slices"][label] = values
    write("table_slices.tex", "\n".join(lines))


def table_cost(numbers):
    runs = pd.DataFrame(json.loads((FORECAST / "experiments.json").read_text()))
    for column in ("epochs", "parameters", "seconds", "validation_mae"):
        runs[column] = pd.to_numeric(runs[column])
    names = {"temporal": "Temporal GRU", **dict(VARIANTS)}
    lines = []
    numbers["cost"] = {}
    for mode in ("temporal", "graph", "self", "uniform", "no_dropout"):
        rows = runs[runs["mode"] == mode]
        low, high = int(rows["epochs"].min()), int(rows["epochs"].max())
        epochs = f"{low}" if low == high else f"{low}--{high}"
        minutes = rows["seconds"].mean() / 60
        lines.append(
            f"{names[mode]} & {int(rows['parameters'].iloc[0]):,} & {len(rows)} & {epochs} & "
            f"{minutes:.1f}\\\\"
        )
        numbers["cost"][names[mode]] = {
            "parameters": int(rows["parameters"].iloc[0]),
            "fits": len(rows),
            "epochs": [low, high],
            "minutes": minutes,
        }
    write("table_cost.tex", "\n".join(lines).replace(",", "{,}"))


def table_control(numbers):
    metrics = pd.read_csv(CONTROL / "metrics.csv")
    paired = pd.read_csv(CONTROL / "paired_system_time.csv")
    mean = metrics.groupby(["scenario", "policy"]).mean(numeric_only=True)
    lines = []
    numbers["control"] = {}
    for key, label in SCENARIOS:
        fixed, responsive = mean.loc[(key, "fixed")], mean.loc[(key, "responsive")]
        reduction = paired.loc[paired["scenario"] == key, "reduction_percent"]
        lines.append(
            f"{label} & {fixed['system_vehicle_minutes']:,.0f} & "
            f"{responsive['system_vehicle_minutes']:,.0f} & {reduction.mean():.0f} & "
            f"{fixed['boundary_wait_vehicle_minutes']:,.1f} & "
            f"{responsive['boundary_wait_vehicle_minutes']:,.1f} & "
            f"{fixed['residual_vehicles']:.2f} & {responsive['residual_vehicles']:.2f}\\\\"
        )
        numbers["control"][label] = {
            "fixed_system": float(fixed["system_vehicle_minutes"]),
            "responsive_system": float(responsive["system_vehicle_minutes"]),
            "reduction_percent_mean": float(reduction.mean()),
            "reduction_percent_min": float(reduction.min()),
            "reduction_percent_max": float(reduction.max()),
            "fixed_wait": float(fixed["boundary_wait_vehicle_minutes"]),
            "responsive_wait": float(responsive["boundary_wait_vehicle_minutes"]),
            "fixed_residual": float(fixed["residual_vehicles"]),
            "responsive_residual": float(responsive["residual_vehicles"]),
        }
    numbers["control_checks"] = {
        "runs": int(len(metrics)),
        "max_conservation_error": float(metrics["max_conservation_error_vehicles"].max()),
        "max_density": float(metrics["max_cell_density_veh_km"].max()),
        "pairs_improved": int((paired["reduction_percent"] > 0).sum()),
        "pairs": int(len(paired)),
    }
    write("table_control.tex", "\n".join(lines).replace(",", "{,}"))


# ------------------------------------------------------------------------ figures


def fig_horizons(frame, numbers):
    minutes = np.arange(5, 65, 5)
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(TWO_COL, 2.55), gridspec_kw={"width_ratios": [1.25, 1], "wspace": 0.28}
    )
    styles = {
        "M0_persistence": (C["context"], (0, (4, 2)), 1.2),
        "M1_ha": (C["context"], (0, (1, 1.6)), 1.2),
        "M3_rf": (C["rf"], "-", 1.6),
        "M4_xgb": (C["xgb"], "-", 1.6),
        "temporal": (C["temporal"], "-", 1.6),
        "graph": (C["graph"], "-", 1.6),
    }
    curves = {}
    for mode, label in MAIN:
        curves[mode] = [seed_stats(frame, mode, "MAE", m)[0] for m in minutes]
        colour, dash, width = styles[mode]
        left.plot(minutes, curves[mode], color=colour, ls=dash, lw=width, label=label)
    left.set(xlabel="Forecast horizon (minutes)", ylabel="Test MAE (mph)", xlim=(5, 60))
    left.set_xticks([5, 15, 30, 45, 60])
    left.set_title("(a) Test MAE by forecast horizon", loc="left")
    left.legend(loc="upper left", ncol=2, handlelength=2.2, columnspacing=1.2, borderaxespad=0.2)
    left.set_ylim(1.4, 6.6)
    left.text(
        59.3,
        1.62,
        "Overlapping lines: GRU with GRU + GAT; RF with XGBoost",
        ha="right",
        va="center",
        color=MUTED,
        fontsize=6.5,
    )

    def paired_gain(other):
        gains = []
        for m in minutes:
            diffs = [
                at_seed(frame, other, "MAE", m, s) - at_seed(frame, "graph", "MAE", m, s)
                for s in (42, 43, 44)
            ]
            gains.append((np.mean(diffs), np.std(diffs, ddof=1)))
        return np.array(gains)

    for other, colour, label in [
        ("self", C["graph"], "vs. self-loop control"),
        ("temporal", C["temporal"], "vs. temporal GRU"),
    ]:
        gain = paired_gain(other)
        right.fill_between(
            minutes,
            gain[:, 0] - gain[:, 1],
            gain[:, 0] + gain[:, 1],
            color=colour,
            alpha=0.18,
            lw=0,
        )
        right.plot(minutes, gain[:, 0], color=colour, lw=1.6, marker="o", ms=3, label=label)
        numbers.setdefault("gain_by_horizon", {})[other] = {
            int(m): float(g) for m, g in zip(minutes, gain[:, 0], strict=True)
        }
    right.axhline(0, color=MUTED, lw=0.6)
    right.set(xlabel="Forecast horizon (minutes)", ylabel="MAE reduction from GAT (mph)")
    right.set_xticks([5, 15, 30, 45, 60])
    right.set_ylim(bottom=-0.005)
    right.set_title("(b) Gain from the graph layer", loc="left")
    right.legend(loc="upper left", borderaxespad=0.2)
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
        seeds = sorted(
            frame[(frame["mode"] == mode) & (frame["split"] == "test")]["seed"].dropna().unique()
        )
        for seed in seeds:
            value = at_seed(frame, mode, "MAE", 60, int(seed))
            filled = seed == 42
            ax.plot(
                value,
                y,
                "o",
                ms=5.5,
                mfc=C["graph"] if filled else "white",
                mec=C["graph"],
                mew=1.1,
                zorder=3 if filled else 2,
            )
        value = at_seed(frame, mode, "MAE", 60)
        ax.annotate(
            f"{value:.3f}",
            (value, y),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=6.5,
            color=INK,
        )
    reference = at_seed(frame, "graph", "MAE", 60)
    ax.axvline(reference, color=C["graph"], lw=0.7, ls=(0, (3, 2)), zorder=1)
    ax.set_yticks(range(len(rows)), [label for _, label in rows])
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.invert_yaxis()
    ax.set_xlabel("60-minute test MAE (mph); lower is better")
    ax.grid(axis="y", visible=False)
    handles = [
        plt.Line2D(
            [], [], marker="o", ls="", ms=5.5, mfc=C["graph"], mec=C["graph"], label="Seed 42"
        ),
        plt.Line2D(
            [], [], marker="o", ls="", ms=5.5, mfc="white", mec=C["graph"], label="Seeds 43, 44"
        ),
    ]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, borderaxespad=0.1)
    save(fig, "ablation")


def fig_learning():
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.2))
    for folder, colour, label in [
        ("tune_temporal_0", C["temporal"], "Temporal GRU"),
        ("tune_graph_0", C["graph"], "GRU + GAT"),
    ]:
        history = pd.DataFrame(json.loads((FORECAST / folder / "history.json").read_text()))
        ax.plot(
            history["epoch"], history["validation_headline_mae"], color=colour, lw=1.6, label=label
        )
        best = history.loc[history["validation_headline_mae"].idxmin()]
        ax.plot(
            best["epoch"],
            best["validation_headline_mae"],
            "o",
            ms=5.5,
            mfc="white",
            mec=colour,
            mew=1.3,
        )
        first = folder == "tune_temporal_0"
        ax.annotate(
            f"best: epoch {int(best['epoch'])} ({best['validation_headline_mae']:.3f})",
            (best["epoch"], best["validation_headline_mae"]),
            xytext=(6, -13) if first else (-6, -14),
            textcoords="offset points",
            ha="left" if first else "right",
            fontsize=6.5,
            color=INK,
        )
    ax.set(xlabel="Epoch", ylabel="Validation MAE, 15/30/60 min (mph)")
    ax.set_ylim(bottom=ax.get_ylim()[0] - 0.008)
    ax.legend(loc="upper right")
    save(fig, "learning")


def fig_hybrid():
    hybrid = json.loads((FORECAST / "hybrid_selection.json").read_text())
    weights = [row["alpha_xgb"] for row in hybrid["candidates"]]
    scores = [row["val_stack_headline_mae"] for row in hybrid["candidates"]]
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.0))
    ax.plot(weights, scores, color=MUTED, lw=1.4, zorder=1)
    colours = [C["graph"]] + [MUTED] * 3 + [C["xgb"]]
    for weight, score, colour in zip(weights, scores, colours, strict=True):
        ax.plot(weight, score, "o", ms=6, color=colour, zorder=2)
        ax.annotate(
            f"{score:.3f}",
            (weight, score),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=6.5,
        )
    ax.annotate(
        "pure GRU + GAT",
        (0, scores[0]),
        xytext=(6, -11),
        textcoords="offset points",
        color=MUTED,
        fontsize=6.5,
    )
    ax.annotate(
        "selected: pure XGBoost",
        (1, scores[-1]),
        xytext=(8, -14),
        textcoords="offset points",
        ha="right",
        color=MUTED,
        fontsize=6.5,
    )
    ax.set(xlabel="XGBoost weight $\\lambda$ in the blend", ylabel="Reserved-validation MAE (mph)")
    ax.set_xticks(weights)
    ax.set_ylim(min(scores) - 0.12, max(scores) + 0.1)
    ax.set_xlim(-0.08, 1.08)
    save(fig, "hybrid")


def fig_sensor_map(numbers):
    locations = ROOT / "data/raw/sensor_graph/graph_sensor_locations.csv"
    if not locations.exists():
        print("skip   sensor_map (graph_sensor_locations.csv not downloaded)")
        return
    place = pd.read_csv(locations).set_index("sensor_id")
    errors = pd.read_csv(FORECAST / "per_sensor_mae_60.csv").pivot(
        index="sensor_id", columns="model", values="mae_60"
    )
    gain = (errors["self_seed42"] - errors["graph_seed42"]).reindex(place.index)
    if gain.isna().any():
        raise ValueError("sensor ids differ between evidence and location file")
    limit = float(np.ceil(np.abs(gain).quantile(0.98) * 20) / 20)
    order = np.argsort(np.abs(gain.to_numpy()))
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.75))
    points = ax.scatter(
        place["longitude"].to_numpy()[order],
        place["latitude"].to_numpy()[order],
        c=gain.to_numpy()[order],
        cmap=DIV,
        norm=TwoSlopeNorm(0, -limit, limit),
        s=16,
        edgecolors="white",
        linewidths=0.4,
    )
    ax.set_aspect(1 / np.cos(np.deg2rad(place["latitude"].mean())))
    ax.set(xlabel="Longitude", ylabel="Latitude")
    ax.grid(visible=False)
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
    bar = fig.colorbar(points, ax=ax, fraction=0.04, pad=0.02, extend="both")
    bar.set_label("MAE change, self-loop $-$ GAT (mph)\nblue: neighbours help", fontsize=6.5)
    bar.outline.set_visible(False)
    numbers["sensor_gain"] = {
        "improved": int((gain > 0).sum()),
        "worse": int((gain < 0).sum()),
        "total": int(len(gain)),
        "median": float(gain.median()),
        "colour_limit": limit,
    }
    save(fig, "sensor_map")


def fig_control_bars():
    metrics = pd.read_csv(CONTROL / "metrics.csv")
    fig, ax = plt.subplots(figsize=(ONE_COL, 2.45))
    width = 0.38
    for offset, policy, colour, label in [
        (-width / 2 - 0.02, "fixed", C["context"], "Fixed time (equal green)"),
        (width / 2 + 0.02, "responsive", C["responsive"], "Responsive rule"),
    ]:
        for x, (key, _) in enumerate(SCENARIOS):
            runs = metrics[(metrics["scenario"] == key) & (metrics["policy"] == policy)]
            values = runs["system_vehicle_minutes"].to_numpy() / 1000
            ax.bar(
                x + offset,
                values.mean(),
                width,
                color=colour,
                label=label if x == 0 else None,
                zorder=2,
            )
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


def fig_control_density(run_dir, settings):
    names = (
        []
        if run_dir is None
        else [run_dir / f"downstream_restriction_101_{p}.npz" for p in ("fixed", "responsive")]
    )
    if not names or not all(n.exists() for n in names):
        print("skip   control_density (no trajectories; pass --control-run)")
        return
    dt_minutes = settings["dt_seconds"] / 60
    fig, axes = plt.subplots(
        1, 2, figsize=(TWO_COL, 2.1), sharey=True, gridspec_kw={"wspace": 0.06}
    )
    for ax, name, title in zip(
        axes, names, ["(a) Fixed time (equal green)", "(b) Responsive rule"], strict=True
    ):
        cells = np.load(name)["cells"][:, :6] / settings["cell_km"]
        image = ax.imshow(
            cells.T,
            aspect="auto",
            origin="lower",
            cmap=SEQ,
            vmin=0,
            vmax=settings["jam_density_veh_km"],
            extent=(0, len(cells) * dt_minutes, -0.5, 5.5),
            interpolation="nearest",
        )
        for minute in (25, 40):
            ax.axvline(minute, color=INK, lw=0.7, ls=(0, (1, 2)))
        ax.axvline(settings["demand_minutes"], color=MUTED, lw=0.7)
        ax.set_title(title, loc="left")
        ax.set_xlabel("Time (minutes)")
        ax.grid(visible=False)
        ax.set_yticks(range(6), [f"Cell {i}" for i in range(6)])
    axes[0].set_ylabel("Main road, upstream $\\rightarrow$ exit")
    bar = fig.colorbar(image, ax=axes, fraction=0.025, pad=0.015)
    bar.set_label("Density (veh/km); jam = 150")
    bar.outline.set_visible(False)
    save(fig, "control_density")


# --------------------------------------------------------------------------- main


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--control-run", type=Path, default=None)
    args = parser.parse_args()
    style()
    frame = load_forecast()
    numbers = {"sources": [str(FORECAST.relative_to(ROOT)), str(CONTROL.relative_to(ROOT))]}
    summary = json.loads((FORECAST / "summary.json").read_text())
    numbers["headline_valid_counts"] = summary["headline_valid_counts"]
    table_main(frame, numbers)
    table_tuning(numbers)
    table_ablation(frame, numbers)
    table_hybrid(frame, numbers)
    table_slices(frame, numbers)
    table_cost(numbers)
    table_control(numbers)
    fig_horizons(frame, numbers)
    fig_ablation(frame)
    fig_learning()
    fig_hybrid()
    fig_sensor_map(numbers)
    fig_control_bars()
    settings = json.loads((CONTROL / "manifest.json").read_text())["settings"]
    fig_control_density(args.control_run, settings)
    curves = {
        label: [seed_stats(frame, mode, "MAE", m)[0] for m in range(5, 65, 5)]
        for mode, label in MAIN
    }
    numbers["mae_by_horizon"] = {"minutes": list(range(5, 65, 5)), **curves}
    histories = {}
    for folder, label in [("tune_temporal_0", "Temporal GRU"), ("tune_graph_0", "GRU + GAT")]:
        history = json.loads((FORECAST / folder / "history.json").read_text())
        histories[label] = [row["validation_headline_mae"] for row in history]
    numbers["validation_history"] = histories
    (GEN / "numbers.json").write_text(json.dumps(numbers, indent=2) + "\n")
    print("wrote ", GEN / "numbers.json")


if __name__ == "__main__":
    main()
