# Phase 2 completion plan — prospective record

Status update 2026-11-13: the bounded forecasting study was executed locally. Actual results/checks/artifacts are in PROJECT_STATE.md and verification/phase2-20261112/. This preserves the original plan; the proposed dates/roles below are not fabricated activity records.

Prepared: 2026-11-12, Asia/Kolkata. No Phase 2 implementation, model training, score improvement or faculty scope acceptance is claimed by this plan.

## Sources and authority

- Verified generic faculty rubric: `CSAI_Project_Instructions_Phase_1_and_Phase_2.pdf`, Phase 2 and individual viva sections.
- Owner-supplied evaluation email: evaluation 2026-11-19, 13:55–14:20; submission by 12:55 IST; room A410. Presentation PPTX/PDF <=10 MB, LaTeX report PDF <=10 MB, GitHub link. One university-email submission by one member.
- Original planning attachment: `/Users/kavyakatal/.codex/attachments/723e549b-d668-42ae-a933-c0114f34a1bd/Pasted text.txt`. Describes graph-aware versus independent-segment forecasting and optional simulated signal policies. This is supplied planning/background, not independently verified original faculty wording.
- Historical teammate proposal: `docs/PHASE1_PLAN_SUBMITTED_2026-10-25.md`. Contains graph, LWR and hybrid suggestions, including proposals not implemented in Phase 1. Its own provenance warning applies.
- Actual implementation/evidence: `PROJECT_STATE.md`, `src/trafficml/`, `verification/full-phase1-20261026/`.
- Repository, attachments, archive and candidate Downloads PDFs were searched. No standalone original faculty Project 4 technical brief was identified. Consequently this plan covers the verified DL rubric and documented forecasting objective; it cannot certify additional project-specific control/LWR requirements absent that source.
- The Downloads End-Sem_Project_Rubric.pdf concerns GenAI/Agentic AI, not this verified DL rubric. Do not import its deployment/video/GenAI requirements without faculty confirmation.

## Proposed question and boundaries

Does using the supplied road-network neighbours improve multi-horizon speed forecasting over temporal-only learning under the same protocol?

Reuse METR-LA, the validated sensor order/graph, 12 history slots, 12 future targets and 15/30/60-minute headline metrics. Preserve Phase 1 evidence unchanged. No promised accuracy or automatic graph superiority. Learned forecasting nodes are not control agents.

## Models

1. Retain four Phase 1 comparison methods: persistence, historical average, independent-sensor Random Forest and direct XGBoost. Validate saved prediction identity or rerun frozen configurations if the evaluation protocol changes.
2. Temporal GRU baseline: one shared per-sensor GRU, 32 hidden units; origin calendar features plus a linear head predicting 12 horizons. No neighbour input.
3. GRU + GAT: encode each sensor history with the same GRU design, aggregate final node embeddings through one graph-attention layer (two heads, 16 channels/head), then forecast 12 horizons through a shared head. Document any residual connection explicitly and preserve it across graph ablations.
4. Optional ML–DL hybrid: blend frozen XGBoost and GAT forecasts. Choose one global weight from {0, .25, .5, .75, 1} using val_stack only; freeze before test. Include pure-model endpoints and report if the hybrid offers no benefit. Do not tune/report a new untouched holdout using the same selection data.

Sizes above are starting proposals, not completed tuning decisions. Explain temporal memory, neighbourhood attention, prediction heads and direct multi-horizon outputs. Do not add LSTM/Transformer/DCRNN implementations merely to increase model count.

## Data contract and evaluation freeze — before training

- Load actual data, verify graph direction and tensor node order, document edge semantics and self-loops. Use the existing thresholded graph's connectivity mask; do not silently treat Gaussian weights as attention probabilities.
- Inputs: [batch, 12 history slots, 207 sensors, 2 channels], containing causally filled speed and original missingness flag. Append the same five origin-calendar features to both neural model heads. Outputs: [batch, 12 horizons, 207 sensors].
- Keep original targets/masks; never impute labels. Masked losses must return safely or skip when an entire batch has no valid targets.
- Reuse causal history filling and training-only sensor medians. Fit one global speed mean/std using valid training observations only; transform filled inputs and targets consistently. Convert predictions back to mph before scoring. Specify handling for zero scale and nonfinite outputs.
- Reuse chronological purged splits. Fit weights on train, tune/early-stop on val_tune. Reserve val_stack for optional hybrid weight selection; if repurposed, document that before looking at its results.
- Existing test interval is already exposed. Freeze the Phase 2 protocol prospectively; use the old interval only for clearly exploratory matched comparisons. A genuinely new holdout requires additional unexposed data and recomputation of all comparable baselines.
- Use matching masks and full evaluation origins for all models. Begin with Phase 1's stride-two training origins for compute comparability; any changed sampling is recorded and controlled in comparisons.
- Traditional models use 38 engineered features while neural models use sequences/calendar inputs. ML-versus-DL results therefore compare pipelines, not graph information alone. Full graph versus self-loop-only neural comparisons isolate neighbour availability more closely.

## Training and regularization

- First verify a small forward/backward pass and that a tiny subset can be overfit; this is a diagnostic, not reported generalization evidence.
- Starting proposal: Adam, learning rate .001, batch size 32, masked MAE loss, explicit dropout .1 after GRU embeddings / in graph module, weight decay .0001, gradient clipping 5, maximum 50 epochs, early-stop patience 7.
- A one-layer GRU needs an explicit dropout module; its recurrent dropout argument alone does not implement inter-layer dropout with one layer.
- Compare learning rates {.001, .0003} per core architecture on val_tune with one fixed seed; stop a divergent run and document it. Expand a search only for a recorded reason, not test scores.
- Save best validation checkpoint, optimizer/config/seed, normalization, masks, data/source hashes, epoch history, parameter count and timing. Evaluate the saved checkpoint, not arbitrarily the last epoch.
- Target three seeds for temporal, full graph and self-loop-only models; report mean/std of run-level metrics. Small error differences and dependent forecasts do not establish significance.

## Ablations

| Comparison | Controlled change | Question |
| --- | --- | --- |
| Full graph vs self-loops only | Same graph-model code/settings; remove neighbour edges | Does neighbour information help? |
| Learned attention vs uniform neighbour averaging | Keep temporal encoder/head and same neighbourhood | Does learned weighting help beyond averaging? |
| With vs without explicit dropout | Same selected architecture and other settings | Does this regularizer affect validation gap/performance? |

Temporal GRU is an additional architecture baseline, not the sole graph ablation. Uniform-attention and no-dropout experiments may initially use one disclosed seed; distinguish them from multi-seed evidence. Use the same frozen hyperparameters for each ablation unless an explicitly equal retuning budget is documented.

## Required evidence

- Common-mask MAE/RMSE/MAPE at 15/30/60 minutes, all-horizon MAE curve and valid counts. No 100-MAPE accuracy.
- Peak/off-peak and per-sensor results; retain timezone caveat. Add weekday/weekend results using existing evaluator.
- Training/validation curves, ablation table, seed variability, parameter counts, runtime and inference example.
- Fixed sensor/day actual-versus-predicted plot, per-sensor error map and attention example. Attention is model behaviour, not causal proof of physical influence.
- Test graph direction/node-order, causal features, training-only scalers, target masks, output dimensions, finite losses and checkpoint reload reproduction.
- Literature: GRU foundation, GAT, DCRNN as traffic/graph context, and LWR foundation. Cite what was actually read; proposed reference count is not a rubric minimum.

## LWR / control scope

Include an accurate theory subsection: density rho, flow q, speed v, conservation equation d(rho)/dt + d(q)/dx = 0 and q = rho*v, plus why congestion propagation motivates network forecasting. Ground equations and interpretations in primary sources before report authoring.

METR-LA supplies speed, not measured density/flow or calibrated signal dynamics. Do not claim calibrated LWR, multi-agent control, measured queue reductions, or upstream propagation solely from graph-attention pictures. Historical chain cross-correlation is a proposed analysis, not a validated physical wave-speed measurement.

If the original brief/faculty confirms LWR/control implementation is compulsory, add a separately specified small simulated traffic-network experiment with explicit synthetic demand/physics parameters, multiple controllers, a fixed-policy comparator and delay/queue/throughput metrics. Validate dynamics, conservation, constraints and matched scenarios. Clearly separate simulation evidence from METR-LA forecasting. This is a conditional workstream, not covered by forecasting MAE, and may change the schedule. Do not label that work optional as a verified faculty ruling.

## Rubric mapping

| Verified category | Completion evidence |
| --- | --- |
| Architecture logic | Temporal/graph diagram, dimensions, direction, attention and forecast-head explanations |
| Hybrid innovation | Optional validated blend, rationale and endpoint comparison; honest negative result if applicable |
| Ablation studies | Controlled neighbour, attention and dropout comparisons |
| DL literature review | Source table connecting papers to actual design/limitations |
| DL dataset and regularization | Training-only transforms/masks, dropout/weight decay/early stopping, learning curves |
| Technical validation | Same-target evaluation, tests, seeds, saved checkpoints and reproduced inference |
| Theoretical rigor | GRU gates, GAT weights, masked loss, chronology, metrics and LWR/data limitations |
| GitHub and code quality | Modular code, environment, meaningful PRs, tests, reproduction instructions and provenance |
| Presentation/report/viva | Measured tables, LaTeX PDF, architecture/slides, real contributions and individual demonstration |

## Proposed genuine responsibilities

- Rudraksh: data/graph integrity, tensor loading and node-order tests.
- Vridhi: normalization, masks, causal input preparation and temporal GRU review/implementation.
- Anshuman: literature/EDA extensions, learning curves, maps and error interpretation.
- Bineet: GAT component, controlled ablations and optional hybrid implementation/review.
- Kavya: experiment contract, integration, evaluation, combined verification and submission coordination.

Assignments are proposals, not completed student contributions. All five must understand the full study, demonstrate their part and record actual work/assistance.

## Schedule and exit criteria

- Nov 12: scope/source record, protocol, environment and tiny end-to-end checks.
- Nov 13: temporal baseline verified; graph direction/order and GAT forward pass verified.
- Nov 14: graph model trained; bounded validation tuning completed.
- Nov 15: main-seed runs and neighbour ablation; detect failures before adding scope.
- Nov 16: remaining ablations, optional hybrid and full evidence export; freeze model choices.
- Nov 17: report and slides from measured outputs; correct existing presentation numerical errors.
- Nov 18: clean reproduction, final file review, mock viva and offline demo; target readiness by evening.
- Nov 19: one member submits verified university-email form by 12:55 IST, evaluation 13:55–14:20 in A410.

Complete means implemented pipelines/checkpoints and tests reproduce, baseline and ablation results are honestly reported, source-scope gaps are resolved or explicitly acknowledged, each member can explain the work, and both upload artifacts are <=10 MB with the correct GitHub link. A poor or negative DL result is not fixed by altering test methodology or fabricating improvement. This plan alone does not certify all project-specific requirements or faculty acceptance.


## Final local extension — 2026-11-16

The owner requested closing remaining LWR/control work. A separate illustrative CTM simulation with two rule-based agents, four predefined scenarios and five paired seeds completed40 runs; the assembled suite passed76 tests. Original faculty-specific brief remains unlocated; see PHASE2_REQUIREMENTS_FINAL_AUDIT.md. This addition does not change neural scores or claim calibrated/MARL/GAT-driven control.
