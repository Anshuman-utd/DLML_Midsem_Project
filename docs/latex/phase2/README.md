# Simple final Phase 2 LaTeX report

Rudraksh's plain-English report from PR #15 is the current narrative. The only submission report is [report/phase2/Phase2_Report.pdf](../../../report/phase2/Phase2_Report.pdf); its source is main.tex with three figure PDFs and four generated tables here. These figure PDFs are build inputs, not alternative reports. The simpler 14-slide [deck](../../../slides/phase2/Phase2_Presentation.pptx) has member modules and per-slide notes; its [PDF preview](../../../slides/phase2/Phase2_Presentation.pdf) matches it. The [whole-team viva guide](../../PHASE2_VIVA_GUIDE.md) explains the same study.

```bash
# From the repository root; reads frozen small evidence, no training
python docs/latex/phase2/make_assets.py
cd docs/latex/phase2
tectonic -X compile main.tex --outdir /tmp/t072-report-build
```

Review the private compiled output before replacing the submission PDF. Original nine-page/six-slide alternatives remain archived outside the repository and in Git history; do not recreate them inside report/slides. Attribution and exposed-test/synthetic-control limitations are preserved. No hybrid improvement or individual understanding is claimed.
