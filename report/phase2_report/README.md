# Phase 2 report (IEEE format) and presentation

Prepared on branch `codex/rudraksh-phase2-report` with AI assistance (Claude Code). It is an alternative write-up of the same frozen Phase 2 evidence; the coordinator-prepared report and deck in `report/phase2/` and `slides/phase2/` are unchanged.

| File | What it is |
| --- | --- |
| `phase2_report.pdf` | Compiled 9-page IEEE conference-format report |
| `main.tex` | LaTeX source (IEEEtran) |
| `make_assets.py` | Builds every table and figure from the evidence files |
| `generated/` | Table bodies and `numbers.json` written by the script |
| `figures/` | Figures written by the script (PDF for the report, PNG for slides) |
| `../../slides/phase2_presentation.pptx` | 14-slide editable deck with speaker notes |

## Where the numbers come from

Nothing was trained, tuned or re-scored. `make_assets.py` reads only:

- `verification/phase2-20261112/` (forecasting metrics, training histories, selection records)
- `verification/phase2-final-20261116/control/` (synthetic control metrics)

Two figures also need local, git-ignored inputs: the sensor map needs `data/raw/sensor_graph/graph_sensor_locations.csv`, and the density figure needs trajectories from a fresh `scripts/run_control.py` run (deterministic; it reproduces the frozen metrics byte for byte).

## Rebuild

```bash
PYTHONPATH=src python scripts/run_control.py --run-dir results/runs/control-report
python report/phase2_report/make_assets.py --control-run results/runs/control-report
cd report/phase2_report && tectonic -X compile main.tex --outdir .
```

## Limits to keep in mind

Forecasting scores are exploratory (the test interval was inspected in Phase 1). GRU+GAT improves on its neural controls but not on XGBoost, and the selected blend is pure XGBoost. The LWR/control study is synthetic: not calibrated to Los Angeles, not MARL and not driven by the forecasts. The 19 references were checked against arXiv, Crossref and the publisher pages on 2026-11-18; that confirms the citations, not that every team member has read each paper.
