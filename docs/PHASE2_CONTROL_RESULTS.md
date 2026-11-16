# Synthetic LWR and two-agent control results

All values below are measured simulation outputs under the predeclared protocol. They are not LA traffic measurements, trained MARL or GAT-driven control evidence.

| Scenario | Fixed system veh-min | Responsive system veh-min | Fixed boundary wait veh-min | Responsive boundary wait veh-min |
| --- | --- | --- | --- | --- |
| Balanced | 3263.3 | 2212.8 | 1.9 | 1.9 |
| Arterial peak | 10850.7 | 2840.5 | 4126.1 | 4.6 |
| Side peak | 6435.1 | 3173.6 | 629.4 | 3.3 |
| Downstream limit | 14308.9 | 6003.9 | 5720.4 | 334.8 |

40 runs, 5 paired seeds per scenario. Maximum cumulative mass residual: 3.04e-12 vehicles. All states stayed within physical bounds. Full per-run metrics and seed variation are in verification/phase2-final-20261116/control/.

The responsive heuristic reduced system time against this equal-green baseline in all four selected scenarios. This does not establish optimality, transfer to another network, real delay savings or neural-control benefit. Fixed time is not demand-optimized. Boundary waiting excludes inside-network queues; system vehicle-time includes movement. Time integration is a numerical estimate. Final residuals are disclosed in metrics.csv, including about4.06 vehicles for the fixed downstream-restriction case on average.

Reproduce with scripts/run_control.py and scripts/build_control_report.py. Physics, rates and settings were fixed before outcomes; no policy tuning was performed. See docs/PHASE2_CONTROL_PROTOCOL.md and docs/PHASE2_CONTROL_NOTES.md.
