# Traffic speed forecasting — Team T072

## Phase 2 submission artifacts — organized 2026-11-18

Two separate studies are implemented and verified locally:

1. **Real-data forecasting:** shared GRU, GRU+GAT, self/uniform/dropout controls, three-seed comparisons, validation-only optional blend and observed-history inference on METR-LA.
2. **Synthetic LWR/control:** an eight-cell conservative CTM corridor, two decentralized rule-based signal agents, a fixed-time baseline and 40 matched runs across four scenarios/five paired seeds.

The simulation is not calibrated from METR-LA, not MARL and not GAT-driven control. The studies do not demonstrate real-world signal benefits. The original faculty technical brief remains unlocated; the [requirements audit](docs/PHASE2_REQUIREMENTS_FINAL_AUDIT.md) distinguishes verified requirements from this conservative completion choice.

- [Current Phase 2 report — nine pages](report/phase2/Phase2_Report.pdf), [LaTeX source](report/phase2/source/main.tex), [14-slide PowerPoint](slides/phase2/Phase2_Presentation.pptx) and [viewable presentation PDF](slides/phase2/Phase2_Presentation.pdf)
- [Reports by phase](report/README.md), [presentations by phase](slides/README.md) and [review / preservation notes](docs/DELIVERABLES_REVIEW_20261118.md)
- [Forecast results](docs/PHASE2_RESULTS.md), [synthetic control results](docs/PHASE2_CONTROL_RESULTS.md) and [final verification](verification/phase2-final-20261116/README.md)
- [Simple forecasting notes](docs/PHASE2_LEARNING_NOTES.md), [LWR/agent notes](docs/PHASE2_CONTROL_NOTES.md), [speaking/viva guide](docs/PHASE2_PRESENTATION_GUIDE.md) and [runbook](docs/PHASE2_RUNBOOK.md)
- [Forecast protocol](docs/PHASE2_PROTOCOL.md), [control protocol](docs/PHASE2_CONTROL_PROTOCOL.md) and [literature](docs/PHASE2_LITERATURE.md)

Forecast results are unchanged: 60-minute MAE is 4.881 mph for graph GRU versus 4.931 for self-only (three-seed means), and 3.874 for frozen XGBoost. Trees remain stronger; RF has the best main-method RMSE. Blend validation selected pure XGBoost. These are exploratory errors on a previously exposed interval, not accuracy.

In the separate synthetic experiment, responsive signals lower total system vehicle-time against the chosen equal-green baseline in all four scenarios. That baseline is not demand-optimized; results do not establish optimality, calibrated city delay savings or neural-control gains. Boundary waiting and end-of-horizon residuals are separately reported.

Local checks: **76 tests passed with real data available and no skips**, Ruff lint/format and integration checks are recorded in the dated verification files, rebuilt wheel imports neural/control modules outside the checkout, saved-model CSV inference works, and all synthetic runs pass per-step conservation/bounds/flow checks. Prior forecasting checkpoints/scores and original Phase 1 source/data are unchanged. Report pages and exact-final-file slides were rendered/inspected; both artifacts are below 10 MB. Native PowerPoint opening and remote CI are not claimed.

PRs #9–#14 are merged into canonical main, including the coordinated Phase 2 implementation and Rudraksh’s latest report/deck. The owner approved publishing the reviewed November 18 file organization and PPT compatibility repair on the kavya branch. Their completed review logs and neural test corrections are preserved. Kavya’s remaining evaluation/inference, CI, evidence and shared docs are integrated locally on `kavya`; see [fresh combined verification](verification/phase2-integration-20261117/README.md). No push, PR, merge or form submission was performed. Five local Phase 2 member handoffs and their common prompt are documented in [the handoff guide](docs/handoffs/phase2/README.md). Owner/faculty-scope review, genuine individual understanding/rehearsal and later handoffs/publication remain owner-managed. Prepared source/analysis preserves substantial AI-assistance and teammate-prototype provenance.

## Preserved Phase 1 study

> Integration status: member PRs #2–#6 are merged into `main`. The owner-authorized `kavya` branch adds the selected report and presentation for review. No direct-main commit or push is used. See [current state](PROJECT_STATE.md).

Canonical repository: `KatalKavya96/DLML_Midsem_Project`. The implementation lives directly at this repository root (`src/trafficml`, `scripts`, `tests`, `configs`). There is no nested `AML/` project. Delivery ZIPs, old scaffolding and private build files were moved to the separate sibling `DLML_Project_Archive_2026-10-27` folder. Read [current state](PROJECT_STATE.md), [team roster](PROJECT.md) and [handoff instructions](docs/handoffs/HANDOFF.md).

A local, end-to-end Phase 1 forecasting study using **Persistence, Historical Average, Random Forest and XGBoost** on the existing METR-LA files. Those frozen runs contain no neural networks, graph-neighbour features, UI or traffic-signal controller. The newer Phase 2 extension is described above. Do not present forecasting results as traffic-control benefits.

Read [the methods/viva guide](docs/METHODS_AND_VIVA.md), [literature synthesis](docs/LITERATURE.md), and [contribution disclosure](docs/CONTRIBUTIONS.md). The integrated implementation was prepared with substantial AI assistance; names/commits are not evidence of individual implementation.

## Preserved Phase 1 report and presentation

- [Report PDF](report/phase1/Phase1_Report.pdf)
- [PowerPoint](slides/phase1/Phase1_Presentation.pptx)
- [Presentation PDF](slides/phase1/Phase1_Presentation.pdf)

These are the owner's supplied files, preserved unchanged. **The presentation's RMSE columns and pilot-candidate labels need correction against the saved evidence.** See [import checks, correct values and provenance](docs/final_deliverables.md). Existing sources and generated experiment evidence are preserved.

## Setup

Use a fresh Python **3.12** environment (tested with 3.12.14). On macOS, XGBoost requires the OpenMP runtime:

```bash
brew install libomp
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m pip check
```

Homebrew is a macOS-only prerequisite; Linux uses the platform OpenMP runtime, typically libgomp. Do not copy someone else's virtual environment. Direct/transitive Python package versions are pinned. Native dependencies/platform differences still matter; the runtime manifest records the measured environment.

## Data

Place the existing files here (not distributed in the source package):

```text
data/raw/metr-la.h5
data/raw/sensor_graph/adj_mx.pkl
data/raw/sensor_graph/distances_la_2012.csv
data/raw/sensor_graph/graph_sensor_ids.txt
data/raw/sensor_graph/graph_sensor_locations.csv
```

Source: [DCRNN](https://github.com/liyaguang/DCRNN). The original download helper is retained but was not executed during this work; it separately requires gdown and also downloads PEMS-BAY. Prefer verified local files and compare checksums with the run manifest. Upstream code is MIT; separate raw-data redistribution rights remain unresolved, so no datasets are bundled. No additional flow/occupancy channels are invented.

## Check

```bash
pytest -q -ra
ruff check .
ruff format --check .
python scripts/check_data.py
```

Two real-data tests skip if datasets are missing; a skip is not a passed integration check. Other tests cover causal features, masks, split purging, artifacts, model label rules and saved-model reuse.

## Run the full pipeline

```bash
python scripts/run_all.py --run-dir results/runs/my-phase1-run
```

This trains/tunes the models, evaluates tuning/second-validation/test partitions, generates data/error figures and writes report result tables. Use a **fresh directory per run**. The second validation interval is reported separately; no hybrid stacker is trained. The default training stride is 2 to bound compute. Full evaluation includes all sensors/anchors. A development check can use `--max-sensors 2`; it must never be described as a 207-sensor result.

The two learned methods share 38 causal features. A small, predeclared search uses only val_tune and six evenly spaced pilot sensors. Parameters freeze before full comparisons. Test data were inspected in the earlier prototype; test results are exploratory, not an untouched final holdout. Do not tune against the test tables or promise a particular error/accuracy.

Outputs within the run:

- `manifest.json`: source/data/config hashes, environment, exact command, partitions, feature names and selected parameters.
- `tuning.json`: every budgeted candidate and its pilot validation score.
- `models/`, `preprocessing.joblib`: locally fitted estimators/transforms for later prediction; load only trusted local artifacts.
- `preds/`: immutable targets and aligned predictions for all methods/partitions.
- `tables/`, `leaderboard_*.csv`: MAE/RMSE/MAPE, valid counts and exploratory significance results.
- `training_records.json`, `timing.json`: actual valid training counts, fallback horizons and timings.
- `analysis/`: EDA, horizon/period comparisons, sensor errors and a fixed-index forecast example.

Evaluation rejects stale source/config/data or misaligned artifacts. Changing runtime code requires a new run; do not mix an old result file with a new code snapshot. Full twelve-horizon tensors are retained, with 15/30/60 minutes highlighted. A three-column tensor cannot silently replace them.

## Make a forecast without retraining

Choose a sensor ID from the run manifest, for example the first listed ID:

```bash
python scripts/predict.py --run-dir results/runs/my-phase1-run --sensor 773869 --at latest
```

This prints forecasts 15, 30 and 60 minutes after the dataset's last observation. It is a historical-data demonstration, not live traffic service. Use `--at '2012-06-05 08:00:00'` for another observed origin with adequate history. Earlier origins inside the training interval are in-sample demonstrations, not held-out results. For an alternative sensor, use its exact recorded ID.

## Explain and report

`report/phase1/results.md` and `metrics.tex` are generated from actual completed outputs. `report/phase1/source/main.tex` is the IEEE-style report source. Copy the generated metrics table and selected run images into its project directory before recompiling, as documented in `report/phase1/source/README.md`. Presentation material is under `slides/`.

Key limitations: prior test exposure; provisional clock timezone/DST and peak windows; missing-target selection bias in multi-output RF; strided training; a small pilot search; a single region/period; low-speed MAPE instability. The graph is verified but not a prediction input. Multi-seed stability, graph learning, calibrated LWR physics and signal simulation remain future work.

## Integrity and ownership

Original teammate code/plan and correction records are retained as history. Report actual contributions and assistance honestly. Team members need to understand the full pipeline for viva; a completed code package cannot certify that understanding. The owner-authorized integration is prepared on branch `kavya`; branch publication and PR review are separate from merging or declaring final acceptance.
