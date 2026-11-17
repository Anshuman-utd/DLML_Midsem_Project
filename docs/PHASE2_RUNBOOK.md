# Phase 2: run, reproduce and explain

This extends Phase 1 with shared temporal GRU and GRU+GAT forecasting. Source and experimental protocol are prepared with substantial AI assistance under Kavya Katal's coordination. Prepared code is not evidence that any student independently implemented or understands it. Record genuine subsequent work and review.

## Environment

Python 3.12. Create a fresh environment and install `requirements-phase2-lock.txt` (full measured environment), or `requirements-phase2.txt` (Phase 1 pins plus PyTorch). Follow Phase 1 macOS OpenMP instructions. Do not commit environments, raw data, checkpoints or prediction arrays.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-phase2-lock.txt
python -m pip install --no-deps --no-build-isolation -e .
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 pytest -q -ra
ruff check .
ruff format --check .
```

On macOS, the test thread limits prevent oversubscription when XGBoost and PyTorch share one process. Training explicitly sets its own CPU thread count. CPU was chosen from measured synthetic timing; GPU availability does not imply it is faster for this workload.

## Real-data experiment

Use actual data at configs/data.yaml paths, with the verified 207-sensor graph files. No synthetic data is substituted for forecasting results.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_WAIT_POLICY=PASSIVE KMP_BLOCKTIME=0 \
  PYTHONPATH=src python scripts/run_phase2.py --run-dir results/runs/phase2-v2 --device cpu
PYTHONPATH=src python scripts/evaluate_phase2.py --run-dir results/runs/phase2-v2
PYTHONPATH=src python scripts/build_phase2_report.py --run-dir results/runs/phase2-v2
```

The first command selects two learning-rate candidates per architecture on val_tune, then trains declared seeds/ablations. The second command is run after training choices freeze. It verifies Phase 1 source/target identities, scores every model and selects the optional blend on val_stack only. No model is selected using test performance. Use a fresh run directory after changing source/config/data. An incomplete fit restarts that fit; completed checkpoints are reused only under the original run identity.

The third command regenerates small evidence, measured tables, learning/horizon plots, a fixed forecast example, signed sensor gains, an attention example and docs/PHASE2_RESULTS.md. Compile report/phase2/main.tex with a TeX installation providing IEEEtran (the recorded build used Tectonic). The editable six-slide PPTX is a separate academic artifact. Generated tables/figures must be rebuilt when experiment results change; do not manually change a score to improve the story.

The passive-wait settings reduce CPU contention from auxiliary thread pools; the script still sets four PyTorch computation threads. For a clean reproduction choose a new run directory. The recorded v2 run inherited five completed v1 fits after a bitwise-verified storage-only preprocessing change; its source snapshots, equivalence proof and checkpoint lineage are retained in verification/phase2-20261112/. This is separate from a fresh run with one uniform source identity.

This study fixes history and horizon at 12; other lengths need a separately implemented/verified experiment, not just a YAML edit. For a custom model configuration, keep it inside this repository's configs directory and pass its absolute path with --config. The default command already uses an absolute configuration path.

Phase 1 frozen prediction bundles are required at results/runs/phase1-full-v1 for comparisons/hybrid. They stay local. If unavailable, reproduce Phase 1 in a fresh run and pass `--baseline-dir` to evaluation; do not invent old predictions. Adding Phase 2 files changes the exhaustive working-tree fingerprint used by old Phase 1 CLIs; do not weaken that old protection or overwrite its manifest. Phase 2 evaluation instead checks every historically recorded source file and exact saved targets before reusing bundles.

## Standalone inference

Input CSV: first column naive recorded timestamp, then exact 207 sensor IDs in training order. Supply at least 12 five-minute observed rows. Zero/NaN are missing; future rows are unnecessary. Use an actual completed model folder from selected.json or experiments.json.

```bash
PYTHONPATH=src python scripts/predict_phase2.py \
  --run-dir results/runs/phase2-v2 \
  --model-folder tune_graph_0 \
  --history /path/to/observed_history.csv \
  --output results/runs/manual-phase2-forecast.csv
```

The model-folder above is an example, not a claim that candidate0 won. Check selected.json. Output contains 12 future timestamps and 207 mph forecasts. Do not clip predictions after observing scores; negative counts are reported in evaluation records.

## What to explain

- A GRU learns a compact summary of each sensor's history; reset/update gates control its memory. The same weights are shared across sensors.
- GAT computes learned weights over permitted sender nodes for each receiver. Our mask uses supplied directed connectivity transposed to receiver-by-sender convention. Physical upstream labels are unresolved.
- The prediction head learns corrections to the latest filled speed. This residual design is not the optional ML-DL hybrid; the hybrid combines XGBoost and neural forecasts.
- Five origin-calendar features are identical across neural variants. All neural inputs use training-only scaling and causal fills; missing labels never become fabricated answers.
- Graph versus self-only keeps architecture/settings more comparable than graph versus a different temporal model. Uniform neighbours test learned weighting; zero dropout tests one regularizer. Single-seed ablations have limited robustness.
- MAE measures average absolute error; RMSE emphasizes larger errors; MAPE becomes unstable for small positive speeds. None is classification accuracy.
- A low forecasting error does not prove congestion propagation, control effectiveness, calibrated LWR, individual understanding or faculty acceptance.

## Submission checklist

- Measured results and checkpoints exist; all planned runs passed or failed/skipped work is clearly disclosed.
- Tests, lint, format, source/data fingerprints and checkpoint reload inference checked.
- Comparison tables share targets/masks/horizons; main multi-seed results include variability.
- Ablation/hybrid conclusions match measurements, including unsuccessful experiments.
- Report explains LWR theory, speed-only limits, exposed-test status and actual contributions/assistance.
- Report PDF and PPTX/PDF presentation each <=10 MB, independently opened/inspected.
- Correct canonical GitHub link, no raw data/secrets/models/bundles in staged changes.
- One university-email form submission by Nov19 2026 12:55 IST; no automatic form submission by this workflow.
- Original technical-brief/control scope gap remains explicit until verified; do not certify full title compliance from forecasting alone.

Member ZIP handoffs are a later owner-requested step after integrated verification. Packages must preserve provenance and contain assigned files/instructions; do not create artificial independent authorship or backdated logs.


## Synthetic LWR/two-agent demonstration (added November16)

No METR-LA files or neural checkpoints are needed for this separate component. Settings were recorded before outcomes in configs/control.yaml and docs/PHASE2_CONTROL_PROTOCOL.md. It is a small rule-based simulation, not MARL, calibrated LA traffic or a GAT-driven controller.

```bash
PYTHONPATH=src .venv/bin/python scripts/run_control.py \
  --run-dir results/runs/control-manual-review
MPLCONFIGDIR=/tmp/t072-mpl-cache XDG_CACHE_HOME=/tmp/t072-cache PYTHONPATH=src \
  .venv/bin/python scripts/build_control_report.py \
  --run-dir results/runs/control-manual-review
```

The first command runs40 paired-policy cases from the fixed four-scenario/five-seed design and retains trajectories locally. The second verifies their hashes and updates small control evidence, report inputs and measured tables. Read PHASE2_CONTROL_NOTES.md for units, topology, agents, timing, measures and limitations. Signals use local occupancy; no neural forecasts enter actions. System vehicle-minutes is not mean completed-trip delay. The full local suite now has76 passing tests; the older69-test record is preserved as November13 history.

The final source/report include generated/final_verification.tex from the November16 checks. The actual latest report/PPTX and manifest are listed in verification/phase2-final-20261116/. Source, settings and scores must stay synchronized. Publication/form submission remain owner actions; no push is performed by this workflow.
