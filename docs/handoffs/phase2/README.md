# Phase 2: five local member handoffs — 2026-11-16

These are prepared owner/AI-assisted integration/review packages, not a division of independent authorship after the fact. Kavya Katal retains coordination/preparation credit; teammate-prototype and Phase 1 provenance and assistance disclosures are preserved. Student understanding requires genuine subsequent study and demonstration.

Canonical destination: https://github.com/KatalKavya96/DLML_Midsem_Project.git, existing repository root, PR target main. No integration branch is needed. Preparation performs no staging, commits, pushes, PRs or merges. A recipient's explicit invocation of COMMON_AGENT_PROMPT.txt authorizes only their personal branch push/PR, never a main/force push or merge. Kavya's branch remains exactly kavya.

| Member | Scope | Branch |
| --- | --- | --- |
| Rudraksh Sharma | Synthetic LWR/CTM physics and two local signal agents | `codex/rudraksh-phase2-control` |
| Vridhi Chaudhary | Causal neural preprocessing, environment and neural contract tests | `codex/vridhi-phase2-preprocessing` |
| Anshuman Mehta | Literature, actual-result plots, report, presentation and learning materials | `codex/anshuman-phase2-artifacts` |
| Bineet Keshari | Shared GRU, graph attention, controlled ablations and training | `codex/bineet-phase2-neural` |
| Kavya Katal | Evaluation, inference, evidence, shared integration and final verification | `kavya` |

## Dependencies and review order

Rudraksh's synthetic module can be reviewed independently using existing base dependencies. Vridhi and Bineet supply the neural input/model pair: tests/test_neural.py intentionally tests both and imports both, so review those two PRs together; do not duplicate their files. Anshuman supplies report/slide sources, plots and narrative; builders need the corresponding runtime modules, and full regeneration also needs local raw data/models/trajectories excluded from the ZIPs. Kavya supplies evaluation/inference, shared docs/CI and frozen small evidence, and performs final combined verification after all modules are assembled.

Suggested coordinator order: review packages 02 and 04 together, integrate 01 independently, then 03 and finally 05/shared integration. Members may open PRs independently from latest canonical main; missing dependencies should be reported, not “fixed” by copying another member's paths or inventing integration branches. Keep separate PRs. No member merges their own PR.

## Package contract

Each ZIP contains payload/ (the only content to import), exact per-file MANIFEST.json SHA-256 values, COMMIT_PATHS.txt, BASELINE.json and original base bytes for modified existing files, the complete Phase 2 ownership map, read-only repo-context, a hash verifier, personal HANDOFF/STUDY_GUIDE, unique pending review log and the same common prompt. Verify before editing review logs. All file paths have exactly one package owner. Existing equal files need no artificial commit; changed files require comparison. Current/newer directives and unrelated work must be preserved. Packages contain no deletions.

Raw METR-LA, neural checkpoints, fitted trees, prediction arrays, simulation trajectories, environments and private slide-build artifacts are intentionally excluded. Historical results/checks retain their actual dates. Do not claim full pipeline reproduction from a partial package or without data/checkpoints. Frozen source snapshots predate handoff-document changes; they are historical records, not a claim of the eventual PR commit identity.

Final local checks before packaging: 76 tests/no skips with owner-held data; 51 Python files pass lint/format; original source/data and evaluated checkpoint hashes preserved. These are coordinator historical checks. Recipient and post-merge checks belong in fresh review logs. The synthetic LWR study is not calibrated LA traffic, MARL or GAT-driven control. The owner confirms no more specific faculty brief is available; use the title/generic rubric and make limits explicit.

## After merging

Compare the combined paths to the ownership manifest; resolve genuine differences explicitly. Run supported full tests, lint/format, imports, data/source fingerprints and inference with local artifacts. Recheck report/table/slide consistency if any method or score changes. Do not overwrite the preserved local final reference by blindly pulling while it is dirty. Owner review and publication/submission are separate from this local preparation.
