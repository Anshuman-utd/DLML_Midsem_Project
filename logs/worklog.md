# Worklog

## 2026-10-27 — Repair inconsistent team coordination baseline

Team messages reported that canonical remote main at 6e611d6 still instructed agents to wait for a nonexistent integration branch, reject main-repository root imports and avoid member PR publication. Those blockers were caused by stale coordinator instructions, not member error. Replaced the active AGENTS.md and common handoff/prompt with one current contract: canonical KatalKavya96/DLML_Midsem_Project; base/PR target main; personal codex/ branches; no integration prerequisite; direct root payload import; member personal-branch/fork PR publication authorized by the owner's shared group instructions; no main pushes or merges. Newer shared instruction/state/ignore files must survive import of stale package copies. Added empty root layout markers so a coordination-only clone can identify the intended structure before module PRs. Prepared a shared-instructions/scaffold-cleanup commit, excluding member runtime source, pyproject dependency implementation, model code, tests/configuration and academic artifacts. The owner's local full reference remains separate from a published coordination-only baseline. Publication by this coordinator still requires owner direction; no push/PR performed during preparation.

## 2026-10-27 — Canonical root consolidation and dependency/artifact hygiene

The owner requested one main project folder and separation of irrelevant folders. Moved the extended working AML implementation into the DLML_Midsem_Project repository root, merging compatible scaffold directories and preserving source/data/config bytes. Nested AML/ no longer exists. Preserved pre-consolidation tracked files and overwritten root documents, unused initial scaffold modules/placeholders, delivery archives/extractions, private slide authoring files, old result layouts/runs and unused PEMS-BAY data in the sibling Desktop/DLML_Project_Archive_2026-10-27 folder. Its MOVE_MANIFEST.json records 76 moves/link updates. Original Downloads/AML and Git history were not changed. Updated the existing Desktop sandbox run symlink to the new saved-run location.

Updated active root README, state, roster status, contributing instructions, handoff guidance and current documentation links. The package inventories now apply at the root with no AML/ prefix. Preserved historical command strings/manifests as provenance. New ignore rules exclude node_modules, dependency caches, delivery archives, root saved runs, model binaries and private build files. No node_modules directory was found in the active tree; large private authoring dependencies were moved with the archived build folder. Existing tracked scaffold removals are intentional relocations into the archive, not lost work.

Verification after the move: PYTHONPATH=src /tmp/aml-repair-env/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/dlml-root-layout-tests reported 56 passed in 2.36 seconds. Ruff lint and formatting checks passed for 37 Python files. scripts/check_data.py confirmed 207 sensors, reference adjacency equality, 1,515 directed edges, 34,272 timestamps, 8.11% missing and retained split counts 23963/1701/1702/6850. scripts/predict.py successfully validated the unchanged run source/config/data identity and loaded saved RF/XGB estimators for the latest sensor-773869 forecast. Current-document links resolved; six ignore probes passed; no untracked Git-visible data/model/dependency/archive files were found. No retraining, new results claim, Git commit, push, PR or member-authorship assignment was performed during consolidation. The existing 6e611d6 shared-documentation commit remains the latest commit; layout/source changes are local and uncommitted.

## 2026-10-27 — Shared documentation commit preparation

The owner requested committing changes needed to coordinate the other agents. Prepared an explicit shared-documentation/configuration allowlist: root instructions/state/ignore policy, team plans/log report, documentation index, experiment/finding/issue/work registers and handoff workflow/prompt/ownership map. Excluded member-assigned AML source, delivery packages, datasets, models and temporary chart files. Added ignore rules for local delivery archives/extractions and private chart scratch files without deleting them. Verified the configured Git identity is Kavya Katal, the index initially has no staged changes, the source ownership map covers all 118 distinct payload/review paths, and the shared prompt matches the packaged commit-only prompt. This entry records preparation; the actual commit result is verified separately. No push or member-authorship reassignment is authorized.

## 2026-10-27 — Self-contained context and commit-only instructions

Updated all five member ZIPs at the owner's request: added 24 read-only context files per ZIP (standalone instructions/state/setup/plan/corrections, methods/dataset/literature/contribution/checklist/evidence/config context, owner roster/role context and full file-ownership map). Added AGENT_PROMPT.txt and context/instruction SHA-256 manifests. Replaced earlier push/PR instructions with assigned local commits only; owner handles pushing. Instructions require existing staged-work protection, explicit inventory staging, personal codex/ branches, true identity/dates, actual agent review versus pending human understanding and no remote writes. Source payloads and original per-person allowlists are unchanged. Verified all five ZIP CRCs, all payload/context/instruction hashes, exact inventory agreement, no overlapping payload paths and byte-exact reconstruction of 113 source files plus five pending logs. No implementation edits, training, Git commits, pushes or PRs performed.

## 2026-10-27 — Five prepared module handoff ZIPs

Created deliverables/member-handoffs with separate Rudraksh data, Vridhi preprocessing/features, Anshuman EDA, Bineet shared estimators/error-analysis and Kavya configuration/evaluation/integration ZIPs. Used the existing curated source archive whitelist and current AML source, omitting four private .chart-data-* scratch files from the old archive. Original archive preserved. Each package contains unique payload paths, an exact staging inventory, SHA-256 manifest, shared integration instructions, provenance disclosure and a pending member review log. Shared trees.py is owned once by Bineet and requires Kavya's XGBoost review; no conflicting duplicated model code. Dataset/model/environment files excluded as in the source archive. ZIP CRC, every payload SHA-256, absence of overlapping paths and exact reconstruction of all 113 source files passed; five new pending review templates are additional. No model tests/training rerun or member participation claimed, no fabricated commit authors/dates, and no commits/pushes performed. Target layout is the standalone sandbox-style repository root; owner confirms destination before team publication.

## 2026-10-27 — Retrospective technical report and proposed handoff

At the owner's request, created docs/13_phase1_log_report.md with Phase 1/2 scope, dataset/loading/EDA/preprocessing/features, recorded model metrics and a proposed five-member allocation. The seven-date reporting window is 21-27 October; all entries in the new report were registered on 27 October. Existing dated project events are referenced; unverified dates and individual work are not invented. Proposed allocation is two data owners, two EDA owners and two model owners, with Bineet spanning error analysis and RF. Added inputs, dependencies, outputs, acceptance/review criteria and a truthful individual activity template. Updated the documentation index, contribution proposal and state. Checked all new report links, five-member coverage, whitespace and git diff --check successfully. No code, training, commit or push; existing ZIP and standalone sandbox were not updated.

## 2026-10-22 — Initial scaffold

### Objective and authorization

Create the entire requested repository structure with `.gitkeep` files and push this initial scaffold only. The owner explicitly authorized this exception to the earlier local-only instruction.

### Starting state

Branch `main`, commit `4897bfa` (Initialisation), clean working tree. Existing files: AGENTS.md, PROJECT_STATE.md, PROJECT.md. Preserved the existing roster, including the owner's updated name for Rudraksh Sharma.

### Work performed

Created the requested directories, short documentation drafts/placeholders, logs, proposed ADR-001, nested READMEs, `.gitignore`, `.gitattributes`, and a comment-only pyproject.toml. Updated the current scope to record this push authorization. No Python implementation, dependency installation, datasets, experiments, or accepted methodological choices.

### Verification and publication

Ran a Python scaffold check: 35 internal Markdown links resolved, all 8 `.gitkeep` placeholders exist and are trackable, and 7 data/secret/artifact ignore probes passed. `git diff --check` passed for tracked changes. The first `git add --dry-run .` attempt was blocked by sandbox access to `.git/index.lock`; `git add --dry-run .` then succeeded with the required Git metadata access and listed the intended scaffold files. No implementation tests apply to this scaffold. Publication is pending the commit/push result returned to the owner; this pre-publication entry does not claim a successful push.

### Remaining work

Expand substantive initial documentation when directed. Clarify the project title/LWR scope and define member responsibilities before implementation. Full documentation is not marked complete.


## 2026-10-25 — Teammate review and sandbox corrections

Reviewed the Downloads AML prototype against the supplied master instructions and generic faculty PDF. Identified split-boundary leakage, stale prediction acceptance, non-finite forecast acceptance, environment reproducibility gaps, and unconfirmed decisions presented as settled. Preserved the Downloads original and legacy results; made corrections in the workspace AML copy.

Added purged splits, regression tests, finite/alignment/fingerprint validation, immutable targets, run manifests, dependency pins, setup instructions, historical plan preservation, and proposal/status corrections. Explained that a UI was not required by the available rubric, and authorized publication to DLML-sandbox. A basic CI workflow is included but its remote result is not pre-claimed.

Verified 51 tests with the actual supplied local data, Ruff checks, dependency compatibility, data shape/frequency/sensor order/adjacency, and all existing baseline split generation plus validation/test evaluation. See AML/CORRECTIONS.md and AML/verification/ for exact commands and evidence. No additional models, EDA, or Phase 2 work was implemented. No project decisions were accepted. The original project remote is unchanged; sandbox push status follows actual execution.

Publication result: successfully pushed standalone sandbox commit `a 020778` to `KatalKavya96/DLML-sandbox/main`. Export checks: 49 passed, 2 real-data skips; lint/format passed. Source/data/environment separation verified before staging. No raw data, environments, generated prediction arrays, or legacy results were published.


## 2026-10-26 — Phase 1 completion plan and work allocation

### Objective

Respond to the owner's request for exactly what remains for Phase 1 and divide that work among all five members.

### Work performed

Inspected current instructions/state, prototype plan/configuration, prediction contract and baseline runner, and the supplied master instruction's requirements. Wrote docs/12_phase1_completion_plan.md with completion evidence, scope boundaries, shared interfaces, five task cards, review responsibilities, dependency gates and readiness checklist. Updated docs/11_team_contributions.md and docs/README.md. Refreshed PROJECT_STATE.md as a current snapshot and recorded planning-only authorization in AGENTS.md.

### Reasoning and limits

Recommended Random Forest and XGBoost alongside the two existing baselines; did not turn those suggestions into faculty requirements or accepted choices. Explicitly covered the existing 12-horizon artifact contract, per-sensor compute pilot, identical evaluation masks, already-inspected test set and source-manifest compatibility. No new implementation, EDA, model training, installation or push was performed. Member availability/acceptance and methodological approval remain open.

### Verification

Python document checks passed: 24 internal links resolved, all five member task cards are present, and checked documents are nonempty with no trailing whitespace. `git diff --check` also passed. No implementation tests are needed for this documentation-only change.

### Next action

Owner/team review of Gate A before further implementation; see the completion plan and contribution framework.


## 2026-10-26 — Integrated-first delivery preference

The owner proposed completing the integrated Phase 1 work together before distributing parts to members for their commits. Updated the completion plan, contribution framework, state and agent instructions to record this sequence. Module handoffs must include explanation, reproduction and real follow-up work; commit attribution must reflect actual contributions, not retroactive or impersonated authorship. This session changed planning documents only; no implementation, experiment, commit or push was performed. Verified modified document links and whitespace.


## 2026-10-26 — End-to-end Phase 1 implementation

### Authorization and scope

The owner explicitly requested completing the local Phase 1 project with simple methods and improved measured forecasting performance. Implemented a real independent-sensor study while preserving honest results/assistance attribution. Did not fabricate member commits or contributions, start Phase 2, or push any repository.

### Work performed

Added causal per-sensor features; RF/XGBoost training with explicit target masks/fallbacks; a two-candidate, six-sensor validation pilot; all-207-sensor fitting with training stride 2; saved estimator inference; run-all orchestration; EDA/error figures; factual result-table generation; dataset/literature/methods/viva/contribution notes; IEEE LaTeX source; editable native-chart slides; and a source/report ZIP. Preserved the Downloads original and old baseline artifacts. Updated the clean Desktop sandbox source/environment locally and linked its completed run to avoid duplicating 1.2 GB.

### Actual commands and results

Installed pinned sklearn 1.7.2, XGBoost 3.1.1 and Matplotlib 3.10.7 in the isolated environment. XGBoost initially failed because macOS OpenMP was missing; installed Homebrew libomp 23.1.3 (1.8 MB), then tests passed. Some initial checks used an incorrect working directory; reran them from AML. A two-sensor run exercised the complete pipeline before the full run.

Ran `python scripts/run_all.py --run-dir results/runs/phase1-full-v1`. The complete run used all 207 sensors and 12 horizons; training/artifact generation took 922.34 seconds. Evaluated all three partitions, produced EDA/forecast/error figures and generated actual result tables. No test-driven parameter changes were made. Full local test suite: 56 passed. Lint, formatting, dependency consistency, saved-model reload equality and latest-origin inference passed. The IEEE compiler initially timed out downloading packages; retry succeeded. The 11-slide presentation passed finalization checks after correcting its font property; each rendered slide was visually inspected. No native PowerPoint test is claimed.

### Scientific findings and limitations

XGBoost reduced exploratory test MAE relative to persistence by 16.1%, 19.1%, 27.2% at headline horizons. RF has lower RMSE; no universal winner or classification accuracy is claimed. Mean valid training fractions: RF 89.65%, direct XGBoost 92.87%; no sparse-label model fallbacks. Found 24 negative raw XGBoost outputs among 17,015,400 test forecasts; disclosed them without silent score clipping. Existing test exposure, timezone/licensing/title ambiguities and individual viva readiness remain limitations.

### Deliverables and verification

See AML/verification/full-phase1-20261026, AML/report/ieee, AML/slides/output/phase1-study.pptx and deliverables/phase1-implementation.zip. ZIP integrity checked; raw data, environments, private build directories and trained-model/prediction binaries excluded. Main and sandbox remotes were not pushed. Current source identity is the run's hash manifest, not the old baseline commit.

## 2026-10-27 — Kavya combined integration branch

The owner requested integrating package 05 and all required remaining local work on the exact branch kavya, with no direct-main commits and no co-author trailer. Fetched canonical main f1ca84f after PRs #2-#5 merged. Preserved all Git-visible uncommitted reference files, verified 32 existing incoming files byte-for-byte, created kavya before fast-forwarding it, then fast-forwarded the inactive local main ref to that same team base. No local work lost. Intake package 05 comparison: 65 matching files, four intentionally newer shared documents, one missing pending review template; all remaining local files were within the package inventory.

Integrated runtime/CI/tests in ad09d88 and prepared evidence/report/slides in 05a3d27. Corrected deferred review-log claims on masking/scaling, causal interpretations, imputation, training versus full-file audits, weekday speed minima, peak windows/metrics and unsupported road-junction explanations. Historical agent execution/environment records remain attributed self-reports; student understanding is not invented. Added requirement/evidence mapping and explicit submission gates. No runtime estimator/source-config changes or retraining were made beyond importing the existing prepared code; frozen run identity still validates.

Actual integrated checks: 56 real-data tests passed in 1.55 seconds; Ruff lint/format passed for 37 files; uv verified all 52 installed packages compatible; setuptools built the wheel offline. Initial python -m pip attempts failed because the uv-created environment has no pip, so the successful alternative tools are recorded rather than claiming pip passed. Real-data loading and saved-model prediction passed; current IEEE source compiled successfully. Presentation ZIP/XML checks found 11 slides and three native charts; visual inspection remains the previously recorded review, not a new native PowerPoint test. A first chart-count check assumed the wrong internal OOXML path; corrected it to the actual ppt/slides/charts layout and passed. Clean tracked-source export checks are recorded separately after execution. All new commits use configured Kavya Katal identity without co-author trailers, preserving assistance disclosure. No branch push, PR or merge performed in this local integration.

### Clean-source closure and final handoff verification

Exported Git-tracked source from 212ebcd into a temporary directory without data/models/runs. With existing verified dependencies, 54 tests passed and two real-data tests correctly skipped; Ruff lint/format and all eight CLI --help imports passed. The wheel imported outside the source checkout. Frozen full-run source/config/requirements hashes matched every exported runtime file. Recorded portable checks.json and explicit limits (dependencies reused, remote CI not run, final PDF still pending). Matplotlib emitted restricted-home cache warnings but CLI imports succeeded. All later edits are verification documentation only. Final new commit authors/trailers and branch/base/scope are audited separately; no member history rewritten or main commits created.

## 2026-11-12–13 — Owner-authorized Phase 2 forecasting extension

Prepared locally on kavya under the owner's request, with substantial AI assistance and preserved teammate/Phase 1 provenance. Located the generic DL rubric and owner-supplied deadline email; the standalone original Project 4 technical brief remains unlocated. Recorded the bounded experiment protocol before fitting. Added causal normalized neural histories, shared GRU, GRU+GAT, self/uniform/no-dropout controls, validation-only tuning/blend selection, checkpoint/CSV inference, tests and academic artifacts. These are preparation/agent activities, not fabricated completed student work.

All 13 unique neural fits completed;11 selected/control fits were evaluated. Graph mean 60-minute MAE4.881 mph versus self-only 4.931, temporal 4.929 and frozen XGBoost 3.874. Trees remain stronger; RF retains the best main RMSE. Removing dropout improves one disclosed seed. Hybrid validation selected pure XGBoost. No score clipping or test-driven retuning was performed.

Host memory pressure stalled an incomplete candidate. Replaced a 681 MB eager feature cache with bounded batches after bitwise comparison of all 34,249 eligible histories and exact fitted-state verification. Preserved original sources, inherited five complete fits with checkpoint/parent lineage, and restarted the incomplete candidate from its fixed seed; first-epoch losses reproduced exactly. Independent fits used separate staging folders. A live fit was suspended/resumed581 seconds to avoid duplicate computation; optimizer state stayed in memory. Timing is not an isolated benchmark.

Fresh checks:69 tests passed in 2.71s with data available/no skips; Ruff lint/format44 files passed;59 dependencies compatible; wheel imported outside checkout; all checkpoint reloads exact; CSV inference passed tolerance. Baseline target/data/source identity and 720 historical metric rows matched. Five-page report compiled and every page inspected; six-slide editable PPTX passed structural/native/import checks and exact-final-file rendering inspection. Cached TeX font failures and PPTX validator configuration failures were corrected before final artifacts were accepted. No native PowerPoint or remote CI run is claimed.

Files are at report/phase2/ and slides/phase2/, both below 10 MB. The original31 Phase 1 runtime/config hashes and original report/slides/data remain unchanged. No commit, push, PR, member ZIP, form submission or fabricated authorship was performed. Owner/faculty-scope review, member understanding/rehearsal and later handoffs/publication remain pending. Evidence: verification/phase2-20261112/.

## 2026-11-16 — Final local LWR/control extension and academic-package review

Owner-authorized preparation with substantial AI assistance on `kavya`; no independent student implementation or understanding is claimed. Rechecked accessible faculty rubric, allocation title, submission email, repository/archive/attachments and connected source searches. The original project-specific technical brief remains unlocated. Added a requirements audit distinguishing verified rubric/logistics from the conservative implementation choice below.

Added a separate eight-cell triangular-LWR/cell-transmission simulation with two interacting local rule-based signal agents. Configuration and protocol were recorded before outcomes. Forty paired runs cover four scenarios and five seeds, comparing responsive signals against a declared equal-green fixed policy. Agents are hand-written, not MARL; the simulator is synthetic, not calibrated METR-LA or GAT-driven control. All steps enforce conservation, finite state, jam bounds and sending/receiving constraints. Responsive agents lower system vehicle-time in these selected scenarios; the fixed baseline is not demand-optimized. Boundary waiting, throughput and final residuals remain separately visible; no real-world delay saving or optimality is claimed.

Fresh final checks: 76 tests passed in 2.40 seconds, zero failures/skips; Ruff lint and format passed for 51 Python files; git diff --check passed. Rebuilt wheel imported simulation/neural modules outside the checkout; a physical update and saved graph-checkpoint observed-history CSV inference passed. Reverified 31 original Phase 1 source/config files, five raw-data hashes, five neural-training source hashes, eleven evaluated checkpoint hashes and unchanged forecasting metrics. No neural refit, test tuning or score clipping was performed.

Updated the seven-page LaTeX report and six-slide editable presentation. Built-in compiler and cached Tectonic both succeeded; every final PDF page and exact-final-file PPTX slide was rendered and visually reviewed. Native chart/table/font/package/import checks passed, without claiming native PowerPoint execution or remote CI. Final report is 684851 bytes and PPTX 100621 bytes; exact SHA-256 values are in verification/phase2-final-20261116/submission_artifacts.json. Previous dated evidence is preserved and superseded explicitly; pre-control artifacts/source were privately archived. Added simple LWR/control viva notes and updated runbook/speaking guide.

No files staged, no new commit, push, PR, merge, form submission or member ZIP was performed. Owner review, missing original technical-brief verification, individual learning/rehearsal and later publication/submission remain human-managed gates.

## 2026-11-16 — Five Phase 2 member handoffs prepared locally

Owner requested five individual ZIPs, work division and a common recipient-agent commit/PR prompt, with no push during preparation. Preserved branch kavya, the full local final reference, staging and history. Owner confirmed no more specific technical brief is available. Assigned one owner per path: Rudraksh synthetic LWR/two-agent control; Vridhi causal neural preprocessing, environment and neural contract tests; Anshuman literature/plots/report/slides/learning materials; Bineet neural architecture/training/protocol; Kavya evaluation/inference/evidence/shared integration. These are prepared integration/review scopes, not independent authorship claims or demonstrated student understanding.

Prepared five ZIPs outside the repository with payload SHA-256 manifests, explicit commit inventories, baseline hashes and original bytes for existing changed files, full Phase 2 ownership map, read-only current instructions/learning context, personal dependencies/checks, a safe read-only verifier, unique pending review logs and one byte-identical common agent prompt. The recipient prompt permits only the requested personal-branch push and PR into canonical main when invoked; it is not executed by this preparation pass. Coordinator branch stays kavya; other branches use codex/<member>-phase2-<module>. No obsolete integration-branch prerequisite.

Validated exact coverage of all 142 Git-visible delta paths, no overlapping ownership, payload byte equality to the owner reference, each ZIP's checksum/extraction and each payload/baseline verifier. Assembled the five ZIPs over the current committed base in a temporary clean directory, reusing the owner's verified environment: 74 tests passed, two correctly skipped because raw data is intentionally absent; lint and format passed for 51 Python files. This clean-source result is distinct from the earlier 76-test real-data result. No dataset/checkpoint/prediction array/simulation trajectory, environment, ZIP or private build artifact is a payload. Validation receipts and ZIP hashes stay with the private delivery set, not copied into the codebase.

No commit, stage, push, PR, merge or form submission. Members must record actual subsequent review/checks and preserve Kavya coordination credit and existing prototype/AI-assistance disclosures. The coordinator still reviews the combined PRs; packages do not certify faculty acceptance or individual viva readiness.

## 2026-11-17 — Combined merged Phase 2 integration on kavya

Owner requested pulling merged team work, integrating Kavya's remaining package and checking the assembled project. Fetched canonical main 4dc98e2 (PRs #9–#12), backed up all 142 local delta files outside Git, relocated 52 incoming untracked duplicates after verification, and fast-forwarded kavya. Preserved four completed member review logs and their genuine neural-test import/fixture changes; all other incoming bytes match the prepared reference. No unrelated work/history/data/model loss or reset/stash.

Kavya/AI-assisted prepared evaluation/inference, CI/ignore protections, frozen evidence and shared docs are integrated with fresh coordinator review. Actual fresh checks: 76 real-data tests passed in 3.41 s/no skips; lint/format 51 files; 59 dependencies compatible; data/graph integrity; graph and temporal observed-history CLI inference; offline rebuilt-wheel outside-checkout imports and physical update; LaTeX compile; final artifact hashes and limits. Forty newly executed synthetic runs reproduce original metric/summary/paired CSV bytes exactly; all fresh trajectory hashes verify. Original 31 Phase 1 source/config, five raw files, five neural source/config, eleven evaluated checkpoints and metric hash unchanged. No retraining/test tuning/clipping. Fresh evidence: verification/phase2-integration-20261117/.

Historical partial-check failures/evidence retain actual dates. Report/PPTX were not edited; hashes identify the prior rendered/agent-reviewed files. No native PowerPoint or new remote CI execution claimed. Prepared local scoped commits use Kavya identity, no co-author trailer, remain on kavya; no push/PR/form/direct-main commit. Individual understanding and faculty acceptance remain separate human gates.
