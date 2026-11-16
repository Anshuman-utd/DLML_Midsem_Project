# Phase 2 integration/review — Anshuman Mehta

- Package: 03-anshuman-artifacts
- Assigned review scope: Literature, actual-result plots, report, presentation and learning materials
- Prepared package date: 2026-11-16 (not a student-work date)
- Status: **integrated and agent-reviewed on 2026-11-17; member understanding and reproduction pending**

The source, experiments and academic materials were prepared under Kavya Katal's coordination with substantial AI assistance, building on the teammate prototype and preserved Phase 1 work. This log records integration and review of that prepared work. It records no completed independent student implementation or understanding.

## Agent integration and review (2026-11-17, Asia/Kolkata)

Performed by an Antigravity agent run for Anshuman Mehta under the configured Git identity `Anshuman-utd <anshumanmehta11@gmail.com>`. Everything in this section reflects what the agent executed and verified. It is not evidence that Anshuman personally reproduced or understands the module.

### Repository, base and branch

- Local clone: canonical repository `KatalKavya96/DLML_Midsem_Project` configured as `upstream`; personal fork `Anshuman-utd/DLML_Midsem_Project` configured as `origin`. Publication pushes to the personal fork branch and targets `upstream:main`.
- Base: fetched latest canonical `upstream/main` at `6fcde57` (2026-11-16/17), which includes merged PR #9 (Rudraksh's synthetic control) and PR #10 (Vridhi's causal neural preprocessing). This advances from the package's preparation baseline `fbb71d1`.
- Branch: created `codex/anshuman-phase2-artifacts` from `upstream/main` (`6fcde57`). Working tree clean before copy; existing unrelated branches preserved.

### Verification and import

- Ran `python3 VERIFY_PACKAGE.py` from `T072_Phase2_03-anshuman-artifacts`: "Verified 24 assigned payload files and all supplied baseline bytes. No repository files modified."
- `BASELINE.json` recorded all 24 paths as additions (`base_sha256: null`). None existed on `upstream/main` or locally.
- Copied only `payload/` contents into the repository root; all 24 files matched `MANIFEST.json` SHA-256 hashes and byte counts.
- Imported unchanged (23 files):
  - `docs/PHASE2_LITERATURE.md`
  - `docs/PHASE2_LEARNING_NOTES.md`
  - `docs/PHASE2_PRESENTATION_GUIDE.md`
  - `scripts/build_phase2_report.py`
  - `scripts/build_control_report.py`
  - `report/phase2/main.tex`
  - `report/phase2/T072_Phase2_Report.pdf`
  - 6 generated LaTeX fragments in `report/phase2/generated/`
  - 9 visual figures in `report/phase2/images/`
  - `slides/phase2/T072_Phase2.pptx`
- Changed (1 file): this review log (`docs/handoffs/phase2/03-anshuman-artifacts/REVIEW_LOG.md`), completed from the prepared template.
- Genuine corrections: none; verified source, data figures, and tables showed no evidence-backed defects.
- Excluded from Git: package directory `T072_Phase2_03-anshuman-artifacts/`, verification script, manifests, delivery metadata, and `repo-context/`.

### What the module does (plain-English explanation)

Purpose: Synthesizes the literature foundation, report generation scripts, LaTeX conference paper, actual-result figures, compiled PDF, presentation slide deck, and comprehensive learning notes for Phase 2.

- `docs/PHASE2_LITERATURE.md`: Registers surveyed literature connecting theoretical foundations to implementation:
  - Cho et al. (2014) for GRU sequence representation and update/reset gates.
  - Veličković et al. (2018) for Graph Attention Networks (GAT) masked neighbourhood aggregation with multi-head attention.
  - Li et al. (2018) DCRNN for spatial-temporal traffic forecasting benchmarks on METR-LA.
  - Richards (1956) and California PATH CTM (2015) for LWR hydrodynamic theory and cell-transmission Godunov discretization.
  - Lioris & Varaiya for max-pressure signal control.
- `scripts/build_phase2_report.py`: Reads actual Phase 2 forecasting run outputs (`evaluation/all_metrics.csv`, `selected.json`, `experiments.json`, `manifest.json`), aggregates multi-seed metrics (mean ± std), formats LaTeX tables (`results.tex`), and generates research figures (`forecast.png`, `horizons.png`, `attention.png`, `sensor_gain.png`, `spatial_attention.png`).
- `scripts/build_control_report.py`: Validates synthetic control run manifests and trajectories, verifies checksums, aggregates 40 matched simulation runs (4 scenarios × 5 seeds × 2 policies), formats LaTeX summary tables (`control_results.tex`), and generates bar plots (`control_comparison.png`) and space-time density diagrams (`control_density.png`, `control_occupancy.png`).
- `report/phase2/main.tex`: 7-page IEEE-format conference paper structured into: Problem & Literature, Data & Preparation, Architecture, Training & Ablations, Measured Forecasting Results, Synthetic LWR Signal Control, and Discussion & Threats to Validity.
- `report/phase2/generated/`: Modular machine-generated LaTeX tables and text fragments (`abstract_results.tex`, `results.tex`, `control_results.tex`, `conclusion.tex`, `verification.tex`, `final_verification.tex`).
- `report/phase2/T072_Phase2_Report.pdf`: Pre-compiled 7-page academic deliverable.
- `slides/phase2/T072_Phase2.pptx`: 6-slide executive presentation covering Problem, Protocol, Architecture, Training/Ablations, Measured Forecasts, and Synthetic Control, with speaking notes allocated across all five team members.
- `docs/PHASE2_LEARNING_NOTES.md` and `docs/PHASE2_PRESENTATION_GUIDE.md`: Deep learning learning materials explaining end-to-end tensor transformations, normalization conventions, GRU gate mechanics, GAT aggregation, loss masking, tuning rules, and honest interpretation of results.

Inputs:
- For report building: run directories containing metrics CSVs, JSON manifests/artifacts, and trajectory `.npz` files.
- For LaTeX document: generated `.tex` fragments and `.png` figures.
Outputs:
- Automated LaTeX tables, comparison charts, 7-page PDF report, 6-slide PPTX, and documentation.
Dependencies:
- Python 3.12, `matplotlib`, `numpy`, `pandas`, `torch`, `PyYAML`, `ruff`.
- Packages 01 (`run_control.py`), 02 (`trafficml.data.neural`), 04 (`run_phase2.py`), 05 (`_common.py`, `predict_phase2.py`).

### Checks run and outcomes

Environment: macOS (Darwin 24.3.0, arm64), CPython 3.12.13 in an isolated uv environment at `/tmp/phase2_env`. Installed pinned packages from `requirements-phase2-lock.txt` (59 packages).

| Command | Outcome | Notes |
|---|---|---|
| `python3 VERIFY_PACKAGE.py` (in package dir) | **Passed** | 24 payload files and baseline bytes verified |
| `uv pip check --python /tmp/phase2_env/bin/python` | **Passed** | 59 installed packages verified compatible |
| `python -m pip check` | **Skipped** | Environment managed by uv without pip module |
| `PYTHONPATH=src /tmp/phase2_env/bin/python scripts/build_control_report.py --help` | **Passed** | Printed usage and options (`--run-dir`) |
| `python scripts/build_phase2_report.py --help` | **Failed** (`ModuleNotFoundError: No module named 'run_phase2'`) | Expected: `scripts/run_phase2.py` belongs to unmerged package 04-bineet-neural |
| `/tmp/phase2_env/bin/ruff check scripts/build_phase2_report.py scripts/build_control_report.py` | **Passed** | All checks passed |
| `/tmp/phase2_env/bin/ruff format --check scripts/build_phase2_report.py scripts/build_control_report.py` | **Passed** | 2 files already formatted |
| `/tmp/phase2_env/bin/ruff check src tests scripts configs` | **Passed** | Clean across entire tracked repository codebase |
| `/tmp/phase2_env/bin/ruff format --check src tests scripts configs` | **Passed** | 47 tracked Python files already formatted |
| LaTeX compilation (`pdflatex` / `latexmk`) | **Skipped** | No LaTeX compiler installed on local system |
| Document inspection: `report/phase2/T072_Phase2_Report.pdf` | **Verified** | 684,851 bytes, 7 pages confirmed via system `mdls` |
| Document inspection: `slides/phase2/T072_Phase2.pptx` | **Verified** | 100,621 bytes, 6 slide XML structures confirmed via Python `zipfile` |
| `PYTHONPATH=src /tmp/phase2_env/bin/pytest -q -ra` | **65 passed, 9 failed, 2 skipped** | 2 skips: raw METR-LA HDF5 data not present. 9 failures: `trafficml.models.neural` (package 04) and `predict_phase2` (package 05) unmerged. 65 passes: 54 Phase 1 tests + 7 synthetic control tests + 4 neural preprocessing tests. |

### Observations and key findings to preserve

1. **Exploratory forecast evaluations**: Because the METR-LA test interval was inspected earlier during Phase 1, Phase 2 test scores are strictly exploratory.
2. **Deep learning vs. Tree baselines**: At 60 minutes, GRU+GAT achieved mean MAE 4.881 mph (across 3 seeds), which improves over the self-loop neural control (4.931 mph) by ~1% (0.050 mph), but does **not** beat frozen XGBoost (3.874 mph) or Random Forest (3.896 mph). On 60-minute RMSE, Random Forest is lowest at 7.255 mph vs 9.619 mph for GRU+GAT. Deep learning did not beat trees on this benchmark.
3. **Hybrid blending outcome**: Grid search on reserved validation selected XGBoost weight $\lambda=1.0$ and neural weight $0.0$. The pure tree endpoint won, meaning blending provided no demonstrated empirical benefit over pure XGBoost.
4. **Synthetic LWR/CTM control scope**: The control study is a separate, synthetic 8-cell simulation comparing two local rule-based agents (fixed time vs queue-responsive) against an unoptimized equal-green baseline. It is not calibrated to METR-LA, does not use GAT forecasts for control, and is not MARL or real-world traffic management.
5. **Cross-package dependencies**: Full report regeneration requires run outputs, trajectories, package 04 (`trafficml.models.neural`, `scripts/run_phase2.py`) and package 05 (`scripts/_common.py`, `scripts/predict_phase2.py`). The coordinator will run final combined verification once all member branches merge.

## Actual activity summary

- Actual date: 2026-11-17 (Asia/Kolkata)
- Reviewer/Agent: Antigravity agent for Anshuman Mehta
- Verified remotes: canonical `upstream`, personal fork `origin`
- Base: `upstream/main` (`6fcde57`), personal branch: `codex/anshuman-phase2-artifacts`
- SHA-256 verification: verified 24 payload files and baseline bytes before copying
- Imported files: 23 files unchanged, 1 review log completed
- Commit IDs:
  - `66e1356`: Integrate prepared literature register and report plot builders
  - `fd42f05`: Integrate prepared Phase 2 IEEE report source, generated tables, figures and PDF
  - Third commit: Integrate presentation, learning guide and record Phase 2 integration review
- PR destination: `KatalKavya96/DLML_Midsem_Project:main`
- Coordinator combined verification / faculty acceptance: **not established by this handoff**.
