# Experiment register

Initialization note (2026-10-22): no experiments had been conducted at scaffold creation. Executed experiments are recorded below.

Future entries need ID, date, hypothesis, dataset version/checksum, partitions, features, model settings, seed, environment, source commit, exact command, artifacts, horizon-wise metrics, interpretation, and limitations.


## EXP-001 — Independent-sensor Phase 1 tree comparison

- Date: 2026-10-26; status: executed, test interpretation exploratory.
- Dataset: existing METR-LA file; exact checksums in AML/verification/full-phase1-20261026/manifest.json.
- Hypothesis: causal temporal tree methods can reduce baseline speed-forecast error; no graph-model claim.
- Partitions: purged chronological split; train 23,963 anchors, tuning 1,701, second validation 1,702, test 6,850. Training stride 2; full evaluation grid.
- Models/features: M0 persistence, M1 HA, per-sensor multi-output RF and direct XGBoost; 38 causal features; seed 42; selected settings/candidate scores in manifest/tuning.json.
- Source: local uncommitted extension; per-file source hashes and actual Git base revision in manifest. No new commit or remote result invented.
- Command: `python scripts/run_all.py --run-dir results/runs/phase1-full-v1` from AML with the pinned isolated Python 3.12 environment; macOS OpenMP dependency installed.
- Results: complete per-horizon/mask/period metrics in verification evidence. XGB relative MAE reductions vs persistence at 15/30/60 min: 16.1/19.1/27.2 percent. RF lower headline RMSE. Training/artifact time 922.34 s; later evaluation/analysis additional.
- Limitations: exposed test, small tuning pilot, strided training, different missing-label training rules, unresolved clock/data rights, and 24 negative raw XGB forecasts. No fabricated accuracy, individual contributions, GAT or signal-control result.
