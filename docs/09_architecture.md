# Planned architecture

Status: directories exist; the pipeline is not implemented.

Proposed flow: raw data → validation → EDA → chronological partitioning → leakage-safe features → training → validation and tuning → final testing → analysis → reporting. EDA that informs modeling choices should use the training partition; validation/test preprocessing must respect fit boundaries.

Future responsibilities in `src/traffic/`: `data/` for loading and validation; `features/` for causal features; `models/` for estimators; `evaluation/` for masks and metrics; `visualization/` for plots. Exact interfaces and experimental policies remain undecided.
