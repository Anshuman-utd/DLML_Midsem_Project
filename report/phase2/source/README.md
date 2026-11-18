# Phase 2 report source — latest write-up, 2026-11-18

Prepared by Rudraksh with Claude Code assistance from frozen project evidence, preserving Kavya coordination and the original team/prototype/assistance attribution. Main source: main.tex; tables: generated/; figures: figures/. These are report build inputs, not extra submission reports.

The current report is ../Phase2_Report.pdf (nine pages). The companion deck is ../../../slides/phase2/Phase2_Presentation.pptx (14 slides) and its browser-friendly PDF is alongside that deck. Original uploaded deck and the earlier coordinator report/deck are preserved in the phase-specific archive directories. The deck received chart-axis/cache-serialization compatibility repairs; text, notes, layouts and scientific values are unchanged.

From repository root:

```bash
PYTHONPATH=src python scripts/run_control.py --run-dir results/runs/control-report
python report/phase2/source/make_assets.py --control-run results/runs/control-report
cd report/phase2/source
tectonic -X compile main.tex --outdir /tmp/t072-report-build
```

Compile in a private output directory and review before replacing the canonical PDF. Nothing here retrains models; input scores come from verification/phase2-20261112/ and verification/phase2-final-20261116/control/. Sensor-map and density regeneration need ignored locations/trajectory files. Graph forecasts and synthetic control remain separate; no hybrid gain, calibrated LA, MARL or GAT-driven control is claimed. Citations do not prove student understanding.
