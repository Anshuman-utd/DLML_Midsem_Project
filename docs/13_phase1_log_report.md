# Phase 1 technical log and proposed team handoff register

Team T072, Section C. Registered: **2026-10-27**, Asia/Kolkata.
Retrospective reporting window: **2026-10-21 through 2026-10-27** (seven calendar dates).

This report summarizes existing project records. Event dates and registration dates are separate: this report was registered on 27 October, not backdated. Proposed owners below are responsible for subsequent study, reproduction, review and actual improvements; they are not claimed as the original authors of existing implementation. The integrated extension was prepared by the owner with substantial AI assistance, building on the teammate prototype. See [contribution disclosure](../AML/docs/CONTRIBUTIONS.md).

## 1. Requirements and scope

The supplied faculty instructions require Phase 1 ML literature review, dataset quality/EDA, feature engineering, theoretical rigor, model application, repository/code quality, presentation, individual viva and a LaTeX/IEEE report. Phase 2 covers DL architecture, DL literature, regularization, ablation studies and technical validation, with the shared submission components. A technically justified ML-DL hybrid can earn additional marks in Phase 2.

The implemented Phase 1 objective is future traffic **speed regression**. No GAT, calibrated LWR model or traffic-signal simulation has been implemented. The broader allocated title's flow/control expectations still need faculty clarification. Any future signal control is simulated only.

Source: [faculty instructions](../AML/CSAI_Project_Instructions_Phase_1_and_Phase_2.pdf).

## 2. Retrospective event register

All entries below were registered in this report on **2026-10-27**. Dates describe existing records, not newly assigned student activity.

| Log | Event date | Recorded event | Evidence/status |
| --- | --- | --- | --- |
| W01 | 2026-10-21 | No dated activity verified in available records | Do not infer work from the start of the reporting window |
| W02 | 2026-10-22 | Initial scaffold and documentation placeholders | Existing [worklog](../logs/worklog.md); no implementation at this stage |
| W03 | 2026-10-23 | No dated activity verified in available records | Individual activity unconfirmed |
| W04 | 2026-10-24 | No dated activity verified in available records | Individual activity unconfirmed |
| W05 | 2026-10-25 | Prototype review and corrections: split boundaries, artifacts, reproducibility and baseline checks | Existing worklog and [correction evidence](../AML/verification/correction-20261025/README.md) |
| W06 | 2026-10-26 | Integrated Phase 1 implementation, full-sensor experiment, EDA, evaluation, report source and slides | Existing worklog and [full-run evidence](../AML/verification/full-phase1-20261026/README.md); 56 tests recorded as passing |
| W07 | 2026-10-27 | Readiness review, technical explanation and this retrospective log/team handoff proposal | This report; no new training or member completion claimed |

Exact individual work dates should be added only when supported by a member's real work and evidence. Unknown dates remain unknown; historical team events do not establish which member performed them.

## 3. Technical work register

Registered 2026-10-27. Implementation statuses below come from the recorded full run, not a new execution today. Named review owners are proposed in section 5.

| ID | Area | Verified implementation/evidence | Remaining review |
| --- | --- | --- | --- |
| D01 | Dataset | METR-LA, 34,272 timestamps x 207 sensors, five-minute readings, 2012-03-01 to 2012-06-27; speed only | Confirm suitability against the project-specific brief; timezone and raw-data rights unresolved |
| D02 | Loading | Shape, timestamp order/frequency, sensor ordering, adjacency alignment and checksums checked; full run used all sensors | Independently reproduce loader checks and explain missing-value convention |
| D03 | Quality | Missing fraction 8.11% overall, 7.13% in training; longest detected missing run 5,800 minutes | Explain long outages and limits of input substitution; no claim gaps are repaired measurements |
| E01 | Distribution EDA | Training speed histogram, missingness visualization and outage-length histogram | Summarize ranges and affected sensors with evidence |
| E02 | Pattern EDA | Weekday/weekend daily profile, first-day sensor-speed heatmap and sensor-location scatter | Explain recurring patterns and spatial/time variation; graph not used by current predictors |
| F01 | Input preparation | Causal forward fill within history, then training-only median for leading gaps; original missingness retained as flags | Verify no backward fill or future information; targets never imputed |
| F02 | Feature creation | 38 features: 12 speeds, 12 missingness flags, six rolling statistics, three change/missing-fraction features and five calendar features | Explain each group and its rationale |
| F03 | Feature selection | All 38 retained; model feature-importance table generated | No formal selection or feature-group ablation completed; importance is not causal proof |
| V01 | Validation | Chronological partitions; 11-anchor boundary purge; training-only preprocessing; stride-two model training | Explain why random time splits are unsuitable; disclose different RF/XGB valid-label rules |
| M01 | Baselines | Persistence and training-only historical average | Reproduce one forecast by hand and inspect all-missing history fallback |
| M02 | Random Forest | One multi-output forest per sensor, jointly predicting 12 horizons | Explain bagging, joint-label exclusion and selected parameters |
| M03 | XGBoost | One direct regressor per sensor/horizon; selected absolute-error objective | Explain boosting, horizon-specific label masks and selected parameters |
| M04 | Tuning | Two candidates per learned family on six pilot sensors, selected using val_tune only | Small budgeted search; no global-optimum or test-tuning claim |
| R01 | Evaluation | Common valid targets; MAE/RMSE/MAPE; 12 horizons; peak/off-peak and weekday/weekend slices; per-sensor errors | Test interval previously inspected, so comparisons remain exploratory |
| R02 | Model limitations | 24 negative raw XGBoost test predictions out of 17,015,400; retained in scores | Any physical-output policy must be declared and revalidated, not silently added |
| Q01 | Verification | 56 tests passed in recorded run; source hashes, saved-model reload checks, lint and dependency checks recorded | Each reviewer must record their own actual rerun separately |
| S01 | Deliverables | IEEE source compiled; 11-slide deck rendered/inspected; source ZIP created | Final PDF export/layout check, fresh-extraction reproduction and faculty requirement mapping remain |

EDA helps justify handling and feature choices; no experiment isolates the performance gain from each individual preprocessing or feature group. No scaling was used for tree models. No synthetic data, future-value interpolation or target imputation is claimed.

Sources: [dataset audit](../AML/verification/full-phase1-20261026/analysis/dataset_audit.json), [methods](../AML/docs/METHODS_AND_VIVA.md), [analysis artifacts](../AML/verification/full-phase1-20261026/analysis/), [training records](../AML/verification/full-phase1-20261026/training_records.json).

## 4. Recorded exploratory test results

Each cell is **MAE / RMSE / MAPE%**. MAE and RMSE are speed errors, reported in mph following the benchmark description. Lower is better; these are not classification accuracy percentages.

| Method | 15 minutes | 30 minutes | 60 minutes |
| --- | --- | --- | --- |
| Persistence | 3.48 / 6.37 / 8.57 | 4.17 / 7.98 / 10.77 | 5.32 / 10.25 / 14.39 |
| Historical average | 4.19 / 7.85 / 13.03 | 4.19 / 7.85 / 13.03 | 4.19 / 7.85 / 13.03 |
| Random Forest | 2.97 / 5.44 / 8.07 | 3.42 / 6.37 / 9.81 | 3.90 / 7.25 / 11.71 |
| XGBoost | 2.92 / 5.78 / 8.04 | 3.38 / 6.91 / 10.06 | 3.87 / 7.99 / 12.59 |

XGBoost has the lowest pooled headline MAE, improving over persistence by 16.1%, 19.1% and 27.2%. RF has lower headline RMSE and better MAPE at 30/60 minutes. No universal winner is claimed. Source: [metric CSV](../AML/verification/full-phase1-20261026/tables/metrics_test.csv).

## 5. Suggested five-member allocation

**Proposed handoff assignments registered 2026-10-27; member acceptance and completion are pending.** This revises the earlier suggested allocation for this handoff only. It does not rewrite historical contributions.

Two data owners + two EDA owners + two model owners = six responsibility slots across five people. Bineet bridges EDA/error analysis and RF; his EDA scope is bounded to balance the extra model responsibility. Kavya coordinates integration and the report.

| Member | Proposed role | Review ownership | Concrete handoff output |
| --- | --- | --- | --- |
| Rudraksh Sharma | Dataset acquisition/provenance and loader validation | D01-D02; review Vridhi's input/target policy | Dataset source/scope note, independently recorded loader checks and unresolved metadata list |
| Vridhi Chaudhary | Dataset cleaning, temporal splits and feature engineering | D03, F01-F03, V01; review Rudraksh's loader evidence | Missing-data/split audit, 38-feature explanation and genuine test/review improvements |
| Anshuman Mehta | Primary EDA and visual interpretation | E01-E02; review Bineet's error interpretation | Captioned EDA summary: distributions, missingness/outages, weekday/weekend profiles, heatmap and locations |
| Bineet Keshari | Secondary EDA/error analysis + Random Forest/baselines | M01-M02, RF part of M04, per-sensor/period analysis in R01; review Kavya's comparisons | RF/baseline reproduction note, peak/per-sensor error interpretation and actual model/test improvements |
| Kavya Katal | XGBoost, comparison, reproducibility and submission integration | M03, XGB part of M04, R02, Q01, S01; review RF and assemble report | XGB reproduction note, common-target metric comparison, limitations and submission readiness register |

### Inputs, dependencies and acceptance criteria

| Member | Inputs/dependencies | Acceptance and verification |
| --- | --- | --- |
| Rudraksh | Existing raw data, loader, dataset card and manifest | Confirm shape/time frequency/sensor order against evidence; explain speed-only scope and avoid unverified licensing claims. Evidence: loader outputs plus actual date and source identity |
| Vridhi | Rudraksh's verified loader output; masking/split/feature modules | Demonstrate a history window and its 38 features, training-only fallback and purge boundary; run relevant data/split/feature checks and record actual outcomes |
| Anshuman | Verified training interval, dataset audit and analysis figures | Give a finding and practical implication for each EDA figure; keep test error plots distinct from training EDA; identify unresolved timezone and long-outage issues |
| Bineet | Validated features/splits, training config and saved RF/baseline evidence | Reproduce saved RF/baseline predictions or a bounded rerun; explain masks, bagging, peak errors and why RF RMSE can beat XGB despite higher MAE |
| Kavya | Common targets/config plus both model owners' reviewed evidence | Reproduce XGB inference and metric table, explain MAE/RMSE tradeoff and exposed-test limitation; verify final report/package checklist without claiming unresolved items complete |

Relevant implementation locations: [data](../AML/src/trafficml/data/), [features](../AML/src/trafficml/features/temporal.py), [trees](../AML/src/trafficml/models/trees.py), [baselines](../AML/src/trafficml/models/baselines.py), [analysis script](../AML/scripts/build_analysis.py), [evaluation](../AML/src/trafficml/eval/), [tests](../AML/tests/).

Every member also supplies verified literature notes, their own report subsection, a short presentation explanation and a cross-review. All five must understand the complete pipeline. Scope is reproduction/review and genuine improvements, not repartitioning existing files to imply authorship.

## 6. Suggested review sequence

These are relative working sessions **after handoff**, not claimed dates in the retrospective week. Record actual dates when the work occurs.

1. Session 1: Rudraksh/Vridhi verify data and preprocessing; others study their modules in parallel.
2. Session 2: Anshuman/Bineet review EDA and error slices; data owners answer quality questions.
3. Session 3: Bineet/Kavya reproduce model inference/evaluation and explain tuning choices.
4. Session 4: Cross-review, integrate genuine changes, inspect final report/package and hold a five-person mock viva.

## 7. Individual activity registration template

Append one entry per actual activity. Do not prefill historical dates, hours, test results, commits or completion signatures.

| Field | Required entry |
| --- | --- |
| Activity ID | Unique identifier |
| Member | Person who actually performed the activity |
| Performed on | Actual date/time, or explicitly unknown if retrospective |
| Registered on | Actual date/time when entered |
| Category | Data / EDA / features / models / evaluation / documentation |
| Work and purpose | Specific reproduction, review, correction, analysis or implementation |
| Inputs and identity | File paths, config and commit/hash where available |
| Output/evidence | Notes, changed files, command output, run artifact or review comments |
| Verification | Actual command/check, result and limitations |
| Assistance | Existing code reused and relevant human/AI assistance |
| Reviewer/status | Named reviewer after real review; pending until then |

No new training, commits, pushes or publication were performed to prepare this report. The original Downloads copy is preserved. Existing source ZIP and standalone sandbox have not been refreshed with this new documentation.
