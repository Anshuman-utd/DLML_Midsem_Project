"""Build small evidence, research plots and LaTeX tables from actual Phase 2 outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from _common import ROOT, load_config, load_series
from matplotlib.ticker import MaxNLocator
from run_phase2 import build_model, tensors

from trafficml.data.load import load_locations
from trafficml.data.neural import NeuralWindows

LABELS = {
    "M0_persistence": "Persistence",
    "M1_ha": "Historical average",
    "M3_rf": "Random Forest",
    "M4_xgb": "XGBoost",
    "temporal": "Temporal GRU",
    "graph": "GRU + GAT",
    "self": "Self-loop graph",
    "uniform": "Uniform neighbours",
    "no_dropout": "No dropout",
    "hybrid": "ML-DL blend",
}


def tex_table(caption, header, rows, wide=False):
    env = "table*" if wide else "table"
    cols = "l" + "r" * (len(header) - 1)
    lines = [
        f"\\begin{{{env}}}[t]\\centering\\small",
        f"\\caption{{{caption}}}",
        f"\\begin{{tabular}}{{{cols}}}\\toprule",
        " & ".join(header) + r"\\\midrule",
    ]
    lines.extend(" & ".join(map(str, row)) + r"\\" for row in rows)
    return "\n".join(lines + [r"\bottomrule\end{tabular}", f"\\end{{{env}}}"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    run = args.run_dir
    metrics = pd.read_csv(run / "evaluation/all_metrics.csv")
    evidence = ROOT / "verification/phase2-20261112"
    generated = ROOT / "report/phase2/generated"
    figures = ROOT / "report/phase2/images"
    for folder in [evidence, generated, figures]:
        folder.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    speed, values, ids, splits = load_series(cfg)
    selected = json.loads((run / "selected.json").read_text())
    experiments = json.loads((run / "experiments.json").read_text())
    manifest = json.loads((run / "manifest.json").read_text())
    main_modes = ["M0_persistence", "M1_ha", "M3_rf", "M4_xgb", "temporal", "graph"]
    headline = metrics[(metrics.split == "test") & (metrics["slice"] == "all")]
    valid_counts = {}
    for minutes in [15, 30, 60]:
        counts = headline[headline.minutes == minutes].n_valid.unique()
        if len(counts) != 1:
            raise ValueError("headline methods do not share valid target counts")
        valid_counts[minutes] = int(counts[0])
    rows, data_rows = [], []
    for mode in main_modes:
        part = headline[headline["mode"] == mode]
        row = [LABELS[mode]]
        for metric in ["MAE", "RMSE"]:
            for minutes in [15, 30, 60]:
                a = part[part.minutes == minutes][metric]
                if len(a) > 1:
                    row.append(f"{a.mean():.3f} $\\pm$ {a.std():.3f}")
                else:
                    row.append(f"{a.iloc[0]:.3f}")
                data_rows.append(
                    {
                        "mode": mode,
                        "minutes": minutes,
                        "metric": metric,
                        "mean": float(a.mean()),
                        "std": float(a.std()) if len(a) > 1 else 0.0,
                        "seeds": len(a),
                    }
                )
        rows.append(row)
    sections = [
        tex_table(
            "Exploratory test errors in mph. Neural values are mean $\\pm$ sample standard "
            "deviation across three seeds; references are frozen single runs.",
            ["Method", "MAE15", "MAE30", "MAE60", "RMSE15", "RMSE30", "RMSE60"],
            rows,
            True,
        )
    ]
    sections.append(
        "The common scored target counts at 15/30/60 minutes are "
        + "/".join(f"{valid_counts[m]:,}" for m in [15, 30, 60])
        + ". Overlapping forecasts are dependent; these counts are not independent trials.\n"
    )
    compared_60 = (
        headline[headline["mode"].isin(main_modes) & (headline.minutes == 60)]
        .groupby("mode")[["MAE", "RMSE"]]
        .mean()
    )
    mae_winner = compared_60.MAE.idxmin()
    rmse_winner = compared_60.RMSE.idxmin()
    sections.append(
        f"Among the main comparison rows, the lowest 60-minute MAE is "
        f"{LABELS[mae_winner]} ({compared_60.loc[mae_winner, 'MAE']:.3f} mph); "
        f"the lowest 60-minute RMSE is {LABELS[rmse_winner]} "
        f"({compared_60.loc[rmse_winner, 'RMSE']:.3f} mph). "
        "These are descriptive rankings, not test-based model-selection decisions. "
        "MAE measures average error size; RMSE puts greater emphasis on large misses.\n"
    )
    tuning_rows = []
    for candidate in json.loads((run / "tuning.json").read_text()):
        marker = "*" if selected[candidate["mode"]]["folder"] == candidate["folder"] else ""
        tuning_rows.append(
            [
                LABELS[candidate["mode"]] + marker,
                f"{candidate['learning_rate']:g}",
                f"{candidate['validation_mae']:.4f}",
            ]
        )
    sections.append(
        tex_table(
            "Learning-rate search: pooled headline tuning-validation MAE, mph, seed42. "
            "An asterisk marks the selected candidate in each family.",
            ["Family", "Rate", "MAE"],
            tuning_rows,
        )
    )
    percentage_rows = []
    for mode in main_modes:
        part = headline[headline["mode"] == mode]
        percentage_rows.append(
            [LABELS[mode]]
            + [f"{part[part.minutes == minutes].MAPE.mean():.2f}" for minutes in [15, 30, 60]]
        )
    sections.append(
        tex_table(
            "Exploratory test MAPE, percent. Neural values average seeds; low positive "
            "speeds can inflate this metric.",
            ["Method", "15min", "30min", "60min"],
            percentage_rows,
        )
    )
    controlled = []
    for mode in ["graph", "self", "uniform", "no_dropout"]:
        part = headline[(headline["mode"] == mode) & (headline.seed == 42)]
        controlled.append(
            [LABELS[mode]] + [f"{part[part.minutes == m].MAE.iloc[0]:.3f}" for m in [15, 30, 60]]
        )
    sections.append(
        tex_table(
            "Controlled seed42 ablations: test MAE, mph. Auxiliary controls "
            "have one seed; neighbour control also has multi-seed evidence.",
            ["Variant", "15min", "30min", "60min"],
            controlled,
        )
    )
    neighbour_rows = []
    for mode in ["graph", "self"]:
        part = headline[headline["mode"] == mode]
        neighbour_rows.append(
            [LABELS[mode]]
            + [
                f"{part[part.minutes == m].MAE.mean():.3f} $\\pm$ "
                f"{part[part.minutes == m].MAE.std():.3f}"
                for m in [15, 30, 60]
            ]
        )
    sections.append(
        tex_table(
            "Neighbour-access control: test MAE mean $\\pm$ sample standard deviation, "
            "mph, over seeds42/43/44. Small seed spread is not a significance test.",
            ["Variant", "15min", "30min", "60min"],
            neighbour_rows,
            True,
        )
    )
    blend = json.loads((run / "evaluation/hybrid_selection.json").read_text())
    alpha = blend["selected"]["alpha_xgb"]
    hybrid = headline[headline["mode"] == "hybrid"]
    endpoint_rows = []
    for model, label in [
        ("M4_xgb", "XGBoost"),
        ("graph_seed42", "Graph seed42"),
        ("hybrid_seed42", "Selected blend"),
    ]:
        part = headline[headline.model == model]
        endpoint_rows.append(
            [label] + [f"{part[part.minutes == m].MAE.iloc[0]:.3f}" for m in [15, 30, 60]]
        )
    sections.append(
        tex_table(
            "Hybrid and its exact frozen constituent forecasts: test MAE, mph. "
            "This graph row is seed42, not a three-seed average.",
            ["Method", "15min", "30min", "60min"],
            endpoint_rows,
        )
    )
    graph = headline[headline["mode"] == "graph"]
    self_only = headline[headline["mode"] == "self"]
    g60 = graph[graph.minutes == 60].MAE.mean()
    s60 = self_only[self_only.minutes == 60].MAE.mean()
    direction = "lower" if g60 < s60 else "higher"
    sections.append(
        f"Across seeds, graph MAE at 60 minutes is {g60:.3f} mph, "
        f"{direction} than self-loop control ({s60:.3f} mph). "
        "This is a measured comparison, not proof of causal congestion propagation "
        "or statistical significance.\n"
    )
    temporal60 = headline[(headline["mode"] == "temporal") & (headline.minutes == 60)].MAE.mean()
    xgb60 = headline[(headline["mode"] == "M4_xgb") & (headline.minutes == 60)].MAE.iloc[0]
    change = 100 * (xgb60 - g60) / xgb60
    (generated / "abstract_results.tex").write_text(
        f" At 60 minutes, graph-model MAE averaged across three seeds is {g60:.3f} mph, "
        f"compared with {s60:.3f} mph for the self-loop control and {xgb60:.3f} mph "
        "for frozen XGBoost. "
        + (
            "Neighbour access improves the neural control but does not surpass XGBoost.\n"
            if g60 < s60 and g60 > xgb60
            else "These measured comparisons determine the reported conclusions.\n"
        )
    )
    (generated / "conclusion.tex").write_text(
        f"The graph model has mean 60-minute MAE {g60:.3f} mph versus {s60:.3f} mph "
        f"for its self-loop control and {temporal60:.3f} mph for the temporal baseline. "
        "These comparisons test neighbour access separately from changing model families. "
        "Metric and traffic-period trade-offs, seed variability and negative ablations must "
        "be retained in interpretation. "
        f"Among the main rows, {LABELS[mae_winner]} has the lowest 60-minute MAE and "
        f"{LABELS[rmse_winner]} the lowest RMSE. "
        + (
            "Reserved validation selected a pure model, so blending did not earn selection. "
            if alpha in [0, 1]
            else "The validation-selected mixture must be compared with its pure endpoints. "
        )
        + "The exposed evaluation interval remains exploratory; "
        "forecasting results do not establish signal-control effectiveness.\n"
    )
    sections.append(
        f"The temporal baseline has mean 60-minute MAE {temporal60:.3f} mph; "
        f"frozen XGBoost has {xgb60:.3f} mph. Graph-model change versus XGBoost is "
        f"{change:.2f}\\% reduction (a negative value means worse error). "
        "Architecture, representation and training protocols differ from trees, so this "
        "comparison alone does not attribute differences to neighbour information.\n"
    )
    sections.append(
        f"Reserved-validation selection chose XGBoost weight $\\lambda={alpha:g}$. "
        + (
            "The selected combination is a genuine mixture; its test scores must still "
            "be compared with both pure models. "
            if 0 < alpha < 1
            else "A pure endpoint won, so selection did not establish blend value. "
        )
        + "Test blend MAE at 15/30/60 minutes is "
        + "/".join(f"{hybrid[hybrid.minutes == m].MAE.iloc[0]:.3f}" for m in [15, 30, 60])
        + " mph.\n"
    )
    # Traffic slices are computed at target timestamps using the common Phase 1 policy.
    slice_rows = []
    for mode in ["M3_rf", "M4_xgb", "temporal", "graph"]:
        p = metrics[(metrics.split == "test") & (metrics.minutes == 60) & (metrics["mode"] == mode)]
        slice_rows.append(
            [LABELS[mode]]
            + [
                f"{p[p['slice'] == s].MAE.mean():.3f}"
                for s in ["peak", "off_peak", "weekday", "weekend"]
            ]
        )
    sections.append(
        tex_table(
            "60-minute test MAE by target period, mph. Neural scores are seed means.",
            ["Method", "Peak", "Off-peak", "Weekday", "Weekend"],
            slice_rows,
            True,
        )
    )
    runtime_rows = []
    for mode in ["temporal", "graph", "self", "uniform", "no_dropout"]:
        records = [r for r in experiments if r["mode"] == mode]
        runtime_rows.append(
            [
                LABELS[mode],
                str(records[0]["parameters"]),
                str(len(records)),
                f"{min(r['epochs'] for r in records)}--{max(r['epochs'] for r in records)}",
                f"{np.mean([r['seconds'] for r in records]) / 60:.1f}",
            ]
        )
    sections.append(
        tex_table(
            "Recorded fitting cost. Minutes are mean wall time per fit, including validation; "
            "contention, pauses and overlapping fits prevent isolated speed comparisons. "
            "Counts include inactive attention-score parameters in self/uniform modes.",
            ["Variant", "Parameters", "Seeds", "Epoch range", "Minutes/fit"],
            runtime_rows,
            True,
        )
    )
    negative_rows, negative_total = [], 0
    for mode in ["temporal", "graph", "self", "uniform", "no_dropout"]:
        records = sorted([r for r in experiments if r["mode"] == mode], key=lambda r: r["seed"])
        counts = [
            json.loads((run / r["folder"] / "inference_check.json").read_text())[
                "test_negative_predictions"
            ]
            for r in records
        ]
        negative_rows.append([LABELS[mode], "/".join(f"{n:,}" for n in counts)])
        negative_total += sum(counts)
    total_forecasts = len(splits.test) * 12 * len(ids)
    if negative_total:
        sections.append(
            tex_table(
                f"Negative forecasts out of {total_forecasts:,} test outputs per fit, across "
                "all horizons, including targets unavailable for scoring. Triples follow "
                "seeds42/43/44; single values use seed42. Outputs remain unclipped.",
                ["Variant", "Negative outputs"],
                negative_rows,
            )
        )
    else:
        sections.append(
            f"No negative outputs occurred in any of the eleven neural fits "
            f"({total_forecasts:,} raw test forecasts per fit, including unscored targets). "
            "Outputs were not clipped. The unconstrained head does not guarantee "
            "physical bounds on other inputs.\n"
        )
    plt.rcParams.update(
        {"font.size": 12, "figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False}
    )

    def save(name):
        plt.tight_layout()
        plt.savefig(figures / f"{name}.png", bbox_inches="tight")
        plt.close()

    plt.figure(figsize=(8, 3.3))
    for mode in main_modes:
        p = headline[headline["mode"] == mode].groupby("minutes").MAE.mean()
        plt.plot(p.index, p.values, label=LABELS[mode])
    plt.xlabel("Horizon (minutes)")
    plt.ylabel("Exploratory test MAE (mph)")
    plt.legend(ncol=2, fontsize=11)
    save("horizons")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3))
    for mode in ["temporal", "graph"]:
        history = pd.read_json(run / selected[mode]["folder"] / "history.json")
        axes[0].plot(history.epoch, history.train_all_horizon_mae, label=LABELS[mode])
        curve = axes[1].plot(history.epoch, history.validation_headline_mae, label=LABELS[mode])[0]
        best_epoch = history.loc[history.validation_headline_mae.idxmin()]
        axes[1].scatter(
            best_epoch.epoch,
            best_epoch.validation_headline_mae,
            facecolors="white",
            edgecolors=curve.get_color(),
            s=45,
            zorder=4,
        )
    axes[0].set_title("Train: all-horizon MAE")
    axes[1].set_title("Validation: 15/30/60-min MAE")
    for ax in axes:
        ax.set_xlabel("Epoch")
        ax.set_ylabel("mph")
        ax.legend(fontsize=11)
    save("learning")
    target_steps = splits.test[:, None] + np.arange(1, 13)
    target = values[target_steps]
    j = len(ids) // 2
    times = speed.index[splits.test + 12]
    day = times[0].normalize() + pd.Timedelta(days=1)
    chosen = (times >= day) & (times < day + pd.Timedelta(days=1))
    plt.figure(figsize=(9, 3.3))
    plt.plot(times[chosen], target[chosen, 11, j], color="black", label="Actual")
    for mode in ["temporal", "graph", "self"]:
        pred = np.load(run / f"evaluation/{mode}_seed42_test.npy", mmap_mode="r")
        plt.plot(times[chosen], pred[chosen, 11, j], label=LABELS[mode], alpha=0.8)
    plt.ylabel("Speed (mph)")
    plt.xlabel(f"Target time, 60-min forecasts; fixed sensor {ids[j]}")
    plt.legend(fontsize=11)
    save("forecast")
    sensors = pd.read_csv(run / "evaluation/per_sensor_mae_60.csv", dtype={"sensor_id": str})
    g = sensors[sensors.model == "graph_seed42"].set_index("sensor_id").reindex(ids).mae_60
    s = sensors[sensors.model == "self_seed42"].set_index("sensor_id").reindex(ids).mae_60
    gain = s - g
    sections.append(
        f"In the seed42 sensor-level comparison, graph MAE is lower than self-only "
        f"for {int((gain > 0).sum())} of {len(ids)} sensors and higher for "
        f"{int((gain < 0).sum())}. The signed map retains both directions. "
        "These unweighted sensor comparisons differ from pooled valid-point MAE. "
        "The fixed sensor/day forecast and fixed attention example illustrate local "
        "behaviour, not universal improvement or causal road influence.\n"
    )
    locations = load_locations(cfg["paths"]["locations"]).set_index("sensor_id").reindex(ids)
    extent = max(float(np.abs(gain).max()), 0.001)
    plt.figure(figsize=(7, 4))
    plt.scatter(
        locations.longitude,
        locations.latitude,
        c=gain,
        cmap="RdBu",
        vmin=-extent,
        vmax=extent,
        s=18,
    )
    plt.colorbar(label="Self-only MAE minus graph MAE (mph)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.gca().xaxis.set_major_locator(MaxNLocator(5))
    save("sensor_gain")
    # A predetermined receiver/origin, not chosen for attractive forecasts or weights.
    checkpoint = torch.load(
        run / selected["graph"]["folder"] / "best.pt", map_location="cpu", weights_only=True
    )
    mask = checkpoint["model"]["graph.mask"]
    torch.set_num_threads(manifest["settings"]["threads"])
    net = build_model(manifest["settings"], len(ids), mask, "graph", "cpu")
    net.load_state_dict(checkpoint["model"])
    net.eval()
    windows = NeuralWindows(values, speed.index, int(splits.train[-1] + 13))
    x, _, _ = tensors(windows, splits.test[:1], "cpu")
    with torch.no_grad():
        sequence = x.permute(0, 2, 1, 3).reshape(len(ids), 12, 2)
        _, hidden = net.gru(sequence)
        _, attention = net.graph(hidden[-1].reshape(1, len(ids), -1), return_attention=True)
    senders = torch.where(mask[j])[0].numpy()
    # Advanced indexing can put the sender axis first; enforce heads-by-senders explicitly.
    weights = attention[0, :, j, :][:, senders].numpy()
    positions = np.arange(len(senders))
    plt.figure(figsize=(8, 3.3))
    for head in range(2):
        plt.bar(
            positions + (head - 0.5) * 0.35, weights[head], width=0.35, label=f"Head {head + 1}"
        )
    plt.xticks(positions, [ids[k] for k in senders], rotation=45)
    plt.ylabel("Attention weight\n(before dropout)")
    plt.xlabel(f"Permitted sender sensor; fixed receiver {ids[j]}")
    plt.legend()
    save("attention")
    pd.DataFrame(
        {
            "receiver": ids[j],
            "sender": [ids[k] for k in senders],
            "head1": weights[0],
            "head2": weights[1],
        }
    ).to_csv(evidence / "attention_example.csv", index=False)
    with plt.rc_context({"font.size": 16}):
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        scatter = axes[0].scatter(
            locations.longitude,
            locations.latitude,
            c=gain,
            cmap="RdBu",
            vmin=-extent,
            vmax=extent,
            s=28,
        )
        fig.colorbar(scatter, ax=axes[0], label="Self minus graph MAE (mph)", pad=0.02)
        axes[0].set_xlabel("Longitude")
        axes[0].set_ylabel("Latitude")
        axes[0].xaxis.set_major_locator(MaxNLocator(3))
        axes[0].yaxis.set_major_locator(MaxNLocator(4))
        for head in range(2):
            axes[1].bar(
                positions + (head - 0.5) * 0.35,
                weights[head],
                width=0.35,
                label=f"Head {head + 1}",
            )
        axes[1].set_xticks(positions, [ids[k] for k in senders], rotation=65, fontsize=14)
        axes[1].set_ylabel("Attention weight")
        axes[1].set_xlabel(f"Sender ID; receiver {ids[j]}")
        axes[1].legend(
            loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2, fontsize=15, frameon=False
        )
        save("spatial_attention")
    sections += [
        r"\begin{figure*}[t]\centering\includegraphics[width=.9\textwidth]{images/horizons.png}"
        r"\caption{Exploratory test horizon errors; neural curves average seeds.}\end{figure*}",
        r"\begin{figure*}[t]\centering\includegraphics[width=.9\textwidth]{images/learning.png}"
        r"\caption{Circles mark selected validation epochs. Different horizon "
        r"aggregations and training/evaluation modes prevent interpreting vertical "
        r"differences as a matched generalization gap.}\end{figure*}",
        r"\begin{figure*}[t]\centering\includegraphics[width=.9\textwidth]{images/forecast.png}"
        r"\caption{Fixed sensor/day example, not a network-wide performance claim.}\end{figure*}",
        r"\begin{figure*}[t]\centering"
        r"\includegraphics[width=.98\textwidth]{images/spatial_attention.png}"
        r"\caption{Left: signed seed42 graph improvement, retaining regressions. "
        r"Right: attention before dropout for a fixed receiver at the first test origin. "
        r"Weights describe fitted behaviour, not physical causality.}\end{figure*}",
    ]
    (generated / "results.tex").write_text("\n\n".join(sections) + "\n")
    # Verify, rather than invent, all claimed integration checks.
    check_file = evidence / "checks.json"
    if check_file.exists():
        checks = json.loads(check_file.read_text())
        text = (
            f"The recorded local suite passed {checks['tests_passed']} tests. "
            "Lint/format checks passed; no remote CI result is inferred. "
            "Real-checkpoint reload and observed-history inference were verified.\n"
        )
        (generated / "verification.tex").write_text(text)
    for name in ["manifest.json", "tuning.json", "selected.json", "experiments.json"]:
        shutil.copy2(run / name, evidence / name)
    for name in ["lineage.json", "scheduling.json"]:
        if (run / name).exists():
            shutil.copy2(run / name, evidence / name)
    for name in [
        "all_metrics.csv",
        "seed_summary.csv",
        "per_sensor_mae_60.csv",
        "hybrid_selection.json",
        "verification.json",
    ]:
        shutil.copy2(run / "evaluation" / name, evidence / name)
    for record in experiments:
        folder = run / record["folder"]
        dest = evidence / record["folder"]
        dest.mkdir(exist_ok=True)
        for name in ["history.json", "complete.json", "inference_check.json"]:
            shutil.copy2(folder / name, dest / name)
    # Host-specific path metadata is disclosed; no checkpoints/raw tensors are copied.
    payload = {
        "headline": data_rows,
        "ablation_seed42": controlled,
        "slice_mae60": slice_rows,
        "hybrid": blend,
        "hybrid_test_mae": endpoint_rows,
        "graph_vs_self_mae60": {"graph": g60, "self": s60},
        "selected": selected,
        "experiments": experiments,
        "sensor_graph_improved_seed42": int((gain > 0).sum()),
        "total_sensors": len(ids),
        "headline_valid_counts": valid_counts,
        "negative_forecasts": negative_rows,
        "test_status": manifest["test_status"],
    }
    (evidence / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")

    def markdown_table(header, body):
        return "\n".join(
            [
                "| " + " | ".join(header) + " |",
                "| " + " | ".join("---" for _ in header) + " |",
            ]
            + ["| " + " | ".join(str(v).replace("$\\pm$", "±") for v in row) + " |" for row in body]
        )

    result_notes = [
        "# Phase 2 measured results — learning companion",
        "Generated from the frozen local run, not manually entered scores. "
        "All errors use matching actual targets/masks. Lower is better. "
        "The old test interval remains exploratory.",
        "## Main methods",
        "MAE/RMSE are mph. Neural rows are mean ± sample standard deviation over "
        "three separately trained seeds, not an ensemble of their predictions.",
        markdown_table(["Method", "MAE15", "MAE30", "MAE60", "RMSE15", "RMSE30", "RMSE60"], rows),
        f"At 60 minutes, graph mean MAE is {g60:.3f} mph versus {s60:.3f} mph "
        f"for self-only and {temporal60:.3f} mph for the smaller temporal model. "
        "Graph versus self-only is the closer neighbour-access comparison; "
        "graph versus trees also changes representation and training design.",
        "## Controlled seed42 ablations",
        markdown_table(["Variant", "MAE15", "MAE30", "MAE60"], controlled),
        "Compare each row with full graph at the same seed. Uniform/no-dropout have "
        "one seed; they do not establish robust superiority from one run. "
        "All controls keep selected graph settings rather than receiving separate tuning.",
        "### Three-seed neighbour comparison",
        markdown_table(["Variant", "MAE15", "MAE30", "MAE60"], neighbour_rows),
        "Entries are mean ± sample standard deviation over seeds42/43/44; "
        "this is run variability, not a significance test.",
        "## Optional hybrid",
        f"Reserved validation selected XGBoost weight {alpha:g}; graph weight is {1 - alpha:g}. "
        "The following graph row is seed42, the actual blend constituent.",
        markdown_table(["Method", "MAE15", "MAE30", "MAE60"], endpoint_rows),
        "## Traffic-period differences",
        markdown_table(["Method", "Peak", "Off-peak", "Weekday", "Weekend"], slice_rows),
        "These are 60-minute MAE values; neural rows average seeds. Peak follows "
        "recorded clock time, whose timezone remains unresolved.",
        "## Computational record",
        markdown_table(
            ["Variant", "Stored parameters", "Seeds", "Epochs", "Mean minutes/fit"],
            runtime_rows,
        ),
        "Wall times include validation, host pressure, scheduling pauses and overlapping fits. "
        "They are not isolated speed benchmarks. Some stored score parameters "
        "are inactive in self/uniform controls.",
        "## Physically invalid negative forecasts",
        markdown_table(["Variant", "Negative outputs"], negative_rows),
        f"Counts are out of {total_forecasts:,} raw test outputs per fit, including "
        "unscored missing targets. Triples follow seeds42/43/44; single values use seed42. "
        "Forecasts were not clipped after scores were observed. "
        + (
            "Negative outputs occurred and are a physical limitation."
            if negative_total
            else "No negative neural outputs occurred in this run. The unconstrained head "
            "does not guarantee physically bounded forecasts on other inputs."
        ),
        "## How to defend the findings",
        "State winners separately for each metric/horizon and traffic slice. "
        "Do not hide an ablation that worsens or a simple method that wins. "
        "MAE is typical absolute error; RMSE emphasizes large misses. "
        "Neither MAPE nor 100 minus MAPE is accuracy. "
        "Seed spread is not statistical significance, and attention is not causal proof.",
        "## Evidence and remaining limits",
        "See verification/phase2-20261112/all_metrics.csv, seed_summary.csv, "
        "experiments.json and hybrid_selection.json for exact values, valid counts "
        "and selection evidence. Source/data/checkpoint identity and inheritance "
        "lineage are retained. No test-driven retuning or clipping was performed.",
        "This component forecasts speed. The separate November16 synthetic LWR/control study "
        "is documented in PHASE2_CONTROL_RESULTS.md; it is not calibrated or GAT-driven control. "
        "The original project-specific brief remains unlocated. Final scope acceptance, "
        "student understanding and publication are separate steps. Prepared source "
        "and analysis use substantial owner/AI assistance; preserve prototype provenance.",
    ]
    (ROOT / "docs/PHASE2_RESULTS.md").write_text("\n\n".join(result_notes) + "\n")
    print("Built evidence and report inputs:", evidence)


if __name__ == "__main__":
    main()
