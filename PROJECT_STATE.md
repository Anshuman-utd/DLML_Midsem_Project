# Project state

## Submission-folder simplification — 2026-11-19

The owner found multiple report/deck versions confusing. Retired Phase 1/2 report/deck alternatives were byte-verified and moved completely outside the repository. Current LaTeX build inputs are under docs/latex/phase2/. report/phase2/ now contains only one report PDF and README; slides/phase2/ contains one PPTX and its PDF preview plus README. No model, scores or final submission bytes changed. Historical draft generators now use ignored results/report_drafts/phase2/, preventing retired folders from being recreated.

Previous cleanup commit fa7da95 is on origin/kavya but was still not merged into origin/main when checked; GitHub’s default branch therefore still shows the older layout. The owner approved committing and pushing this further simplification to kavya on November 19. Main remains unchanged until the owner merges the PR. See docs/DELIVERABLES_LAYOUT.json for the archive/relocation chain.

## Artifact organization and preview — 2026-11-18

PR #14 from Rudraksh is merged at eaa4eee. Latest nine-page report and fourteen-slide deck are grouped under report/phase2/ and slides/phase2/; Phase 1 artifacts live under their corresponding phase1/ directories. Old alternatives/original uploads are archived with exact relocation hashes. Three charts received valid-positive-axis-ID and negligible numeric-cache serialization repairs; slide/notes/workbook content is preserved. An exact repaired-deck PDF preview and local slide viewer are available. No training/score/hybrid project changes or publication. See docs/DELIVERABLES_REVIEW_20261118.md and report/README.md / slides/README.md. The owner approved committing and pushing this reviewed organization on kavya. It is prepared as a scoped branch commit; main changes only through owner-reviewed PR/merge. Older verification/publication-status records below retain their historical meaning.

## Combined team integration — 2026-11-17

Fetched canonical origin/main at 4dc98e2 after owner-merged PRs #9–#12, preserved all 142 pre-sync local delta files outside the repo, and fast-forwarded kavya. Kept completed member logs and the neural test import/fixture correction. All other incoming source/artifact bytes match the prepared reference. Kavya's package supplies evaluation/inference, CI/environment protections, frozen small evidence and shared documentation, with genuine coordinator review recorded separately.

Fresh combined checks: 76 tests passed in 3.41 seconds, no skips; Ruff lint/format 51 files passed; 59 dependencies compatible; raw data/graph validated; graph and temporal checkpoint CSV inference succeeded. A fresh 40-run synthetic simulation reproduces original metric/summary/paired CSV bytes exactly; all fresh trajectory hashes verify. Rebuilt wheel imports neural/control outside checkout and passes a physical update. LaTeX source compiles; report/PPTX hashes match the previously visually reviewed final files, both below 10 MB. Phase 1 source/data and neural source/checkpoints/scores remain unchanged. No retraining or test tuning.

Prepared scoped local commits remain on kavya; nothing is pushed and no PR/form is created by this integration. The four member PRs are already remote history; their historical partial-check failures are preserved and resolved by the assembled suite, not misreported as new passes. Individual understanding/faculty acceptance remains unestablished. See verification/phase2-integration-20261117/ and docs/handoffs/phase2/05-kavya-integration/REVIEW_LOG.md.

Below is the preserved pre-merge November 16 record. Its local-only status is superseded above.

## Final local Phase 2 extension — 2026-11-16

The owner requested completing remaining submission work after checking LWR/control requirements, keeping viva simple and pushing nothing. Renewed local/Gmail/Drive searches found generic faculty instructions and planning sources, but not the original Project4 technical brief. See docs/PHASE2_REQUIREMENTS_FINAL_AUDIT.md. The owner subsequently confirmed that no specific brief is available; no mandatory simulator/MARL requirement is invented.

Added a conservative synthetic eight-cell LWR/CTM corridor and two local rule-based signal agents. Forty runs compare responsive and equal-green fixed-time policies over four predefined scenarios and five paired seeds. Physics, arrival rates and control rules were recorded before outcomes. Invariants enforce conservation, CFL, jam bounds, red gating and sending/receiving limits. Responsive system vehicle-time is lower in all four scenario means; fixed time is not demand-optimized and residual vehicles are retained. The simulation is not calibrated LA traffic, MARL or GAT-driven control. It is a separate illustration, not an end-to-end learned traffic controller.

Frozen forecasting results, checkpoints, source/data identity and exposed-test caveats are preserved. Fresh assembled suite: 76 tests passed in 2.40 seconds (latest final run), no skips; Ruff lint/format for 51 files passed. Rebuilt wheel imports simulation/neural modules outside checkout; a real observed-history checkpoint CLI forecast ran again. Current report includes synthetic equations/results/limits and current checks; deck remains six editable slides. Updated artifacts now occupy the local final paths after visual review; previous November13 report/source/figures/deck are preserved in the private Phase2_Submission/history/pre-control-2026-11-16 archive. Dated November13 evidence remains historical, not a fresh check.

Everything is local/uncommitted on kavya. No push, PR, merge or form submission was performed. Five Phase 2 handoff ZIPs have been prepared locally under the subsequent owner request; see docs/handoffs/phase2/. Code/data binaries/private builds remain excluded from Git. Human review/understanding, any original faculty-specific requirements, later publication and the one-time university-email submission remain separate owner actions. Final verification and artifact hashes are in verification/phase2-final-20261116/.

Below is the preserved November13 forecasting-only verification record. Its no-controller status and old artifact sizes are superseded by the November16 extension above.

## Phase 2 local verification — 2026-11-13

The owner-authorized forecasting extension is implemented, trained and evaluated locally on `kavya`. It includes shared GRU, GRU+GAT, self-only/uniform/no-dropout controls, validation-only optional hybrid, standalone observed-history inference, tests, learning notes, a five-page IEEE-style LaTeX/PDF report and six-slide editable PPTX. Thirteen unique complete fits include four learning-rate candidates; eleven selected/control fits were evaluated. No publication, new commit, PR, form submission or member ZIP was performed in this phase.

Measured exploratory 60-minute MAE: temporal GRU 4.929, graph GRU 4.881, self-only 4.931, XGBoost 3.874 mph. Graph modestly improves its neural controls but does not surpass the tree baselines. RF retains the best main-method RMSE; the blend selected pure XGBoost. No-dropout improves seed 42 graph MAE, with single-seed limits. See docs/PHASE2_RESULTS.md and verification/phase2-20261112/.

Verification: all 69 tests passed in 2.71 seconds with real data available and no skips, using OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1. Ruff lint/format passed for 44 Python files; uv checked 59 compatible installed packages. A rebuilt wheel imported neural modules outside the checkout. Every checkpoint reload reproduced exactly; observed-history CSV inference passed its documented tolerance. Historical baseline targets, source/data identity and all 720 historical metric rows matched. All 31 original Phase 1 source/config hashes remain unchanged. All 5 final PDF pages and 6 slides rendered from the exact final PPTX were visually inspected. PPTX package/native chart/table/font/import gates passed. Native PowerPoint execution and remote CI are not claimed.

Host memory pressure prompted a storage-only amendment: phase2-v2 constructs batches rather than retain a 681 MB history cache. All 34,249 histories were bitwise equal and normalization unchanged. Five completed fits retain parent/checkpoint lineage; the unfinished candidate restarted from its seed and reproduced first-epoch losses exactly. An in-memory self-only fit was suspended/resumed for 581 seconds to avoid duplicate scheduling, retaining its optimizer state. Timing includes contention and pauses. Source snapshots, equivalence, lineage and scheduling records remain in the evidence.

Final local artifacts: report/phase2/T072_Phase2_Report.pdf (421,704 bytes), slides/phase2/T072_Phase2.pptx (98,803 bytes); both below 10 MB. Old Phase 1 report/slides remain unchanged. Datasets, model binaries, predictions, environments and private slide-build files remain excluded from Git. The raw files and original Downloads/AML were preserved.

The original project-specific faculty brief remains unlocated. The generic DL rubric and supplied deadline email guide this study; calibrated LWR, multi-agent control and full title compliance are not established. The old test remains exploratory; timezone/raw-data rights and genuine member understanding remain unresolved. Final owner review, faculty-scope confirmation, member review/rehearsal, later ZIP handoffs/publication and the one-time university-email submission remain pending.

Below is the preserved October28 state. Its Phase 2 deferral was superseded by the November12 owner request.

Updated: 2026-10-28, Asia/Kolkata. Team T072, Section C.

## Current branch and integration

PRs #2–#6 are merged in canonical `main` at `b717675973aa32f966d7d38f177d08087013177c`. The owner authorized uploading the selected final report and presentation on 2026-10-28. Branch `kavya` was fast-forwarded to that main base before adding the three supplied binary artifacts and their documentation. New commits use Kavya Katal's configured identity without a co-author trailer. Publication is to the personal branch for review; no direct-main commit, direct-main push or merge is performed.

The supplied report has 17 pages, and the supplied presentation/PDF export have 8 slides/pages. Their original bytes are preserved under `report/final/` and `slides/final/`. The presentation's RMSE table and pilot-candidate labels disagree with the frozen evidence; see [correct values and import checks](docs/final_deliverables.md). Do not mark these numerical issues or final-submission acceptance resolved. Existing sources, generated results/provenance and contribution history are preserved.

The canonical project is this repository ROOT: src/trafficml/, scripts/, tests/, configs/, report/, slides/ and verification/. There is no nested AML/. Original Downloads/AML is unchanged. Delivery ZIPs/extractions, historical placeholders, unused data and private build files remain in the separate sibling DLML_Project_Archive_2026-10-27 archive; they are not submitted.

## Integrated implementation

Package 05 supplies the remaining pinned environment, model config, training/evaluation/prediction/report runners, CI, integrity/metric tests, small experiment evidence, literature/methods/contribution notes, IEEE source and 11-slide deck. At intake, every remaining Git-visible local file belonged to that package; newer shared docs were preserved. Added [requirements mapping](docs/02_requirements_traceability.md), truthful [Kavya review](docs/handoffs/05-kavya-integration/REVIEW_LOG.md) and [integration evidence](verification/integration-20261027/README.md). Corrected the deferred interpretations in member review logs without altering runtime code, scores or their historical check reports.

The study compares persistence, historical average, independent-sensor multi-output RF and direct-horizon XGBoost with 38 causal features, bounded validation-only tuning, training stride 2, purged chronology, common masked targets, EDA/error analysis and saved-model inference. No GAT, calibrated LWR, UI, stacking or traffic-signal simulation is implemented. Phase 2 remains deferred; any future control is simulated only.

## Recorded implementation verification — 2026-10-27

Full real-data suite: 56 passed without skips. Ruff lint/format passed for 37 Python files; uv checked 52 compatible installed packages. A wheel built offline with setuptools. The existing uv-created verification environment has no pip module, so the initial pip check/build attempts failed; alternative actual checks succeeded.

Real-data loading confirms 207 sensors, 34,272 five-minute timestamps, graph ordering/reference adjacency, 1,515 directed edges, 8.11% missing and split counts 23963/1701/1702/6850. Saved-model prediction loads and reproduces the working historical demo after validating unchanged source/config/data identity. The IEEE source compiled at its canonical root location. Previous rendered-slide inspection is preserved as historical evidence; no native PowerPoint test is claimed. A clean Git-tracked export passed 54 tests with two real-data skips, lint/format and all eight CLI import checks using the existing verified dependencies. The wheel imported outside the checkout; frozen runtime source hashes matched. The source snapshot is recorded in verification/integration-20261027/checks.json. No remote CI result is claimed before publication.

## Existing results and limits

The frozen full run remains local at results/runs/phase1-full-v1 with measured small evidence under verification/full-phase1-20261026/. XGBoost exploratory test MAE at 15/30/60 minutes is 2.9205 / 3.3764 / 3.8737, 16.1% / 19.1% / 27.2% below persistence. RF has lower headline RMSE. These are regression errors, not classification accuracy. The raw XGBoost tensor retains 24 negative predictions out of 17,015,400; no silent clipping or retuning occurred.

Original implementation and substantial owner/AI assistance remain disclosed. Member PR imports and agent reviews do not prove independent student authorship or understanding. See docs/CONTRIBUTIONS.md.

## Gates before final locking/submission

Review the integration PR and actual CI, export/inspect the final PDF, rehearse slides/viva, verify allowed assistance and genuine member contributions, and clarify project-specific flow/LWR scope versus speed-only Phase 1. Raw-data redistribution/timezone remain unresolved; the exposed test remains exploratory. Do not certify these gates from passing code checks alone. Data/models/predictions/environments/bundles remain excluded from Git.
