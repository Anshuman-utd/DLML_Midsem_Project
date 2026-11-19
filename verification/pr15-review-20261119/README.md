# PR #15 reconciliation and verification — 2026-11-19

The owner explicitly requested a detailed review of Rudraksh's simpler documents, conflict resolution on top of his branch, a commit and merge after checks. Original PR head2b493b0 was based on eaa4eee; canonical main had since merged cleanup PR#16 at e262867. The conflicts are primarily content-versus-relocation, not runtime model changes.

Kept his simpler seven-page IEEE report,14-slide module-based deck, nine-reference literature structure, separate hybrid section, speaker notes and whole-team viva guide. Kept main's single-submission paths and docs/latex/phase2 source layout. Accepted removal of unused placeholders/stale historical proposals; preserved all source/data fingerprints, historical evidence and member commits. Previous artifacts are backed up privately and retained in Git history.

Corrected overclaims about dropout, causation, hybrid failure, exact vehicle conservation, model counts, input-time use and CI skips. Repaired invalid negative IDs in both native charts and matched numeric-cache serialization to unchanged embedded worksheets. New report source and PDF match; matching14-page PDF preview regenerated. Native PowerPoint opening is not claimed.

76 local tests pass/no skips (2.96s);52 Python files pass lint/format. All four generated tables and numbers.json reproduce the original PR's frozen input numbers exactly.31 original Phase1 source hashes, five raw files, five neural-training source/config hashes, seven control-source/config/protocol hashes and11 evaluated checkpoint hashes remain unchanged. No training, tuning, clipping, new model results or private hybrid integration. Artifact sizes/hashes and render/compile checks are in checks.json.

Historical evidence remains dated; its old hashes refer to prior artifacts and must not be relabelled as this version. Fresh CI on the resolved PR head must pass before the authorized expected-head merge. Preserve authorship and assistance; no student understanding or faculty acceptance is inferred.
