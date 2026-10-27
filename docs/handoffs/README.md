# Session handoffs

Use `YYYY-MM-DD-short-topic.md` for substantial transitions. Record starting and ending state, actual work, verification, unresolved issues, next steps, and required reading. Keep the latest snapshot in [PROJECT_STATE.md](../../PROJECT_STATE.md); avoid duplicating the entire journal.

## Phase 1 member commits

- [Commit-only workflow](HANDOFF.md)
- [Common agent prompt](AGENT_PROMPT.txt)
- [Exact standalone payload ownership map](FILE_OWNERSHIP.json)

These shared documents coordinate the five prepared module packages. ZIPs and their read-only snapshots are local delivery files, not part of this repository commit. Member implementation paths in the ownership map are relative to the standalone sandbox repository root, not this parent scaffold. Existing member code under AML/ remains uncommitted here. The owner must select the actual implementation repository/base before package integration. No push, PR, merge or member-authorship claim is authorized by these documents.
