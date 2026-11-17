# Phase 2 forecasting evidence — historical November13 verification

The November16 synthetic LWR/two-agent extension and updated final artifacts/checks are in ../phase2-final-20261116/. Forecasting metrics/checkpoints below remain unchanged. The old final-file hashes identify the November13 artifacts, whose copies/source are retained in the private Phase2_Submission/history/pre-control-2026-11-16 archive; they do not identify the later updated final-file paths.


This is the measured owner-authorized forecasting extension, prepared with substantial AI assistance and preserved teammate/Phase 1 provenance. Protocol/configuration were recorded before real neural fitting. No independent member implementation/understanding, faculty acceptance, remote CI, GitHub publication or form submission is claimed.

## Actual completed work

- Thirteen unique completed fits: four learning-rate candidates, with two winners reused; three seeds each for temporal GRU, GRU+GAT and self-only; one seed each for uniform attention and no dropout. Eleven fits were evaluated.
- Every model shares exact targets/masks/horizons. All 31 historical Phase 1 source/config hashes and raw-data identity remain unchanged. Reused baseline bundles reproduce all 720 preserved metric rows.
- 69 tests passed in 2.71 seconds with real data available and no skips; Ruff lint/format passed for 44 files. uv checked 59 compatible installed packages. The rebuilt wheel imports both neural modules outside the checkout.
- All eleven saved checkpoints reproduce predictions exactly after reload. Actual observed-history CSV inference passed documented float32-scale tolerance; it does not need future-label inputs.
- Five-page PDF compiled with the built-in editor and Tectonic 0.15.0, then every page was rendered/visually inspected. Six-slide PPTX passed package/layout/font/native chart/table/import checks, and every slide rendered from the exact finalized PPTX was inspected. Native PowerPoint opening is not claimed.

## Findings

60-minute MAE, mph: temporal GRU 4.929, graph GRU 4.881, self-only 4.931 (three-seed means); XGBoost 3.874 and RF 3.896 (frozen single fits). Graph access modestly helps its neural control but does not beat trees. RF has the best main-method RMSE. No-dropout improves the seed 42 graph result, with single-seed limits. The blend selects XGBoost weight1, so there is no selected blend benefit. Retain unsuccessful findings.

Read [full measured tables](../../docs/PHASE2_RESULTS.md), `all_metrics.csv`, `seed_summary.csv`, `hybrid_selection.json` and `summary.json`. These are exploratory comparisons on a previously exposed test interval, not classification accuracy or an untouched holdout.

## Records

- `manifest.json`, `tuning.json`, `selected.json`, `experiments.json`: exact settings, source/data hashes, sensor order, normalization, selection and checkpoint identity.
- Per-fit folders: actual histories, completion records and exact reload checks. No model binaries/prediction tensors are included here.
- `verification.json`: target/baseline identity, historical metric comparison, bundle checksums and evaluation coverage.
- `checks.json`, `pytest.txt`, `package_check.json`, `environment.json`: actual checks/environment. `tiny_fit.json` is a synthetic learnability diagnostic, not traffic performance.
- `observed_history*_check.json`: inference interface examples from the training interval; not generalization evidence. Fitted checkpoint/statistics already contain the training interval.
- `source_snapshot_v1/`, `memory_equivalence.json`, `lineage.json`: storage-only amendment after host memory pressure. All 34,249 eligible histories were bitwise equal, normalization unchanged and restarted first-epoch losses identical. Five completed fits retain parent/checkpoint hashes; the incomplete candidate restarted from its fixed seed.
- `scheduling.json`: an active self-only fit was suspended/resumed for 581 seconds while its independent final seed finished. Live optimizer state was retained. Recorded timing includes contention/pauses and is not an isolated hardware benchmark.
- `source_snapshot.json`, `submission_artifacts.json`, `artifact_checks.json`: final local source and reviewed academic-artifact identity.

## Commands actually used

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  OMP_WAIT_POLICY=PASSIVE KMP_BLOCKTIME=0 PYTHONPATH=src \
  .venv/bin/python scripts/run_phase2.py --run-dir results/runs/phase2-v2 --device cpu
PYTHONPATH=src .venv/bin/python scripts/evaluate_phase2.py --run-dir results/runs/phase2-v2
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/pytest -q -ra
.venv/bin/ruff check .
.venv/bin/ruff format --check .
MPLCONFIGDIR=/tmp/t072-mpl-cache XDG_CACHE_HOME=/tmp/t072-cache \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src \
  .venv/bin/python scripts/build_phase2_report.py --run-dir results/runs/phase2-v2
```

Independent predeclared fits also ran in isolated staging folders with the same settings and selected learning rate, then were checksum-verified before publication into the local run. The run manifest and lineage describe inherited fits; it is not a single uninterrupted from-scratch run. Standard TeX fonts were downloaded after cached compilation failed; the final cached build succeeds with two minor underfull-line warnings and no missing fonts or overfull boxes. The PPTX finalizer initially needed its native-table policy and bundled runtime environment corrected; the final artifact passed. Restricted Matplotlib cache warnings were resolved with writable temporary caches. Earlier failed/stalled attempts are not counted as passes.

## Limits and next steps

The original project-specific brief remains unlocated. Speed-only forecasting does not establish calibrated LWR or multi-agent control; no simulated/real signal benefit is claimed. Timezone, raw-data redistribution rights, exposed-test status, owner review and genuine member learning remain explicit. Both upload artifacts are below 10 MB. Member ZIP handoffs/publication are later owner-coordinated steps; the one-time university-email form submission is not automated.
