# Project state

Updated: 2026-10-27, Asia/Kolkata. Team T072, Section C.

## Canonical project and current scope

The one canonical working project is `/Users/kavyakatal/Desktop/DLML_Midsem_Project`. Its Phase 1 implementation now lives directly at the repository root: `src/trafficml/`, `scripts/`, `tests/`, `configs/`, `report/`, `slides/` and `verification/`. The nested `AML/` working folder no longer exists. The owner requested this consolidation so the prepared ZIP payload paths match the main repository root. Original `/Users/kavyakatal/Downloads/AML` is unchanged.

The local Phase 1 study includes persistence, historical average, RF, XGBoost, 38 causal features, budgeted validation tuning, chronological purged splits, common target masks, EDA/error plots, saved-model prediction, literature/methods/viva notes, compiling IEEE source and an 11-slide presentation. No GAT, calibrated LWR, UI or traffic-signal simulation is implemented. Phase 2 remains deferred. Implementation is not a certificate of final faculty acceptance or individual understanding.

## Existing measured evidence

The recorded all-207-sensor run is now `results/runs/phase1-full-v1`; its relative-path source/data/config fingerprints are preserved. Model fitting and artifact generation took 922.34 seconds. See [verification evidence](verification/full-phase1-20261026/README.md). The earlier full run recorded 56 passing tests, lint/dependency checks and saved-model reload equality. After root consolidation, all 56 tests passed again in 2.36 seconds, Ruff lint and formatting checks passed for 37 files, the real-data loader/graph checks passed and latest-origin saved-model prediction succeeded with manifest validation. Checks used the existing isolated environment and explicit PYTHONPATH=src; no retraining or environment reinstall was needed. The IEEE source previously compiled; rendered slides were inspected. Native PowerPoint and updated remote CI were not tested.

Exploratory test XGBoost MAE: 2.9205 / 3.3764 / 3.8737 at 15/30/60 minutes, 16.1% / 19.1% / 27.2% below persistence. RF has lower headline RMSE. These are regression errors, not classification accuracy. Raw test contains 24 negative XGBoost outputs among 17,015,400; no silent clipping.

## Preserved separate archive

`/Users/kavyakatal/Desktop/DLML_Project_Archive_2026-10-27/` contains delivery ZIPs/extractions, pre-consolidation root-document snapshots, obsolete placeholder scaffolding, historical result layouts/runs, unused PEMS-BAY data and private presentation authoring files. MOVE_MANIFEST.json records relocation. No work was deleted. Frozen manifests retain historical command paths as provenance, not current execution instructions.

The separate Desktop/DLML-sandbox checkout was not merged into this repository. Its existing shared-run symlink was updated to the new root saved-run location so it remains usable.

## Team workflow and Git status

The local shared-documentation commit is 6e611d6; it preceded consolidation. The layout changes and member-assigned implementation remain uncommitted after this move, pending deliberate review/member integration. No push or PR was performed. Data, saved runs/models, environments, caches, node_modules and delivery bundles are excluded from Git; small measured evidence, report source and slides remain eligible.

[Handoff workflow](docs/handoffs/HANDOFF.md) and [agent prompt](docs/handoffs/AGENT_PROMPT.txt) now describe this root layout. Payload paths need NO AML/ prefix. Preserve newer root instructions/state/ignore rules when reviewing prepared package versions. Member ownership is in [the path map](docs/handoffs/FILE_OWNERSHIP.json); existing owner/AI-assisted implementation must retain truthful provenance. Each member records actual agent review separately from their own learning or participation. The owner's group workflow permits members to publish personal branches and open PRs; it does not authorize direct-main writes/merges or publication by this cleanup operation. The fixed canonical remote is KatalKavya96/DLML_Midsem_Project and the base/PR target is main. No integration branch is required.

## Remaining final-submission review

Clarify speed-only versus broader faculty title/LWR scope, timezone/DST and raw-data redistribution terms. The previously inspected test remains exploratory. Export/inspect the final PDF, reproduce the final assembled package and verify individual understanding and accurate contribution/assistance disclosures. Initial planning placeholders were archived; requirements mapping is not thereby completed.

## Coordination repair prepared 2026-10-27

Rudraksh and Anshuman correctly reported that the remote 6e611d6 instructions conflicted with the owner group workflow. Replaced active instructions and prompt rather than layering another contradictory override. Canonical repository/base are now explicit; members are authorized to push personal branches and open PRs into main. Shared files must preserve these newer directives when importing old package copies. The repair commit includes root-layout placeholders and shared coordination/scaffold cleanup only, leaving member runtime source/configuration, estimator code, tests and deliverables uncommitted. It needs owner-authorized publication before teammates can fetch these updated rules. No integration branch is needed.
