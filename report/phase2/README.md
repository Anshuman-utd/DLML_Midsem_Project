# Phase 2 report (IEEE format)

| File | What it is |
| --- | --- |
| `T072_Phase2_Report.pdf` | Final 7-page IEEE conference-format report |
| `main.tex` | LaTeX source (IEEEtran) |
| `make_assets.py` | Builds the tables and figures from the saved results |
| `generated/` | Table bodies and `numbers.json` written by the script |
| `figures/` | Figures written by the script |

The matching 13-slide deck is `slides/phase2/T072_Phase2.pptx`, and the team's viva guide is `docs/PHASE2_VIVA_GUIDE.md`.

## Where the numbers come from

Nothing is trained, tuned or re-scored. `make_assets.py` reads only the saved results in `verification/phase2-20261112/` and `verification/phase2-final-20261116/control/`.

## Rebuild

```bash
python report/phase2/make_assets.py
cd report/phase2 && tectonic -X compile main.tex --outdir . && mv main.pdf T072_Phase2_Report.pdf
```

## History

This report and deck replace the two earlier Phase 2 versions (the coordinator-prepared report and six-slide deck, and the first alternative in `report/phase2_report/`). Both remain in Git history. `scripts/build_phase2_report.py` and `scripts/build_control_report.py` belong to the earlier report: they write `generated/results.tex`, `generated/control_results.tex` and `images/`, which this report does not use.

## Limits

Forecasting scores are exploratory because the test period was inspected in Phase 1. GRU + GAT improves on its neural controls but not on XGBoost, and the selected blend is XGBoost alone. The LWR study is synthetic: not calibrated to Los Angeles, not trained, and not driven by the forecasts. The report was drafted with AI assistance.
