# Prospective Phase 2 experiment protocol

Recorded 2026-11-12 before any real-data neural fitting or test evaluation. Owner authorized Phase 2 implementation. This document and configs/phase2.yaml define the initial bounded study. Any amendment must be recorded before dependent evaluation and cannot be justified by exposed test scores.

## Data and comparison

Reuse METR-LA and validated sensor ordering/adjacency, 12 history slots, 12 future targets, the Phase 1 purged chronological partitions and training stride 2. Baselines are frozen Phase 1 predictions, checked against actual targets and IDs before combination. Old test is exploratory, not an untouched holdout. Do not tune using its labels or scores.

Zero/NaN means missing under the benchmark policy; raw data stay unchanged. Causal forward fill within each sample followed by training sensor median. If a sensor has no valid training reading use the global training mean, disclose this exceptional fallback. Fit global mean/std only from valid training values. Neural inputs are normalized speed plus original missing flag; five origin-calendar features enter the head. Mask future missing labels from loss/scoring; skip all-missing training batches. No target imputation. MAE is used for training, normalized by the common global training scale; report in mph.

## Architecture

Shared per-sensor one-layer GRU, 32 hidden units. Temporal model: GRU embedding + calendar -> linear 12-output head. Graph model: GRU local embedding + one GAT aggregate + calendar -> linear 12-output head. GAT has 2 heads, 16 channels/head, additive original-style attention with LeakyReLU and masked softmax. Explicit dropout .1 on GRU embeddings and attention. Output equals latest filled normalized speed plus learned correction; zero-initialize final head so training starts at this persistence-like forecast. This starting forecast uses the training median for an all-missing history, while the reported Phase 1 persistence baseline uses historical average in that case; disclose the distinction.

The supplied adjacency is directed with entries [from,to]. Graph messages use mask[receiver,sender] = adjacency[sender,receiver] > 0, with self loops. Gaussian edge magnitudes determine connectivity only, not attention strength. Physical upstream/downstream interpretation is unverified and not claimed. A model's attention is not causal evidence of real congestion propagation. This architecture is not DCRNN and not a simulation/controller.

## Search and controlled runs

For each temporal/graph family: two learning-rate candidates (.001 and .0003), Adam weight decay .0001, clip gradients to norm 5, batch 32, <=50 epochs, early stopping patience 7. Select pooled headline 15/30/60-minute val_tune MAE only, using every tuning-validation origin. No val/test refit. Checkpoint the best validation epoch. Predeclared seeds 42/43/44 for selected temporal, graph and self-loop graph; uniform-attention and zero-dropout graph use seed 42 initially with limitations explicit. Graph ablations share the selected graph learning rate and other settings; removing edges or replacing attention is the controlled change. CPU/GPU device chosen from synthetic timing and compatibility checks before real training. Benchmark showed MPS slower for this small recurrent workload; CPU chosen. Pure compute settings may be amended from synthetic timing, recorded before fitting.

No neighbour ablation is the same graph module with identity connectivity; uniform ablation averages the same permitted neighbours. Temporal GRU differs in capacity from graph model, so the self-loop control is necessary. Uniform mode retains unused attention-score parameters to preserve module/checkpoint structure; report effective parameter distinction.

## Optional hybrid and evaluation

### Memory-only amendment before final evaluation

The eager cache required680,596,128 bytes of history features. After severe host RAM pressure stalled an unfinished fit, phase2-v2 changes only the timing of feature construction: batches are generated on demand (635,904 feature bytes for batch 32). All 34,249 eligible raw-data histories were compared bitwise, and fitted state was identical. The original source snapshot and phase2-v1 manifest are preserved; five completed fits are inherited with checkpoint/parent hashes in phase2-v2/lineage.json. The unfinished learning-rate candidate restarts from its fixed seed. No model, feature definition, search budget, split or metric was changed. Final reports must preserve this lineage rather than implying all fits used identical source-file bytes.

Independent predeclared fits may overlap on CPU to reduce total elapsed time. Completed fits can be moved from distinct staging folders only after checking selected learning-rate identity; active folders are never shared. Per-fit wall times under contention are not isolated hardware benchmarks. A dense-versus-sparse equivalent GAT synthetic timing experiment showed no material gain, so the original dense implementation was retained; no real-data scores drove that implementation choice.

After base model settings are frozen, fit one global blend weight alpha in {0,.25,.5,.75,1} for alpha*XGBoost+(1-alpha)*graph on val_stack headline MAE only, seed 42 models. No extra tuning on val_stack for base models. Evaluate frozen blend once and include pure endpoints. If no improvement, report failure to demonstrate hybrid value.

Report per-seed scores and mean/std for main models, not a best-test seed. MAE/RMSE/MAPE all 12 horizons and slices all/peak/off_peak/weekday/weekend on identical valid points. Peak definition matches Phase 1 recorded clock. Low positive values affect MAPE. Keep negative predictions unmodified for primary evaluation; report count rather than post-hoc clipping. Save forecasts, parameter counts, curves, per-sensor errors, fixed sensor/day example, checkpoint hashes and inference reproduction.

Source/data/config/device/runtime identity is frozen in a run manifest before fitting. A completed run refuses resume after identity changes. Checkpoints and predictions remain gitignored; small evidence and academic deliverables may be tracked. Do not overwrite Phase 1 artifacts or fabricate results.

Implementation detail versus the initial plan: best checkpoints contain model weights, configuration, normalization, mode/seed/learning-rate and epoch, but not optimizer state. Incomplete fits restart from the fixed seed; there is no optimizer-state continuation. The runner reuses completed fit records under the run identity; the evaluator verifies checkpoint checksums/metadata before scoring. The coordinator also verifies staging-folder checksums before publication into the local run. This changes recovery cost, not the declared training/evaluation algorithm.

## Scope and sources

The generic CSAI PDF is verified; the 2026-11-06 email supplies Nov19 deadline/slot. Original master and historical teammate plan are background/proposals, not independently verified original faculty Project 4 wording. LWR theory and missing measured flow/density must be discussed. Calibrated LWR, multi-agent control or real signal improvements are not claimed. Any mandatory simulation discovered in the original brief needs a distinct scoped implementation and verification.

Primary implementation/theory sources: Cho et al., 2014, https://arxiv.org/abs/1406.1078; Velickovic et al., 2018, https://arxiv.org/abs/1710.10903; Li et al., 2018, https://arxiv.org/abs/1707.01926; official PyTorch GRU/module documentation. Sources support components, not scores or correctness of this implementation.


## Separate extension — 2026-11-16

The owner requested final completion and LWR/control checking. A separate synthetic cell-transmission/two-agent study is now recorded in PHASE2_CONTROL_PROTOCOL.md. It does not change this forecasting protocol, source/checkpoints or scores, and it does not establish GAT-driven control. The earlier theory-only deferral above is historical to the forecasting study.
