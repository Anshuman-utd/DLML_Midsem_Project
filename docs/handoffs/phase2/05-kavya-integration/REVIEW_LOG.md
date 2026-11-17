# Phase 2 integration/review — Kavya Katal

- Actual integration/review date: 2026-11-17, Asia/Kolkata.
- Role: evaluation, inference, evidence, CI/shared coordination and combined verification.
- Repository: canonical origin https://github.com/KatalKavya96/DLML_Midsem_Project.git.
- Branch: exactly kavya; base synced to owner-merged main 4dc98e2 (PRs #9–#12).
- Identity: configured Kavya Katal; no co-author trailer.
- Assistance: Codex-assisted preparation/integration/checking. Existing owner coordination, teammate prototype and substantial AI-assistance disclosures preserved. No independent student implementation or understanding is inferred.

## Integration and preservation

Original package verifier passed for all 90 assigned payload files and supplied baseline bytes. Preserved all 142 pre-sync local delta files in a private external backup. Compared every incoming main path before fast-forwarding: 47 exactly match prepared bytes; four completed teammate review logs and the neural test import/fixture correction intentionally differ and are preserved. All teammates' runtime modules and final academic artifacts remain unchanged from the merged base. The old partial-import failures remain historical in member logs; do not erase them.

Imported prepared scripts/evaluate_phase2.py and scripts/predict_phase2.py, CI/environment ignore protections, frozen November 12–16 evidence, requirements/results/runbook and shared navigation/coordination docs. Updated only coordinator-owned current-state/review/log records and added fresh verification/phase2-integration-20261117 evidence. Frozen manifests retain actual dates and identities. Existing source/checkpoints/data/scores were not tuned or regenerated. Current report/PPTX match the previously reviewed artifacts exactly.

## What these modules do

Evaluation reloads frozen checkpoints after source/data/normalization/order/lineage checks, aligns exact historical targets/masks and computes horizon/period errors. Optional blend weights are selected on reserved validation, not test; selected endpoint is pure XGBoost and no blend improvement is claimed. CSV inference takes at least 12 five-minute observed timestamps with exact sensor order, validates source/checkpoint identity and produces 12 future speeds for each of 207 sensors without future data. Shared docs explain reproducibility, metric trade-offs and synthetic-control boundaries; CI is prepared but a fresh remote run is not claimed.

## Actual checks and results

- OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/pytest -q -ra: **76 passed in 3.41 s**, no skips/failures, real data available.
- .venv/bin/ruff check .; .venv/bin/ruff format --check .: passed, 51 Python files formatted. git diff --check: passed.
- uv --cache-dir /tmp/t072-uv-cache pip check --python .venv/bin/python: 59 packages compatible.
- PYTHONPATH=src .venv/bin/python scripts/check_data.py: 34272×207, 8.11% zero/NaN missing, 1515 directed edges, adjacency reference match, partitions 23963/1701/1702/6850.
- scripts/predict_phase2.py with tune_graph_0 and tune_temporal_0 plus actual demo_history.csv: both saved 12×207 finite observed-history forecasts to ignored integration-20261117 CSVs. No new accuracy claim.
- PYTHONPATH=src .venv/bin/python scripts/run_control.py --run-dir results/runs/control-integration-20261117: 40 runs completed, per-step invariants enforced; metric/summary/paired CSVs byte-identical to original run and all 40 trajectory hashes verify. No policy tuning or original-run overwrite.
- uv offline wheel build succeeded; imports from the wheel outside checkout and a physical arrival-conservation update passed.
- Built-in LaTeX compiler: success. Final PDF/PPTX SHA-256 match previously rendered/agent-reviewed artifacts; below 10 MB. Native PowerPoint opening and new remote CI were not run.
- 31 Phase 1 source/config hashes, five raw data hashes, five neural-training source hashes, eleven evaluated checkpoint hashes and forecast metric hash all match their frozen records.

Fresh machine-readable evidence is in verification/phase2-integration-20261117/. No neural training/test tuning, fabricated metric or authorship claim. No push, PR, direct-main commit, remote merge or form submission. Local scoped commits are described by the current branch's actual git log; no self-referential future commit ID is invented.

## Limits and human work

Previously exposed test results are exploratory. Trees remain stronger on headline MAE/RMSE; graph improves matched neural controls only. LWR/control is separate synthetic physics with two hand-written agents, not calibrated LA, MARL or GAT-driven control. No specific faculty brief is available. Human explanation/reproduction and viva readiness are **not established by agent checks**. Owner reviews/publishes later; faculty acceptance is not certified.
