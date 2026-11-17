# Phase 2 measured results — learning companion

Generated from the frozen local run, not manually entered scores. All errors use matching actual targets/masks. Lower is better. The old test interval remains exploratory.

## Main methods

MAE/RMSE are mph. Neural rows are mean ± sample standard deviation over three separately trained seeds, not an ensemble of their predictions.

| Method | MAE15 | MAE30 | MAE60 | RMSE15 | RMSE30 | RMSE60 |
| --- | --- | --- | --- | --- | --- | --- |
| Persistence | 3.482 | 4.173 | 5.321 | 6.374 | 7.983 | 10.250 |
| Historical average | 4.187 | 4.187 | 4.187 | 7.852 | 7.852 | 7.852 |
| Random Forest | 2.972 | 3.423 | 3.896 | 5.438 | 6.374 | 7.255 |
| XGBoost | 2.920 | 3.376 | 3.874 | 5.777 | 6.911 | 7.993 |
| Temporal GRU | 3.119 ± 0.001 | 3.811 ± 0.001 | 4.929 ± 0.002 | 6.112 ± 0.006 | 7.674 ± 0.004 | 9.721 ± 0.005 |
| GRU + GAT | 3.099 ± 0.001 | 3.780 ± 0.002 | 4.881 ± 0.003 | 6.067 ± 0.004 | 7.606 ± 0.006 | 9.619 ± 0.003 |

At 60 minutes, graph mean MAE is 4.881 mph versus 4.931 mph for self-only and 4.929 mph for the smaller temporal model. Graph versus self-only is the closer neighbour-access comparison; graph versus trees also changes representation and training design.

## Controlled seed42 ablations

| Variant | MAE15 | MAE30 | MAE60 |
| --- | --- | --- | --- |
| GRU + GAT | 3.098 | 3.778 | 4.877 |
| Self-loop graph | 3.109 | 3.802 | 4.923 |
| Uniform neighbours | 3.101 | 3.785 | 4.891 |
| No dropout | 3.075 | 3.756 | 4.847 |

Compare each row with full graph at the same seed. Uniform/no-dropout have one seed; they do not establish robust superiority from one run. All controls keep selected graph settings rather than receiving separate tuning.

### Three-seed neighbour comparison

| Variant | MAE15 | MAE30 | MAE60 |
| --- | --- | --- | --- |
| GRU + GAT | 3.099 ± 0.001 | 3.780 ± 0.002 | 4.881 ± 0.003 |
| Self-loop graph | 3.116 ± 0.006 | 3.809 ± 0.007 | 4.931 ± 0.007 |

Entries are mean ± sample standard deviation over seeds42/43/44; this is run variability, not a significance test.

## Optional hybrid

Reserved validation selected XGBoost weight 1; graph weight is 0. The following graph row is seed42, the actual blend constituent.

| Method | MAE15 | MAE30 | MAE60 |
| --- | --- | --- | --- |
| XGBoost | 2.920 | 3.376 | 3.874 |
| Graph seed42 | 3.098 | 3.778 | 4.877 |
| Selected blend | 2.920 | 3.376 | 3.874 |

## Traffic-period differences

| Method | Peak | Off-peak | Weekday | Weekend |
| --- | --- | --- | --- | --- |
| Random Forest | 5.954 | 3.379 | 4.041 | 3.333 |
| XGBoost | 6.308 | 3.261 | 4.073 | 3.098 |
| Temporal GRU | 7.751 | 4.220 | 5.308 | 3.454 |
| GRU + GAT | 7.691 | 4.174 | 5.251 | 3.435 |

These are 60-minute MAE values; neural rows average seeds. Peak follows recorded clock time, whose timezone remains unresolved.

## Computational record

| Variant | Stored parameters | Seeds | Epochs | Mean minutes/fit |
| --- | --- | --- | --- | --- |
| Temporal GRU | 3912 | 3 | 35--50 | 16.5 |
| GRU + GAT | 5384 | 3 | 35--48 | 23.5 |
| Self-loop graph | 5384 | 3 | 30--48 | 23.8 |
| Uniform neighbours | 5384 | 1 | 48--48 | 27.8 |
| No dropout | 5384 | 1 | 50--50 | 24.7 |

Wall times include validation, host pressure, scheduling pauses and overlapping fits. They are not isolated speed benchmarks. Some stored score parameters are inactive in self/uniform controls.

## Physically invalid negative forecasts

| Variant | Negative outputs |
| --- | --- |
| Temporal GRU | 0/0/0 |
| GRU + GAT | 0/0/0 |
| Self-loop graph | 0/0/0 |
| Uniform neighbours | 0 |
| No dropout | 0 |

Counts are out of 17,015,400 raw test outputs per fit, including unscored missing targets. Triples follow seeds42/43/44; single values use seed42. Forecasts were not clipped after scores were observed. No negative neural outputs occurred in this run. The unconstrained head does not guarantee physically bounded forecasts on other inputs.

## How to defend the findings

State winners separately for each metric/horizon and traffic slice. Do not hide an ablation that worsens or a simple method that wins. MAE is typical absolute error; RMSE emphasizes large misses. Neither MAPE nor 100 minus MAPE is accuracy. Seed spread is not statistical significance, and attention is not causal proof.

## Evidence and remaining limits

See verification/phase2-20261112/all_metrics.csv, seed_summary.csv, experiments.json and hybrid_selection.json for exact values, valid counts and selection evidence. Source/data/checkpoint identity and inheritance lineage are retained. No test-driven retuning or clipping was performed.

This component forecasts speed. The separate November16 synthetic LWR/control study is documented in PHASE2_CONTROL_RESULTS.md; it is not calibrated or GAT-driven control. The original project-specific brief remains unlocated. Final scope acceptance, student understanding and publication are separate steps. Prepared source and analysis use substantial owner/AI assistance; preserve prototype provenance.
