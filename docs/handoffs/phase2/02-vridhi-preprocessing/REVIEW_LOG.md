# Phase 2 integration/review — Vridhi Chaudhary

- Package: 02-vridhi-preprocessing
- Assigned scope: Causal neural preprocessing, environment and neural contract tests
- Prepared package date: 2026-11-16 (not a student-work date)
- Review activity: 2026-11-16, Asia/Kolkata — Codex assisted integration and source review for Vridhi Chaudhary.

The source, experiments and academic materials were prepared under Kavya Katal's coordination with substantial AI assistance, building on the teammate prototype and preserved Phase 1 work. This review records integration of prepared work and the follow-up below. Independent student implementation, understanding and reproduction have not been established.

## Integration

- Existing repository: `DLML_Midsem_Project`. Verified `upstream` as `KatalKavya96/DLML_Midsem_Project` and `origin` as Vridhi's writable fork, `vridhichaudhary/DLML_Midsem_Project`. Fetched `upstream/main` at `84f9610764070b22b665903d0824960da9fab69f`; created `codex/vridhi-phase2-preprocessing` from it. Preserved the previous local branch and unrelated untracked Phase 1 handoff folder.
- `python3 VERIFY_PACKAGE.py` passed in the extracted package: five payload files and SHA-256 values verified. All five paths were absent at preparation baseline `fbb71d1` and at the fetched base. Imported only those paths at the repository root.
- `src/trafficml/data/neural.py` and both requirements files match their prepared bytes. In `tests/test_neural.py`, scoped PyTorch and model imports to the tests that need them. This lets the preprocessing tests run independently and fixes the original Ruff import ordering failure. The test assertions and model cases are unchanged. Completed this review log.
- Source commit: `23ffef1`. Environment and contract tests: `e57fa73`. The review log is recorded separately. The [GitHub comparison](https://github.com/KatalKavya96/DLML_Midsem_Project/compare/main...vridhichaudhary:DLML_Midsem_Project:codex/vridhi-phase2-preprocessing?expand=1) tracks the personal branch against canonical main.

## What the preprocessing does

`NeuralWindows` takes a time-by-sensor speed array, a matching datetime index and the exclusive training endpoint. Upstream preparation handles the benchmark's zero-as-missing convention; the window code treats nonfinite speeds as missing. It uses finite training speeds to compute a global mean and scale and per-sensor medians. The default input is the last 12 observed five-minute slots through the forecast origin. It fills gaps only from earlier values within that window, uses the sensor's training median for leading gaps (global training mean if the sensor has no training readings), and preserves the original missing flag next to each normalized speed. The origin contributes five calendar values: sine and cosine of time of day and time of week, plus a weekend flag.

The batch returns those inputs and the next 12 normalized target slots. Missing targets stay missing for the model's masked loss. For example, with training mean 30, scale 10 and sensor median 30, a history of [missing, 45, missing] becomes normalized speeds [0, 1.5, 1.5] with flags [1, 0, 1]; a missing future target remains NaN. The agent checked this trace on a synthetic window. The caller must align the input timestamps and sensor order, choose the training endpoint, enforce chronological partitions and match target timestamps and masks for model comparisons. The preprocessing class does not enforce those partition guarantees.

## Fresh checks and remaining work

Used an isolated Python 3.12.9 uv environment outside the checkout. In the commands below, `$PHASE2_ENV` denotes that environment.

- `uv pip install --python "$PHASE2_ENV/bin/python" -r requirements-phase2-lock.txt` resolved and installed the pinned environment (using the identical extracted lock). `uv pip check --python "$PHASE2_ENV/bin/python"` passed for all 59 packages; `uv pip freeze` output matched the lock. `python -m pip check` was not run because this uv environment has no pip module.
- `"$PHASE2_ENV/bin/ruff" check --no-cache src/trafficml/data/neural.py tests/test_neural.py`: prepared tests initially failed I001; passed after the import change.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src "$PHASE2_ENV/bin/python" -m pytest -q -ra -p no:cacheprovider tests/test_neural.py`: initially failed during collection on `trafficml.models.neural`. After the test change, 4 preprocessing tests passed and 9 dependent tests failed on imports (8 missing package 04's model module; 1 missing package 05's `scripts/predict_phase2.py`). No dependent test reached its model assertions.
- Git staged diff and whitespace checks passed. No other package's files were imported. The coordinator still needs to rerun the neural contracts and combined verification with packages 04 and 05 assembled. No real-data or saved-checkpoint reproduction was attempted; the raw speed file was absent and the delivery does not contain checkpoints. The historical 76-test record is separate from this run.

The exposed test interval makes the recorded forecasting results exploratory; matched neural controls improve with GAT, frozen XGBoost has lower MAE, and the selected blend is pure XGBoost. LWR/control remains a separate synthetic experiment with two local rule-based signal agents and no calibrated LA, MARL or GAT control claim. No model was retrained and no scores, predictions or historical manifests were edited. Individual explanation/reproduction, combined verification and faculty acceptance remain pending.
