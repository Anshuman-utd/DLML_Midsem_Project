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

## EXP-002 — Shared temporal versus graph-aware neural forecasting

- Protocol recorded2026-11-12; execution/verification2026-11-12–13; owner/AI-assisted preparation, not independent member activity.
- Question: does supplied neighbour access improve a shared temporal model under matching chronological evaluation?
- Data/targets: same METR-LA sensor order, raw hashes,12 observed slots,12 future steps, purged splits 23963/1701/1702/6850; stride-two training, full evaluation origins. No label imputation.
- Inputs: normalized causal speed/missingness sequences plus five origin-calendar features. Shared GRU 32; graph 2 heads×16; direct residual forecast head. Self-only/uniform/no-dropout controls.
- Search: learning rates .001/.0003, seed 42, tuning-validation headlineMAE, Adam, decay .0001, dropout .1, clipping 5, batch 32, <=50 epochs, patience 7. Both core families selected.001. Seeds42/43/44 for temporal/graph/self; auxiliary controls42. Thirteen completed unique fits; eleven evaluated.
- Run: results/runs/phase2-v2. Manifest/lineage preserve a bitwise-verified memory-only amendment and five inherited fits; active-process suspension is separately recorded. Source is local/uncommitted on kavya; no source commit is invented.
- Results: graph mean 60-minute MAE4.881±0.003 mph, self 4.931±0.007, temporal 4.929±0.002; XGBoost 3.874 and RF 3.896. Graph improves its neural control but not the tree methods. No-dropout seed 42 has MAE4.847 versus fullgraph 4.877. Hybrid chose pure XGBoost on reserved validation; no blend benefit selected. See all_metrics.csv for every metric/horizon/slice/count.
- Verification:69 tests/no skips, lint/format, dependency compatibility, wheel import, exact checkpoint reload, CSV inference and historical baseline reproduction passed. Actual commands/checks/artifact SHA-256 values are in verification/phase2-20261112/.
- Limits: previously exposed test, one region/season, bounded tuning/compact architecture, single-seed auxiliary controls, unresolved clock/raw-data rights and original faculty-scope gap. LWR theory is discussed; calibrated LWR/control are not implemented or claimed. No publication/form submission.

## EXP-003 — Synthetic LWR corridor and two local rule-based signal agents

- Protocol/configuration recorded before outcomes on 2026-11-16; owner/AI-assisted local preparation, not independently completed student activity.
- Scope: eight-cell CTM, triangular flux, 0.25 km cells, 5 s updates, free speed 60 km/h, backward wave magnitude 20 km/h, jam density 150 veh/km; implied capacity 2250 veh/h. CFL, conservative simultaneous updates, supply/demand and retained external queues are checked.
- Policies: equal-green fixed 40 s/5 s clearance with declared offset; occupancy-pressure-inspired local agents with 20 s minimum and 60 s maximum green, 5 s all-red clearance. Two junctions interact through the corridor. No learned reward/policy, MARL, neural forecast input or calibrated LA parameters.
- Design: balanced, arterial peak, side peak and downstream restriction; seeds 101–105, identical arrivals within each pair, 60 min arrivals plus 20 min drain; 40 completed runs, no outcome-based policy tuning.
- Run: results/runs/control-20261116-v1. Full trajectories remain local/ignored. Small manifests, trajectory checksums, per-run metrics, five-seed summaries and invariants are in verification/phase2-final-20261116/control/.
- Mean system vehicle-minutes fixed/responsive: balanced 3263.3/2212.8; arterial peak 10850.7/2840.5; side peak 6435.1/3173.6; downstream restriction 14308.9/6003.9. These include moving vehicles, not mean completed-trip delay. External-boundary waiting and final residuals are reported separately. Maximum mass residual across runs: 3.0411229090532288e-12 vehicles.
- Interpretation: responsive agents outperform this equal-green baseline for the selected synthetic scenarios; the baseline is not demand-optimized. No general optimality, real-city delay saving or GAT-control benefit is demonstrated.
- Verification: seven added physics/agent tests; assembled suite 76 passed/no skips (latest 2.40 s); Ruff 51 files passed; all 40 runs check invariants every step; source and trajectory hashes verified. Frozen forecasting scores/checkpoints/data remain unchanged. No publication/form submission.

## 2026-11-17 — Integration reproduction, no new tuning experiment

Reran the existing frozen control configuration in results/runs/control-integration-20261117: all 40 paired cases complete and metric/summary/paired CSV bytes exactly reproduce EXP-003, with trajectory hashes verified. No policy/model/parameter changes. Graph and temporal saved-checkpoint observed-history CSV inference also pass. Assembled suite: 76 tests/no skips. Historical forecast/checkpoint/data/source/metric identities unchanged. Evidence: verification/phase2-integration-20261117/. This is a fresh reproduction/integration check, not new model selection or independent student activity.
