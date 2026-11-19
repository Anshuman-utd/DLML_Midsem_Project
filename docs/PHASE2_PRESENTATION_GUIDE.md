> Current deck (November 18): [14-slide PowerPoint](../slides/phase2/Phase2_Presentation.pptx), [PDF preview](../slides/phase2/Phase2_Presentation.pdf). It contains per-slide speaker notes. The six-slide speaking plan below is historical; that earlier deck is archived outside the repository, not offered as a current submission.

# Final six-slide presentation and viva guide — November16

This is a proposed speaking allocation, not fabricated independent authorship. Prepared implementation and artifacts use substantial owner/AI assistance. Each member must actually demonstrate understanding and record their own review.

## 1. Forecasting and synthetic control — Kavya

“We study two parts. On METR-LA, we test whether graph neighbours help forecast traffic speed. Separately, a small synthetic LWR road model demonstrates two local signal controllers. We do not claim a calibrated neural controller for Los Angeles roads.”

Introduce the five members and allocated Project4 title. Explain the separation early; it prevents confusing good simulation numbers with real-data forecasting accuracy.

## 2. Data and protocol — Rudraksh

“METR-LA has207 sensors and34,272 five-minute timestamps. Twelve observed slots predict the next twelve speeds. We keep time order, purge overlapping future targets, fit preprocessing on training data, and compare the same valid answers.”

Explain zero/NaN convention, flags, exact graph/sensor order and why12 slots span55 minutes. The old test interval is exploratory. The simulation is separate: eight cells, two agents, four synthetic scenarios and five paired seeds.

## 3. Temporal and graph architecture — Vridhi

“The shared GRU learns a32-number summary for each sensor from speed and missingness. GAT aggregates allowed neighbours with two attention heads. The head predicts twelve corrections to the latest filled speed.”

Explain reset/update gates, direct horizons and five calendar features. The receiver/sender convention is a coding convention, not verified physical upstream labels. The two attention heads are not the two signal agents.

## 4. Training and ablations — Bineet

“We trained with masked MAE and Adam. Tuning validation chose learning rate.001 for both main families. We saved the best validation checkpoint and compared graph, self-only, uniform attention and no-dropout variants.”

Three seeds support temporal/graph/self comparisons; uniform/no-dropout have one seed. Explain dropout, decay, clipping and early stopping. Neighbours modestly help; removing dropout helped this seed, so do not claim all regularization improved scores. Training choices were not changed using test results.

## 5. Measured forecasts — Anshuman

“Lower MAE means smaller average errors; RMSE gives big misses extra weight. XGBoost remained best for headline MAE and RF for RMSE. Graph learning slightly improved the neural baseline/control but did not beat the trees.”

At60 minutes, XGBoost MAE3.874 mph, graph mean4.881, self-only4.931. Neural means are three separately scored seeds, not a forecast ensemble. Reserved validation chose pure XGBoost, so the hybrid did not demonstrate added value. MAPE is not accuracy. Read peak/sensor and variability tables in the report; no significance claim from dependent forecasts.

## 6. Synthetic LWR and local agents — Kavya

“LWR conserves vehicles. Our cells limit flows by what upstream can send and downstream can receive. Agent A chooses main or side flow at the first merge; B does so at the second. They use local occupancies,20–60-second greens and5-second clearance.”

Read the table as mean **system vehicle-minutes**, not average trip delay or measured city savings. The responsive policy beats this unoptimized equal-green baseline in the four selected synthetic cases. Forty runs use matching arrivals for each pair. Residual vehicles remain in the evidence. Agents are hand-written rules, not trained RL policies; no GAT prediction enters their actions. Parameters and demand are synthetic, and the original faculty technical brief remains unlocated.

## Offline demonstrations

- Forecast: use scripts/predict_phase2.py, the verified selected checkpoint and a12-row observed-history CSV. Output has12 future timestamps and207 sensor columns. Follow PHASE2_RUNBOOK.md. A new clone needs documented data and reproduced checkpoints, which are excluded from Git.
- Control: run scripts/run_control.py with configs/control.yaml in a fresh run directory. No data download, neural model, SUMO or CityFlow installation is needed. Show metrics.csv, then explain a single conservation update and the two local decisions.

## Everyone must answer

1. Which part is learned, and which is rule-based?
2. Why do the two GAT heads differ from the two agents?
3. What are density, flow and speed units? Why not infer LA density from speed?
4. How does red/green gate a sending/receiving flow?
5. How do controllers affect one another without learned messages?
6. What does system vehicle-time include? What does boundary waiting omit?
7. What failed to improve, and where is the evidence?
8. What is not established: calibrated physics, real control, GAT-driven actions, MARL, optimality, significance or individual understanding from prepared code.

Read PHASE2_CONTROL_NOTES.md and PHASE2_LEARNING_NOTES.md for simple worked explanations. Rehearse with the actual artifacts, not only this script. Publication and the one-time university-email submission are owner-managed actions and have not occurred.
