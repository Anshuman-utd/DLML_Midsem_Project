# Review of Rudraksh's simpler final documents — 2026-11-19

## Decision

Keep the approach: it is easier to present and learn than the previous nine-page/two-study deck. The report explains equations in words, limits the literature list to nine relevant sources, and separates the failed ML–DL blend from ablation results. The deck has four overview slides, five module slides, results, a dedicated hybrid slide and limitations. The whole-team viva guide is useful and replaces the stale six-slide guide.

## Conflict resolution

PR#15 started before the already-merged folder cleanup. Keep its simpler content but use the current paths: report/phase2/Phase2_Report.pdf, docs/latex/phase2/main.tex, slides/phase2/Phase2_Presentation.pptx and matching PDF. No obsolete T072 filenames, archive folders or duplicate source projects are reintroduced. The assets builder root calculation and commands follow the relocated source. Main's current coordinator instructions, metadata, provenance and Phase1 artifacts are preserved. His seven commits remain in history; fixes are committed on top, not squashed or rewritten.

## Corrections required before approval

- Dropout removal improved one seed; it does not prove that the model never over-fits.
- A weaker model can still improve an ensemble if errors complement each other. Report the five tested validation weights, not a universal rule that parts must be equally good.
- Matched self-loop controls support a small observed neighbour-access benefit. They do not prove physical causation or identical effective parameter use.
- The maximum mass residual is about3.041e-12 vehicles; report a safe bound below3.1e-12 or numerical precision, not exact conservation.
- The residual forecast starts from the latest causally filled speed. All-missing fallback differs from the Phase1 persistence reference.
- Inference may use already-observed readings from the test period. It may not use future labels or test-fitted preprocessing statistics.
- Local real-data76-test results and CI jobs with unavailable data/optional dependencies must be distinguished.
- Gradient clipping limits gradients before Adam, not parameter-step size directly. Softmax sums to one before training dropout and at evaluation. The responsive pressure is clipped at zero.
- RF has207 forests; XGBoost has2484 sensor/horizon regressors; a neural fit shares weights across207 sensors. Preserve this distinction in learning notes.
- Private later hybrid attempts were not adopted into the submission; describe integrated residual correction as not used in the submitted pipeline rather than claiming no follow-up ever occurred.

Kavya remains first-listed author and preparation/integration coordinator. Original prototype and AI-assistance disclosure remain, and member module labels describe integration/review responsibilities, not manufactured independent authorship or demonstrated understanding.

## Verification

See verification/pr15-review-20261119/:76 tests/no skips, lint/format52 files, exact frozen tables/number reproduction, unchanged training/data/checkpoints/scores, seven-page LaTeX compilation,14 rendered slides with repaired charts/tables and matching PDF preview. A fresh successful CI run on the final reviewed head is required before merging; no direct-main push or force push.
