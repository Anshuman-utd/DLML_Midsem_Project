# LWR and the two control agents — simple viva notes

## The short explanation

“We have two separate experiments. On real METR-LA data, GRU and graph attention predict future speed. In a separate synthetic road corridor, an LWR cell-transmission model moves vehicles and two local signal agents choose which approach gets green. The simulation is a demonstration, not calibration of Los Angeles roads or a learned neural control policy.”

A GAT attention head is a mathematical aggregation inside a forecasting network. A control agent is a separate object that chooses a signal action. Our two attention heads are **not** the two signal agents.

## What LWR means

- Density: how many vehicles occupy one kilometre of road, veh/km.
- Flow: how many vehicles cross a boundary each hour, veh/h.
- Speed: how quickly vehicles move, km/h in this simulator.
- Conservation: vehicles do not appear or disappear inside the road. New occupancy equals old occupancy plus arrivals minus departures.

The real forecast scores remain in mph. The synthetic physics uses km/h. We do not silently substitute forecast mph into density equations or infer measured density from METR-LA speed.

LWR writes conservation as `density change over time + flow change over space = 0`. The relation `flow = density × speed` uses consistent units. A triangular fundamental diagram limits both free movement and crowded receiving capacity.

## Our assumptions, not measured LA parameters

Free-flow speed is 60 km/h, backward wave-speed magnitude20 km/h and jam density150 veh/km. These are illustrative fixed parameters. Capacity is `60 × 20 × 150 / (60 + 20) = 2250 veh/h`; critical density is `2250 / 60 = 37.5 veh/km`.

Each cell is 0.25 km. At jam, a cell stores `150 × .25 = 37.5` vehicles. Fractional vehicles are valid in a macroscopic continuum approximation; the simulator is not tracking individual cars.

A step is 5 seconds, not the forecast dataset's five-minute sampling. At free speed, movement in one step is `60 × 5/3600 = .0833 km`, below the.25-km cell length. This satisfies the CFL stability limit; an excessive step is rejected by tests.

## Eight cells and two signals

The main road is `0 → 1 → 2 → 3 → 4 → 5 → exit`. Side cell 6 joins before cell 2; side cell 7 joins before cell 4.

- Agent A chooses between main cell 1 and side cell 6 entering cell 2.
- Agent B chooses between main cell 3 and side cell 7 entering cell 4.
- Main flow and side flow never receive green together at the same merge.
- Clearance gives neither movement green for 5 seconds.

External queues wait before source cells 0,6,7 if those cells cannot receive more vehicles. We retain every arrival in a cell, a source queue or the cumulative exit count. Spillback is physical coupling: if downstream storage fills, receiving flow falls, so upstream cells fill and may block the next signal. The agents do not exchange learned messages or share a reward; their actions affect each other through the corridor.

## One update, in ordinary words

1. Read all old cell occupancies before changing any of them.
2. Calculate how much each upstream cell can send and each downstream cell can receive.
3. For a green connection, flow is the smaller limit. For red, it is zero.
4. Admit source vehicles only if the first cell has receiving capacity. Others stay in its external queue.
5. Update every cell simultaneously from incoming minus outgoing flow. Count exit flow.
6. Check mass conservation, finite state, capacity limits and nonnegative density/queues.

Example: an upstream cell can send1500 veh/h and the next cell can receive600. Green permits600 veh/h, or `600 × 5/3600 = .8333` vehicles this step. Red permits zero. These are teaching values; actual run values come from the current state.

## What the agents decide

Fixed-time baseline:40 seconds main green,5 seconds all-red,40 seconds side green,5 seconds all-red. B has a 45-second offset. The equal split is simple and not optimized for each demand pattern.

Responsive policy: each agent observes its own main/side/downstream cell counts. Its pressure proxy is `max(upstream vehicles − downstream vehicles, 0)`. These counts include moving vehicles; they are not measured stopped queues or a full reproduction of a max-pressure theorem.

Hold a green for at least 20 seconds. After that, switch if the competing pressure exceeds the current pressure by 2 vehicles, or the current approach is empty while the other contains traffic. Force an alternate phase after60 seconds to bound starvation. Every switch includes 5 seconds all-red. All constants were declared before outcomes.

This is a **rule-based decentralized controller**, not reinforcement learning. There is no control-training loss, reward optimization, DQN, PPO, multi-agent RL, learned safety guarantee or optimal-policy claim. Both policies start with empty traffic; their initial signal phases/offsets are part of their declared rules.

## What we tested

Four fixed synthetic scenarios: balanced demand, arterial peak, side-road peak and a temporary downstream exit restriction. Each has 60 minutes of demand plus 20 minutes with no new arrivals to let vehicles leave. Five paired seeds give40 runs:4 scenarios ×5 seeds ×2 policies. Both policies receive the same sampled arrivals and physics for each paired run. No policy tuning was performed after seeing outcomes.

## What the numbers mean

Total system vehicle-minutes is the numerical area under the number of vehicles in cells plus external queues. It includes movement and waiting. For example,10 vehicles present for 2 minutes contribute20 vehicle-minutes. Lower is better when arrivals/horizon are matched.

Boundary waiting vehicle-minutes counts only the area under the three external queues. It excludes congestion inside cells. It is **not** average completed-trip delay. Throughput is vehicles leaving the exit; residual is vehicles still present at the horizon. Report residuals to avoid hiding unfinished trips.

The responsive policy has lower total system time against this equal-green baseline in all four selected scenarios. That is evidence for this illustration, not universal superiority. The baseline is not demand-optimized, the network is tiny and parameters/demand are synthetic. In the downstream-restriction case, the fixed policy leaves about4.06 vehicles on average; those are retained in the accounting. Read the measured tables for exact per-run values and seed spread.

## How it connects to the prediction study

Both studies concern connected traffic systems. The real-data forecasting study tests learned neighbour information. The synthetic control study shows conservation, storage, spillback and interacting local decisions. They are **not** a calibrated end-to-end predictive-control system. We never claim GAT forecasts caused the simulated control gains.

## Demonstrate it

```bash
PYTHONPATH=src .venv/bin/python scripts/run_control.py \
  --run-dir results/runs/control-manual-review
MPLCONFIGDIR=/tmp/t072-mpl-cache PYTHONPATH=src \
  .venv/bin/python scripts/build_control_report.py \
  --run-dir results/runs/control-manual-review
```

The second command refreshes shared report/evidence inputs; use it intentionally when reviewing the frozen configuration. No METR-LA data, neural checkpoint, simulator installation or network access is needed for these runs. Main forecasting inference is a separate command in the runbook.

## Likely viva questions

- Why can fractional vehicles appear? Continuum cell densities, not microscopic cars.
- Why are there two agents? Each independently controls one different merge with local observations.
- What is learned in these agents? Nothing; only the forecasting networks are trained.
- Why no GAT-to-signal link? Speed-only data do not supply calibrated flow, density or signal dynamics. We keep the evidence streams honest.
- What prevents impossible flow? Sending/receiving capacity, red gating, CFL and per-step physical checks.
- Is the simulation real LA traffic? No. Parameters, network and arrivals are synthetic.
- Is the policy always better? Not demonstrated. Results concern four selected scenarios and an unoptimized equal-green baseline.
- What remains unverified? Original faculty-specific simulator/MARL requirements and each member's actual understanding.

Preparation is owner/AI-assisted; assignments and reading notes do not prove independent student implementation.
