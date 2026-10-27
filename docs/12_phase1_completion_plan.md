# Phase 1 completion plan and five-member work allocation

Prepared 2026-10-26 at the owner's request. This is a recommended delivery plan, not evidence that its tasks are completed or that every methodological choice has been accepted. Member availability and acceptance remain to be confirmed. No code, training, installation, or publication is authorized by this planning document alone.

> Status update: the integrated local implementation and EXP-001 now exist; see [current state](../PROJECT_STATE.md). This earlier plan is retained as the delivery/learning checklist. Individual contributions and viva readiness are not certified.

## Delivery sequence update — integrated version before member handoffs

The owner prefers completing and testing the integrated Phase 1 version together before distributing module ownership to the five members. The assignment cards below are handoff/learning/review areas, not instructions to manufacture separate authorship histories for existing code.

1. Build the integrated reference implementation, execute actual experiments, resolve defects and prepare the agreed research outputs. Preserve accurate authorship, assistance disclosures and experiment history.
2. Package each module with its purpose, theory, inputs/outputs, code walkthrough, reproduction steps, known limitations and concrete follow-up tasks.
3. Each student studies their module and the full pipeline, reproduces its results, reviews another module and makes substantive corrections, tests, analysis, documentation or extensions they can explain.
4. Students commit their actual work from their own accounts. Do not impersonate members, backdate commits, reassign existing authorship or split already-written files into commits that falsely imply independent implementation. Attribute assisted work according to applicable course requirements.
5. Record initial implementation and subsequent member contributions separately. Final readiness still requires individual understanding and the owner's acceptance of important choices.

This changes the delivery sequence; it does not mark the project complete, accept unresolved technical decisions, or authorize another publication. The first work remains requirements and methodology documentation; Phase 2 stays deferred.

## 1. Completion target and requirement sources

The supplied generic faculty instructions assess literature review, dataset quality/EDA, feature engineering, theoretical rigor, model application, repository/code quality, presentation, individual viva, and a LaTeX/IEEE report. The owner's supplied master instruction additionally specifies the traffic-specific methodology: chronological partitions, comparable history windows, training-only fitted preprocessing, missing/outage handling, MAE/RMSE/MAPE, horizon-wise comparisons, peak/off-peak analysis, and discussion of independent-segment limitations.

The project-ideas PDF itself is not available in the reviewed materials. Reconcile it before describing any particular model or number of experiments as mandatory. This checklist is a defensible completion target against the supplied requirements, not a guaranteed grade or faculty sign-off. No fixed accuracy threshold, paper count, slide count, or report length is established by the supplied generic rubric.

### What already exists

The corrected [prototype](../README.md) contains data loaders, graph construction/verification, missing-value handling, purged chronological partitions, two forecasting baselines (M0 persistence and M1 historical average), evaluation utilities, manifests, and regression tests. The verified local-data suite passed 51 tests. Sandbox source was published at commit `a020778`; GitHub CI subsequently passed. Existing baseline test results have already been inspected and must not be called an untouched final holdout.

### Recommended completion scope

Keep the two existing baselines and add **Random Forest and XGBoost** for a four-method comparison. This model pair is our recommended scope, not a faculty requirement to implement both. If time/compute is insufficient, a narrower set with one rigorously evaluated learned ML model should be agreed with the owner/faculty before reducing scope. Ridge is an optional additional linear reference. Graph-neighbour features, SHAP, extensive significance studies, a dashboard, and Phase 2 are not prerequisites in this completion plan.

Improvement over the baselines is an experimental question, not a promised outcome or an automatic completion criterion. A weaker learned model must be reported and investigated honestly.

## 2. Required work packages and evidence

| ID | Remaining deliverable | Primary owner | Evidence needed for acceptance |
| --- | --- | --- | --- |
| P1-01 | Reconcile scope and freeze a proposed evaluation contract | Rudraksh; owner accepts decisions | Requirements traceability, title/LWR clarification, targets, horizons, splits, masks, tuning rules and holdout disclosure |
| P1-02 | Dataset suitability, provenance and EDA | Anshuman | Verified source/field/unit/licensing notes, quality audit, training-focused EDA figures and dataset recommendation for owner review |
| P1-03 | Causal feature pipeline | Vridhi | Documented feature schema, reproducible feature generation, masks and leakage/alignment tests |
| P1-04 | Random Forest experiments | Bineet | Working training/prediction path, validated outputs, validation-selected configuration, runtime and training-coverage records |
| P1-05 | XGBoost experiments | Kavya | Working training/prediction path, validation-selected configuration, runtime and coverage records, validated outputs |
| P1-06 | Fair comparisons and error analysis | Rudraksh integrates; Bineet/Kavya provide runs; Anshuman provides plots | Four-method metrics, headline horizons, full error curves, peak/off-peak results, representative prediction plots and limitations |
| P1-07 | Literature synthesis and theoretical explanation | All five; Anshuman edits review table | Verified citations, paper comparison, method/data relevance, equations with explained symbols and limitations |
| P1-08 | Reproducible repository and contribution evidence | Rudraksh coordinates; everyone contributes | Fresh-environment setup, tests, CI, manifests, configs, complete reproduction instructions, genuine individual contribution records |
| P1-09 | IEEE/LaTeX report and presentation | Everyone authors their section; Rudraksh assembles report; Kavya assembles slides | Compilable source/PDF, figures traceable to experiments, consistent slides, limitations and contribution statement |
| P1-10 | Individual viva readiness | All five | Each member can explain and demonstrate the whole pipeline, including another member's module |

## 3. Shared technical contract — review before implementation

The following is a concrete proposal to prevent incompatible contributions. It preserves the current prototype interface; it is not an accepted ADR.

- **Working code location:** the standalone sandbox's `src/trafficml/`, `scripts/`, `configs/` and `tests/`. The main repository's `src/traffic/` is still a scaffold. Do not independently implement the same package in both places.
- **Target:** future speed for each sensor. Verify units and available measured channels; do not invent flow or occupancy. Dataset selection requires a documented recommendation and owner acceptance.
- **History:** 12 five-minute observations, ending at forecast origin t. Feature computations must not read observations after t.
- **Outputs:** retain all 12 future steps in an array `(samples, 12, sensors)`. Highlight offsets 3/6/12 as 15/30/60 minutes. Include explicit sensor order and forecast anchors; validate against immutable targets.
- **Compatibility warning:** producing only three columns currently makes the evaluator label them as 5/10/15 minutes. Do not silently substitute a three-horizon tensor. Any reduction requires a shared explicit horizon-offset schema and consistent changes to every method, evaluator and test.
- **Partitions:** retain the corrected purged chronological implementation while reviewing the formal protocol. Current retained counts are 23,963 training anchors, 1,701 tuning anchors, 1,702 reserved-validation anchors, and 6,850 test anchors. The validation-half/stacking allocation remains provisional, not an approved Phase 2 commitment.
- **Holdout:** do not tune using the already-inspected test results. Record that exposure. Decide a defensible future reporting/validation protocol with the owner; do not invent a fresh holdout or repeatedly choose its boundaries after seeing performance. Rolling-origin validation inside training is an option for review.
- **Preprocessing:** fit imputation statistics, profiles, scalers and any learned threshold on the permitted training interval only, and refit inside each temporal validation fold. Never impute targets. If historical-profile features are introduced later, specify out-of-fold construction before implementation; a full-training target-derived profile is not automatically safe for its own training rows.
- **Missing inputs:** preserve missingness indicators; agree a causal bounded fill and training-only fallback for completely missing windows. Do not drop difficult evaluation points separately for each model. A model fallback must be specified before evaluating it and its usage counted.
- **Scoring:** same target masks, sensor order, forecast anchors and horizons for all methods. Report valid counts. Keep MAE/RMSE aggregation, MAPE denominator/low-speed policy, speed units and peak-window definitions explicit.
- **Artifact identity:** freeze the integrated source/configuration before generating a comparison run. Existing manifests reject source changes. New code/config/data requires a new run and regeneration of the common artifacts; do not mix predictions from different run identities.
- **Compute:** develop with a small, documented sensor subset, benchmark runtime/memory, then use the accepted full evaluation coverage. A subset result must never be presented as a 207-sensor result. Final coverage/reductions need explicit agreement and disclosure.

## 4. Individual assignment cards

### Rudraksh Sharma — methodology, integration and evaluation

**Inputs:** current corrected sandbox; supplied requirements; Anshuman's dataset findings; Vridhi's feature contract; Bineet/Kavya's prediction outputs.

**Tasks:**

1. Complete requirements traceability and explain the target, forecast origin, horizon, chronology, purging, masking and aggregation. Prepare proposed decisions for owner review rather than accepting them on behalf of the team.
2. Establish the common interfaces and a recorded plan for the exposed test set before model tuning. Resolve the provisional validation-half allocation.
3. Review feature/model integration; retain immutable target and alignment checks. Ensure all model code is included in one source snapshot before a shared run.
4. Extend the common runner/evaluator for the agreed learned models. Collect overall and horizon-wise MAE/RMSE/MAPE, valid counts, peak/off-peak results, runtime, fit/predict boundaries and fallback counts.
5. Maintain reproducibility commands, environment pins, configs, run manifests, issue/experiment records and CI. Reproduce the final agreed pipeline from a clean environment.
6. Assemble the report from the five authored sections; cross-check all metric claims against saved runs.

**Planned outputs:** completed methodology/traceability documents, common evaluation/configuration contract, integration tests, reproducible comparison tables, experiment register, report source and compiled report. Paths for new scripts/configs must be documented when implementation is authorized; no executable command is claimed to exist yet.

**Acceptance:** no shared target timestamps across ordered partitions; no preprocessing fit beyond allowed boundaries; all methods scored on the same points; source/config/data identity verified; genuine tests/CI and clean-environment reproduction recorded. Report accurately distinguishes proposals, observed results and limitations.

**Reviewer:** Kavya, with each model owner checking their own method's integration. **Theory to explain:** regression, leakage, chronological validation, metric definitions, purging, fair comparison, and inference versus training.

### Anshuman Mehta — dataset engineering, EDA and research synthesis

**Inputs:** original dataset/graph files, provenance/checksums, corrected loaders/splits, supplied requirements; later the common prediction outputs.

**Tasks:**

1. Verify dataset source/version, fields, units, timestamps, sensors, graph alignment, measured channels, distribution rights/licensing and suitability. Compare alternatives sufficiently to justify a recommendation; owner accepts the selection.
2. Audit duplicate/missing timestamps, missingness by sensor/time, outage runs, invalid/implausible readings and any unexplained speed cap. Separate documented missing-value conventions from assumptions.
3. Investigate timezone/DST evidence. If unresolved, label clock-based features/slices provisional instead of silently interpreting timestamps as local time.
4. Produce training-focused EDA: speed distribution; missingness heatmap; outage-length distribution; weekday/weekend daily profiles; representative sensor traces; sensor map or appropriate network visual. Explain each figure and its modeling implication.
5. Document peak/off-peak definitions based on the agreed policy and training evidence. Comparisons across later partitions are descriptive audits, not a basis for tuning after test inspection.
6. After predictions exist, produce forecast-versus-actual traces, error-versus-horizon plots and congestion visualizations. Any congestion threshold/proxy needs an agreed, training-derived definition; speed proxies are not measured flow/density.
7. Edit the literature comparison table using contributions from all five members. Distinguish unread candidates from actually reviewed papers.

**Planned outputs:** dataset card, suitability matrix and recommendation, EDA report/figures, short finding register, literature synthesis table, report sections on data/EDA/related work.

**Acceptance:** every statistic/figure has an actual source or generation command; no invented channels/units; unresolved licensing/timezone questions remain visible; features/slice definitions do not arise from test optimization; outputs can be regenerated.

**Reviewer:** Rudraksh for data integrity; Kavya for research interpretation. **Theory to explain:** speed/flow/density/occupancy, missingness versus genuine observations, seasonality, spatial dependence, and dataset limitations. Measuring LWR wave speed is not required by this completion plan; speed alone does not directly identify flow/density or a calibrated LWR model.

### Vridhi Chaudhary — feature engineering and leakage tests

**Inputs:** agreed target/split/feature contract, validated data and sensor order, Anshuman's training EDA and missing-value findings.

**Tasks:**

1. Specify and implement per-sensor causal features: 12 speed lags; trailing mean/std/min/max; speed differences; cyclic time-of-day and day-of-week; weekend indicators; missingness flags/counts.
2. Keep sensor batches manageable instead of requiring one giant pooled feature table. Define stable anchor alignment and feature names/dtypes.
3. Implement the agreed causal input fill and training-only fallback, preserving missingness indicators. Missing targets remain masked.
4. Provide one shared feature interface to both model owners. Any training-fitted transformations must expose fit/transform boundaries and temporal-fold behavior.
5. Write meaningful synthetic tests: changing future speeds cannot change an earlier feature row; trailing windows have exact known values; feature/label alignment is correct; evaluation data cannot change fitted statistics; outage windows retain flags.
6. Support a small temporal-feature ablation if time permits: lags-only versus lags plus engineered temporal features, using the same estimator/settings and evaluation points. This is recommended evidence, not a generic faculty requirement for a particular ablation.

**Planned outputs:** reusable feature modules, feature schema/data dictionary, feature configuration, feature-generation script/interface, leakage/alignment tests and report feature section.

**Acceptance:** all features are available at forecast time; labels are shifted correctly; no centered/future rolling operations; fixed transformations fit on permitted training data; identical outputs for identical input/config; both model owners can consume the same schema.

**Reviewer:** Rudraksh; Bineet validates usability. **Theory to explain:** lags, causal rolling statistics, cyclic encodings, missingness indicators, target leakage and train-only fit/transform.

### Bineet Keshari — Random Forest and baseline comparison

**Inputs:** frozen feature schema and split/mask contracts, existing M0/M1 runners, common artifact writer/evaluator.

**Tasks:**

1. Keep existing M0/M1 baselines as reference runs. Document persistence's historical-average fallback and the information available to each method.
2. Proposed Random Forest design: one independent model per sensor, outputting the 12 horizons jointly. This is a multi-output temporal forecast per sensor, not a claim of network-aware learning.
3. Define training-row validity for multi-output labels before fitting. If rows with any missing future target are excluded, report removal rates per sensor and the likely training bias. Do not remove matching evaluation rows merely to improve comparison.
4. Benchmark a few sensors first, then implement the agreed coverage with bounded memory, reproducible seeds and a modest documented validation search. Do not use random observation cross-validation or OOB error as the final time-series estimate.
5. Save finite, aligned forecasts through the common writer. Agree and count fallback behavior for sensors lacking enough valid training rows.
6. Record validation selection, complete parameters, runtime/memory where measured, prediction artifacts, results and failure cases. Author the baseline/Random Forest report section.

**Planned outputs:** Random Forest module, training/prediction entry point, model configuration, model/missing-target tests, run records and baseline comparison explanation.

**Acceptance:** predictions cover the agreed common scoring grid; no future or target-derived inputs; label exclusions and fallbacks disclosed; tuning only uses allowed validation information; reproducible results and correct bagging/multi-output explanation. Better scores than M0/M1 are not assumed.

**Reviewer:** Vridhi for data/feature use; Kavya for model comparison. **Theory to explain:** decision trees, bagging, variance, hyperparameters, direct versus joint multi-step forecasting, and masked-target training choices.

### Kavya Katal — XGBoost, comparative interpretation and presentation

**Inputs:** the same feature/split/mask contract used by Random Forest, existing baselines, common artifact writer/evaluator and Anshuman's plots.

**Tasks:**

1. Proposed XGBoost design: independent per-sensor models, one direct model per horizon. Retaining 207 sensors and 12 horizons implies 2,484 estimators; measure a small pilot's runtime/memory before committing to that workload. If infeasible, propose a shared scope/interface revision rather than silently changing coverage.
2. Drop invalid training labels separately for each horizon; preserve the common evaluation target mask. Keep a predefined, counted fallback for sparse sensors.
3. Use a bounded, recorded validation search/early-stopping policy. Include the XGBoost dependency/version in the environment only when implementation is authorized; no test optimization.
4. Save predictions with the same sensor/anchor/horizon identity as the other methods. Record seed, full parameters, chosen iteration count, source/config/data identity and measured runtime.
5. Compare with Random Forest, M0 and M1 by horizon and traffic period. Explain failures and potential independent-segment limitations without claiming graph models would necessarily solve them. Feature importance may be used as exploratory association; it does not establish causation. SHAP is optional.
6. Author the XGBoost/results/discussion sections, assemble slides from everyone's material and coordinate contribution evidence and mock viva questions.

**Planned outputs:** XGBoost module and training entry point, configuration, label/alignment tests, run records, comparative interpretation and complete presentation.

**Acceptance:** validation-only model selection; finite aligned predictions; measured compute/coverage and fallback disclosure; no invented improvement claims; discussion grounded in observed errors; slides reproduce verified report numbers.

**Reviewer:** Bineet for model comparison; Rudraksh for evaluation integrity. **Theory to explain:** gradient boosting, objective/loss and regularization, hyperparameters, early stopping, direct horizons, and error interpretation.

## 5. Dependency order and checkpoints

### Gate A — documentation and decisions first

Rudraksh drafts traceability/evaluation contracts; Anshuman drafts dataset suitability and quality findings; Vridhi drafts the feature schema; Bineet/Kavya draft model plans and pilot budgets. All five review. Obtain owner acceptance where a real project decision is needed. No code/experiments begin merely because this plan has been written.

### Gate B — shared data/features

After implementation authorization, Vridhi builds the agreed feature pipeline; Rudraksh reviews leakage/alignment tests. Anshuman's EDA runs alongside the agreed training-only analysis. Model owners use tiny synthetic fixtures or documented development subsets until the shared interface passes review.

### Gate C — model pilots and runs

Bineet implements Random Forest; Kavya implements XGBoost. Review pilot compute and target-coverage records. Freeze the integrated source/configuration, regenerate common baseline/target artifacts, then run the approved learned-model comparisons. A change to the pipeline creates a new manifest/run, not mixed artifacts.

### Gate D — evaluation, explanation and submission

Rudraksh integrates verified results; Anshuman creates figures; each person authors their own report section and slides. Conduct cross-review, clean-environment reproduction and rotating mock vivas. Do not publish or push without the owner's subsequent instruction.

No deadline was supplied; the gates are dependency order, not promised dates or fabricated time estimates.

## 6. Shared report, literature and viva obligations

- Each member contributes verified literature notes relevant to their role. An optional planning target is two well-understood papers per person; it is not a faculty-prescribed count. The final review must synthesize methods, evidence, limitations and relevance rather than concatenate summaries.
- Report content: problem and scope; related work; data/provenance/EDA; causal feature design; models and mathematics; chronological protocol; reproducible results; discussion and limitations; contributions; references. Follow confirmed faculty formatting/length instructions when available.
- Every figure/table cites a real run or actual data analysis. Report learning failures and inconclusive findings. No graph-model comparison appears as an observed result until those models are authorized and tested.
- Everyone presents their own work and can explain the rest. Cross-review one other member's module; answer why random splitting is inappropriate, how horizons/masks work, why zeros need a policy, what the model learns, and what the results cannot establish.
- Understanding is verified by explanation and a small live demonstration, not by an arbitrary promised quiz score or a contribution table alone.

## 7. Final readiness checklist

- [ ] Relevant faculty requirements traced, ambiguities recorded and important project choices accepted by the owner.
- [ ] Dataset provenance, fields/units, quality limitations, rights/licensing and suitability documented with evidence.
- [ ] EDA complete, reproducible and used without test-driven selection.
- [ ] Shared causal feature pipeline implemented and leakage/alignment checks pass.
- [ ] Agreed learned ML model set implemented, understood and evaluated against M0/M1.
- [ ] Same evaluation grid/masks/horizons across methods; horizon and peak/off-peak comparisons included.
- [ ] Model/tuning settings, compute, removed training labels, fallbacks and test exposure disclosed.
- [ ] Forecast/error/congestion visualizations produced with justified definitions and source artifacts.
- [ ] Literature review and theoretical explanations complete and correctly referenced.
- [ ] Clean-environment reproduction, relevant tests and CI verified; results traceable to code/config/data.
- [ ] LaTeX/IEEE report compiles; slides agree with report and contain contributions and limitations.
- [ ] Every student can explain and demonstrate the full project and their own genuine contribution.

These checkboxes are intentionally unchecked: this is the remaining-work plan. UI, GAT, deep learning, a hybrid stacker, SUMO and real-world traffic control are not completion requirements in this plan. Signal-control scope remains simulated-only future work.
