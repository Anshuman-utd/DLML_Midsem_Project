# Five-member handoff: LOCAL COMMIT ONLY

Updated 2026-10-27. This replaces the earlier push/PR workflow. The owner will
push; each member's agent prepares only its assigned local commit. No remote
integration branch is required to exist for the agent to work from an agreed
local base. Preserve existing history and use codex/<package-id>-review.

## What to send and paste

Send each member their individual ZIP. They extract it OUTSIDE their Git clone,
open their intended checkout with their agent, and paste AGENT_PROMPT.txt.
If the agent cannot identify the checkout/package, supply those paths.

- payload/: only these files are candidates for copying/committing.
- COMMIT_PATHS.txt: exact per-person allowlist, including one pending review log.
- MANIFEST.json: original payload SHA-256 values, name, role and commit scope.
- repo-context/: common read-only background snapshots; DO NOT copy/commit these.
- CONTEXT_MANIFEST.json: SHA-256 values for context and instruction files.
- README.md / AGENT_PROMPT.txt / HANDOFF.md: instructions outside commit scope.

Each agent must inspect live instructions, existing changes and staged files;
validate hashes; use the agreed personal local branch; review and record only
actual agent activity; stage only the allowlist; inspect every staged path; and
create a truthful local commit. Stop on identity/base/conflict ambiguity. Never
commit other people's staged work or manufacture author/date/activity history.

Do not use git add . or git add -A. Do not commit snapshots/inventories from
outside payload/. Shared files are committed by one owner only. Bineet owns
shared models/trees.py; Kavya reviews its XGBoost portion using context and
assembled source, without copying a competing version.

Prepared implementation remains owner/AI-assisted work based on the teammate
prototype. Each review log distinguishes actual agent work from pending human
understanding. Receiving or importing prepared files does not establish original
student authorship. Preserve docs/CONTRIBUTIONS.md and historical evidence.

## Coordinator after receiving local commit details

All five commits must be available on one integration branch for combined
checks. Separate local clones do not exchange commits automatically: the owner
must explicitly arrange branch publication or transfer later. The package does
not automate that step or authorize agents to publish. Preserve commits/history
when integrating and inspect conflicts rather than assuming the final tree.

The five source payloads have disjoint paths and reconstruct the curated 113-file
snapshot, plus five review logs. Partial assemblies may not import or pass tests.
Once all parts are present, follow the assembled README for Python 3.12 setup,
platform OpenMP, raw-data placement and these checks:

```bash
python -m pip check
pytest -q -ra
ruff check .
ruff format --check .
python scripts/check_data.py
```

Run installation/setup only where authorized. Datasets, trained models, prediction
arrays and environments are excluded. Missing-data skips do not validate real-data
integration. Saved prediction requires trusted model artifacts or a new run.
Historical results are exploratory because test outputs were already inspected;
56 passing tests describe the prior full run, not a fresh check by this package.
Final report, faculty scope, metadata/rights and individual viva review remain.

The original combined ZIP is preserved. No commits, pushes, PRs or merges were
performed when preparing these packages.
