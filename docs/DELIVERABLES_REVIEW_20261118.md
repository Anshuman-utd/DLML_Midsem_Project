> Superseded folder layout, 2026-11-19: old artifact versions are now archived outside the repo, not in report/slides archive subfolders. Current report source is docs/latex/phase2/. Submission PDF/PPTX bytes remain unchanged. See report/README.md, slides/README.md and DELIVERABLES_LAYOUT.json for current locations; the dated review below preserves the November 18 activity.

# Deliverable review and organization — 2026-11-18

## Current files to use

| Phase | Report | Presentation | Preview |
| --- | --- | --- | --- |
| Phase 1 | report/phase1/Phase1_Report.pdf (17 pages, preserved) | slides/phase1/Phase1_Presentation.pptx (8 slides, preserved) | slides/phase1/Phase1_Presentation.pdf (original compressed export) |
| Phase 2 | report/phase2/Phase2_Report.pdf (9 pages, Rudraksh latest) | slides/phase2/Phase2_Presentation.pptx (14 slides, repaired) | slides/phase2/Phase2_Presentation.pdf (rendered from exact repaired file) |

Phase 2 report source/tables/figures are grouped under report/phase2/source/. Figure PDFs are build assets, not extra report versions. Older coordinator report and source sit under report/phase2/archive/coordinator-20261116/; its six-slide deck and Rudraksh's unmodified original upload are labelled in slides/phase2/archive/. Phase 1 earlier source/deck are similarly separated. No original artifact was discarded. DELIVERABLES_LAYOUT.json maps every moved file and its before/after-move hash. Current navigation is updated; historical evidence retains original path identities and is resolved through that map.

## What was reviewed

Rudraksh PR #14 adds an alternative report/deck from the existing frozen evidence, not new trained models. All nine report pages and fourteen original and exact-repaired slides were rendered and visually inspected. Headline MAE/RMSE, three-seed controls, blend endpoint and synthetic means agree with frozen results. Kavya remains first-listed author and coordination/preparation attribution plus prototype/AI-assistance disclosure are preserved. The report correctly keeps forecasting separate from synthetic control and reports no hybrid gain.

Interpretation reminders: matched controls support a small observed neighbour-access benefit for these runs; they do not prove physical causation or global optimality. Three seeds are not a statistical significance test. The slide4 shorthand “persistence” means latest filled speed (training-median fallback for an entirely missing history), which differs from the historical-average fallback in the Phase 1 reference. Slide11's pressure shorthand is clipped at zero in code. Keep those details in viva. Existing compact-model/peak errors and single-seed ablation limitations remain visible. New private hybrid follow-ups are NOT inserted into the final project or these artifacts.

## PPT compatibility repair

Three chart parts contained negative axId/crossAx values. OOXML requires unsigned axis IDs; see Microsoft documentation: https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.axisid . Those references were consistently remapped to valid positive IDs. Several chart caches differed from their original embedded worksheet values by floating-point decimal serialization below 1e-12; cache strings were refreshed from the exact existing referenced cells, preserving worksheets/formulas. No substantive values, slide text, notes, layouts, theme, images or embedded workbook parts changed.

The final repaired PPTX passes package/layout, all five native quantitative-chart workbook checks and first-party import. All 14 repaired slides render pixel-identically to the original's repair-tolerant import. This validates the repair/rendered preview; native Microsoft PowerPoint opening is not claimed. The original PPTX is archived unchanged. PDF preview is rasterized slide rendering; use the PPTX for editable charts and speaker notes.

## Phase 1 historical cautions

The preserved Phase 1 PPTX is 20.4 MB and exceeds the current 10 MB form limit; its PDF is about1.31 MB. Known RMSE/candidate-label discrepancies remain documented in docs/final_deliverables.md and were not silently corrected. Phase 1 is retained as historical material, not the Phase 2 submission. Current Phase 2 report, deck and preview are each below10 MB.

## Scope and workflow

Only artifact organization, presentation compatibility, navigation and report-builder output locations changed. Original training scripts/data/configuration/models/scores remain unchanged. The current report source compiles after relocation. Historical builders target their archived source tree; current report assets use the relocated source builder with a corrected repository-root calculation. No commits, pushes, score tuning or model training were performed for this organization.
