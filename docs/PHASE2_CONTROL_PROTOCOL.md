# Synthetic LWR/control extension — protocol recorded 2026-11-16

Owner request: finish remaining Phase 2 work locally, check LWR/multi-agent requirements, keep viva simple, do not push. Original Project4 faculty technical brief was again not found in repository, attachments, candidate Downloads, connected Gmail or Drive. Generic faculty instructions require DL architecture/ablations/validation/report/viva, but do not specify a simulator, calibrated LWR or MARL algorithm. The supplied planning master describes optional simulated policies; this is background, not verified faculty wording. A request for the missing brief remains open.

## Purpose and boundary

Add a small, separately labelled synthetic demonstration of LWR dynamics and two decentralized signal agents to address the title's unimplemented components. This is our implementation choice under the owner's request, not a newly discovered compulsory requirement. It is not calibrated from METR-LA, does not train a control policy, does not use GAT forecasts for actions and does not establish GAT-driven control improvements. No real-world actuation. Preserve all frozen forecasting scores, data and checkpoints.

## Fixed model before simulation results

Eight one-lane cells: six along a corridor and one side approach at each of two merges. Agent A controls main1/side6 into main2; B controls main3/side7 into main4. Other links follow the corridor to one exit. Each active phase serves exactly one competing approach; clearance serves neither. External source queues feed main0, side6, side7. No turns, pedestrians, lane changes or microscopic vehicles.

Use the triangular LWR flux and Godunov/cell-transmission update. Units: km, hours, vehicles. Free-flow speed60 km/h; backward wave-speed magnitude20 km/h; jam density150 veh/km; capacity derived as v*w*jam/(v+w)=2250 veh/h. Cell length.25 km, time step5 seconds, satisfying CFL. All links start empty. At each step compute flows from the old state simultaneously, with sending/receiving bounds; update every cell by inflow minus outflow. External arrivals enter a queue before receiving-limited admission. Vehicles rejected by a full cell stay in that queue; no hidden loss/clipping.

## Matched policy comparison

- Fixed-time baseline: both agents follow40s main green,5s clearance,40s side green,5s clearance (90s cycle); B has45s offset. This equal-split baseline is deliberately simple and is not demand-optimized.
- Queue-responsive agents: independent local approach/downstream occupancy observations, same phase/clearance constraints. Hold green for at least20s; maximum60s; switch after minimum when the other pressure exceeds current by2 vehicles, or current approach is empty and the other occupied. Pressure=max(upstream vehicles - downstream vehicles,0). Force alternating phase at max green to bound service starvation.5s clearance on every switch. Pressure-inspired heuristic, not a replication of a stability-guaranteed max-pressure theorem or learned MARL.

No policy tuning based on simulation outcomes. Same precomputed arrivals, topology, initial state, exit constraint and time grid for both policies. Five paired seeds101–105. Report all scenarios/seeds and unsuccessful cases.

## Scenarios (demand60min, then20min zero-arrival drain)

Three source rates are main/sideA/sideB, veh/h. Poisson arrivals sampled once per scenario/seed.

1. Balanced:800/200/200 throughout the demand interval.
2. Arterial peak:800/200/200 except minutes15–45 with1100/300/300.
3. Side-road peak:600/250/250 except minutes15–45 with600/650/650.
4. Downstream restriction:900/300/300; exit capacity900 veh/h during minutes25–40, otherwise the physical capacity. This tests spillback and the inability of signals to remove a downstream bottleneck.

Rates, seeds and policy settings are fixed here before execution. Synthetic rates/physics are illustrative assumptions, not measured LA demand/vehicle densities.

## Measures and verification

Report total system vehicle-minutes (cell occupancy plus external queues), boundary-queue waiting vehicle-minutes, mean/maximum external queue vehicles, exit throughput, final residual vehicles and switches. Queue waiting is only at the three external boundaries, not a measured mean complete-trip delay. System time includes movement and congestion. Finite horizon can censor vehicles; retain final residuals instead of hiding unfinished trips. Optional queue-wait-per-arrival is explicitly horizon-truncated, not mean completed-trip delay.

At every step require finite state, densities between0 and jam, nonnegative source queues/flows, sending/receiving/capacity limits, mutually exclusive greens, minimum/maximum green/clearance and exact network conservation (arrivals = departed + cells + boundary queues, numerical tolerance). Test red blockage, closed downstream spillback, a closed-system mass balance, empty demand, deterministic replay and CFL rejection. No improvement guaranteed. Store full local trajectories under ignored results/runs/, small metrics/manifests and plots under verification/report only.

## Theory sources

Daganzo, The Cell Transmission Model: Network Traffic (1994), Berkeley ITS research report https://its.berkeley.edu/publications/cell-transmission-model-network-traffic . Lioris and Varaiya, Variants of max pressure control for a network of signalized intersections, https://connected-corridors.berkeley.edu/sites/default/files/Variants%20of%20Max%20Pressure%20Control%20for%20Signalized%20Intersections.pdf . Source-inspired components are not full reproductions or transferred optimality/stability guarantees.

Plot examples use the first declared seed101, chosen before running comparisons. State integrals use trapezoidal quadrature on the5-second grid; reported vehicle-minutes are numerical aggregate estimates, not microscopic measured trip delays. Exact conservation/bounds are checked independently at every update.
