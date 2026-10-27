"""Small, causal, per-sensor features. No graph or target-derived profiles."""

from __future__ import annotations

import numpy as np
import pandas as pd


class SensorFeatures:
    """Fit one fallback median on training observations, then transform past windows only."""

    def __init__(self, history: int = 12, engineered: bool = True):
        self.history = history
        self.engineered = engineered

    def fit(self, training_values: np.ndarray):
        valid = np.asarray(training_values)[np.isfinite(training_values)]
        self.median_ = float(np.median(valid)) if len(valid) else 0.0
        return self

    @property
    def names(self):
        names = [f"lag_{i}" for i in range(self.history)]
        if not self.engineered:
            return names
        return (
            names
            + [f"missing_lag_{i}" for i in range(self.history)]
            + [
                "mean_3",
                "mean_6",
                "mean_history",
                "std_history",
                "min_history",
                "max_history",
                "difference_1",
                "difference_history",
                "missing_fraction",
                "sin_time",
                "cos_time",
                "sin_week",
                "cos_week",
                "weekend",
            ]
        )

    def transform(self, values, index, anchors):
        values, anchors = np.asarray(values), np.asarray(anchors)
        if not hasattr(self, "median_"):
            raise ValueError("fit on training values before transforming")
        if values.ndim != 1 or anchors.ndim != 1 or anchors.dtype.kind not in "iu":
            raise ValueError("expected one sensor and integer anchors")
        if (anchors < self.history - 1).any() or (anchors >= len(values)).any():
            raise ValueError("feature window outside observed series")
        offsets = np.arange(-self.history + 1, 1)
        raw = values[anchors[:, None] + offsets]
        raw = np.where(np.isfinite(raw), raw, np.nan)
        missing = np.isnan(raw)
        # Fill left-to-right within each sample; no backward fill and no future readings.
        filled = pd.DataFrame(raw).ffill(axis=1).fillna(self.median_).to_numpy(np.float32)
        lags = filled[:, ::-1]
        if not self.engineered:
            return lags.copy()
        # Statistics use the same causal, explicitly imputed history as the lag features.
        stats = np.column_stack(
            [
                filled[:, -min(3, self.history) :].mean(axis=1),
                filled[:, -min(6, self.history) :].mean(axis=1),
                filled.mean(axis=1),
                filled.std(axis=1),
                filled.min(axis=1),
                filled.max(axis=1),
                filled[:, -1] - filled[:, -min(2, self.history)],
                filled[:, -1] - filled[:, 0],
                missing.mean(axis=1),
            ]
        )
        times = index[anchors]
        day = (times.hour * 60 + times.minute).to_numpy() / 1440
        week = (times.dayofweek.to_numpy() + day) / 7
        clock = np.column_stack(
            [
                np.sin(2 * np.pi * day),
                np.cos(2 * np.pi * day),
                np.sin(2 * np.pi * week),
                np.cos(2 * np.pi * week),
                times.dayofweek.to_numpy() >= 5,
            ]
        )
        return np.column_stack([lags, missing[:, ::-1], stats, clock]).astype(np.float32)
