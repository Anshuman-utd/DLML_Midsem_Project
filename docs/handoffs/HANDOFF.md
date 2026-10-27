# One team workflow - 2026-10-27

This replaces the previous integration-branch, sandbox-only and commit-only handoff workflows, including old instructions inside ZIPs.

## Fixed coordination contract

| Item | Required value |
| --- | --- |
| Team repository | https://github.com/KatalKavya96/DLML_Midsem_Project.git |
| Base and PR target | main |
| Integration branch prerequisite | None; do not wait for integration/phase1-handoff |
| Destination | Repository root; no AML/ prefix or ZIP wrapper |
| Personal branch | codex/<member>-<module> |
| Publication | Owner authorizes members to push personal branches and open PRs |
| Main/merges | Only coordinator integrates; no member direct-main/force pushes or merges |

A coordination-only baseline establishes instructions and root directories. Module implementation arrives through reviewed member PRs. Empty module directories before those PRs are expected; packages create their own assigned files. The owner's complete local reference and its past test results do not imply the remote baseline already contains the implementation.

## Per-member execution

1. Extract the personal ZIP outside the Git clone. Read its inventory/manifests and current repository instructions. Current live instructions override older ZIP snapshots.
2. Verify repository/fork remotes. Fetch main and branch from the canonical main tip (upstream/main for a fork, origin/main for a canonical clone). Preserve unrelated work and staged changes. If a previously created branch has actual work, preserve it and reconcile its base deliberately.
3. Verify payload SHA-256 values before changes. Copy only assigned payload contents into the root. Restrict staging to COMMIT_PATHS.txt. Never copy repo-context/ or delivery instructions/manifests into the tree.
4. Preserve updated shared coordinator files: AGENTS.md, PROJECT_STATE.md, README.md, CONTRIBUTING.md, .gitignore and docs/handoffs/*. If the assigned package includes an older version, review/merge required information instead of clobbering current rules.
5. Review/reproduce the module and complete the unique review log with actual agent activity, dates, checks, assistance and limitations. Student understanding stays unverified unless actually demonstrated. Explain prepared source as imported owner/AI-assisted work, not newly independent authorship.
6. Use meaningful scoped commits. Stage explicit paths, inspect every staged path/diff and check identity. Do not include data, models, environment/dependency trees, ZIPs or unrelated work. Already-present identical files do not need artificial commits.
7. Run supported checks. Record cross-package dependencies/skips honestly; no full pass is expected from one incomplete package. Push only the personal branch and open a PR to canonical main. A fork PR is valid if collaborator access is absent. Do not merge.
8. PR description: role, exact changes, original prepared-source provenance, personal/agent follow-up work, checks passed/failed/skipped and remaining dependencies. Coordinator reviews and tests the combined tree before accepting it.

## Ownership and exclusions

FILE_OWNERSHIP.json maps original payload paths. Bineet owns shared models/trees.py; Kavya reviews its XGBoost part and owns orchestration/configuration/evaluation. Do not import competing copies. Protected shared-file merging is a deliberate exception to blind package replacement, not permission to stage other modules.

Original code, datasets and historical results remain preserved. Raw data, fitted estimators, prediction arrays and environments are not included in delivery ZIPs. Prior full-local-run evidence is exploratory and distinct from new member checks. No final faculty acceptance or individual contribution is fabricated.

## Coordinator verification after assembly

Follow the assembled README for Python 3.12 setup, OpenMP and data placement; then check dependency consistency, pytest, Ruff lint/format, real-data loading, saved-model prediction/run provenance and report/package completeness. Do not claim missing-data skips prove real-data integration. Main may remain incomplete until all dependent PRs are integrated; review dependencies together.
