# METR-LA working dataset card

This project uses the existing METR-LA speed file operationally for the independent-speed forecasting experiment. This is not a claim that the missing project-ideas brief's broader flow/control expectations have been signed off by faculty.

Verified local properties: shape 34,272 by 207; five-minute ordered timestamps from 2012-03-01 00:00 through 2012-06-27 23:55; speed-only sensor matrix; graph ordering and constructed adjacency verified against the supplied reference. Actual checksums, masks, outage distributions and per-sensor statistics are in the run's manifest/analysis files. No separate measured flow/occupancy channels are created.

The upstream DCRNN repository provides download and benchmark instructions: https://github.com/liyaguang/DCRNN. Its code license is MIT; raw-data redistribution terms were not separately verified, so raw files are excluded from the package. Timezone/DST and unit metadata are not resolved by the file loader; mph follows the benchmark description.

METR-LA is suitable for the current speed-regression objective and future graph compatibility. It is insufficient to directly validate measured flow, occupancy, calibrated LWR parameters or real traffic-signal control. PEMS-BAY is an available alternative speed benchmark in the supplied folder but is not used here. PEMS04/08 remain alternatives requiring their own authoritative channel/license/data audit if measured flow is required; no uninspected properties are asserted. No dataset-score matrix or claim of optimal dataset choice is fabricated.
