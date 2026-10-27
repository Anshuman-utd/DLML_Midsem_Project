# Findings register

No dataset or experimental findings recorded.

Future entries: ID, date, question, observation, source, verification method, status (verified/provisional/inconclusive/superseded), implications, and follow-up.


## F-001 — Temporal tree comparison on the inspected METR-LA period

- Date: 2026-10-26; status: Verified execution, limited generalization.
- Question: do simple independent-sensor tree methods improve baseline errors on the common evaluation grid?
- Observation: XGBoost MAE is lower than persistence at headline test horizons by 16.1/19.1/27.2%; RF has lower headline RMSE than XGBoost. No single method is universally superior across metrics/periods.
- Evidence: EXP-001, source/config/data hashes and full CSV tables in AML/verification/full-phase1-20261026.
- Verification: actual training/evaluation on all 207 sensors, saved-model reload equality, 56 tests and manual latest-origin inference.
- Limits/follow-up: the test interval was inspected earlier; no prospective validation or individual contributor understanding is certified. Negative raw XGB forecasts and missing-label/stride effects are disclosed.
