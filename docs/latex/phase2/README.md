# Current Phase 2 LaTeX source

This is the source for [the only Phase 2 submission report](../../../report/phase2/Phase2_Report.pdf). main.tex, generated/ and figures/ form one LaTeX project. Figure PDFs here are build inputs, not separate reports. The [current presentation](../../../slides/phase2/Phase2_Presentation.pptx) and its [viewable PDF](../../../slides/phase2/Phase2_Presentation.pdf) are separate submission artifacts.

From the repository root, when raw locations and the local control run are available:

```bash
python docs/latex/phase2/make_assets.py --control-run results/runs/control-integration-20261117
cd docs/latex/phase2
tectonic -X compile main.tex --outdir /tmp/t072-report-build
```

Review private build output before replacing the submission PDF. Source reads frozen verification evidence and does not retrain models. The repository root is resolved at the same directory depth after this move. Authorship/coordination/prototype/assistance disclosures remain intact. Earlier report versions are archived outside the repository and retained in Git history.
