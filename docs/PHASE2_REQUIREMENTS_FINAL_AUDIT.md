# Final requirements audit — 2026-11-16

The owner requested completing remaining Phase 2 work, checking LWR/multi-agent requirements first, keeping viva simple and pushing nothing.

## What the sources actually establish

| Source | Verified content | Authority/limit |
| --- | --- | --- |
| CSAI_Project_Instructions_Phase_1_and_Phase_2.pdf, section6 | DL architecture logic, hybrid innovation, ablations, DL literature, dataset/regularization, validation, theory, code quality, presentation, viva and LaTeX/IEEE report | Faculty generic rubric. Hybrid bonus needs meaningful demonstrated value; merely combining models does not qualify. No named LWR simulator, MARL algorithm or mandatory UI here. |
| Same PDF, sections2/7 | Project-ideas PDF supplies project-specific requirements; viva is individual | The separate ideas/technical brief is still missing from accessible sources. |
| Owner-pasted Nov6 evaluation email | Nov19 2026 13:55–14:20 A410; deadline12:55 IST; PPTX/PDF presentation and LaTeX PDF report each <=10MB; GitHub link; one university-email form submission | Submission logistics, not a technical control specification. |
| Allocation image | Project4: Multi-Agent Traffic Flow Control via Graph Attention Networks and LWR Models | Establishes allocated title, not exact simulator/algorithm/calibration requirements. |
| Supplied master planning attachment | Network-aware forecasting; optional simulated signal-policy experiments; no real actuation | Owner-supplied planning/background. Its claim to be authoritative is not independent faculty confirmation. |
| Historical teammate Phase1 plan | LWR/graph motivation and proposed later control/experiments | Historical proposal; many planned techniques were not implemented. Not authority to invent mandatory requirements. |

Renewed search: repository, sibling archive, original attachments and relevant Downloads PDFs; connected Gmail queries for T072/Deep Learning/Traffic and LWR/GAT returned no matches; Drive traffic/LWR results contained the old Phase1 report/deck, not the original brief. This describes accessible search results, not proof that no brief exists. The owner has since confirmed that no specific technical brief is available. The unrelated GenAI end-sem rubric is excluded.

## Completion decision under the owner's request

Implement a small, explicitly synthetic LWR/cell-transmission corridor with two decentralized rule-based signal agents, fixed-time comparison, four declared scenarios and five paired seeds. This closes the previous *implementation* gap without pretending the missing faculty brief was found. It is our conservative completion choice; it does not certify every possible project-specific requirement.

The simulator follows a standard sending/receiving conservative discretization; it is not calibrated from speed-only METR-LA, not SUMO/CityFlow, not MARL and not a GAT-driven controller. The forecasting and control studies are separate evidence streams. Real-data prediction metrics are unchanged. Physics/demand/policy settings were recorded before comparisons; positive simulated gains were not obtained by outcome-based policy tuning.

## Final evidence mapping

| Category | Local evidence |
| --- | --- |
| Architecture and theory | GRU/GAT implementation/equations/diagram; triangular LWR flux, cell conservation and two local agents |
| Dataset and regularization | Frozen METR-LA audit, causal transforms/masks, training-only normalization, dropout/decay/early stopping |
| Ablations and technical validation | Neural/self/uniform/dropout controls, three seeds, common masks, checkpoint inference; seven additional physics/control tests and40 invariant-checked simulation runs |
| Hybrid innovation | Five-weight validation search selected pure XGBoost. No hybrid benefit or bonus marks are claimed. |
| Literature | Actual inspected GRU/GAT/DCRNN/Richards/PyTorch sources plus Berkeley CTM technical overview and pressure-inspired local-control paper; no transferred stability/optimality claim |
| Report/presentation | Updated LaTeX PDF and editable six-slide PPTX; exact values and limitations from saved evidence |
| Code/reproduction | Local source, environment pins, CLI runbook, hashes, full tests/lint/format, small evidence |
| Individual viva | Plain-English notes and assigned speaking/review scopes. Human understanding is not established by agent preparation. |

## Remaining owner actions, not automated here

Review final local materials, verify any original technical-brief requirements if supplied, demonstrate individual understanding, publish through the owner-approved handoff workflow when requested and submit the one-time form using university email by Nov19 12:55 IST. The explicit no-push instruction means the canonical GitHub link does not yet publish this Phase2 extension. No push/PR/merge/form action is performed by this completion pass.
