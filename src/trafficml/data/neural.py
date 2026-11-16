"""Training-only normalization and causal windows for the Phase 2 neural models."""

from __future__ import annotations

import numpy as np


class NeuralWindows:
    """Build bounded batches, preserving original target NaNs and missing flags.

    Every window starts its own forward fill. Earlier observations outside that
    window cannot leak into leading gaps. Means/std/medians see training only.
    """

    def __init__(self, values, index, train_end, history=12, horizon=12):
        self.values = np.asarray(values, dtype=np.float32)
        if self.values.ndim != 2 or not history <= train_end <= len(values):
            raise ValueError("invalid data shape or training endpoint")
        self.history, self.horizon = history, horizon
        training = self.values[:train_end]
        observed = training[np.isfinite(training)]
        if not len(observed):
            raise ValueError("training observations are entirely missing")
        self.mean = float(observed.mean(dtype=np.float64))
        self.scale = float(observed.std(dtype=np.float64))
        if not np.isfinite(self.scale) or self.scale < 1e-6:
            self.scale = 1.0
        self.medians = np.array(
            [
                np.median(x[np.isfinite(x)]) if np.isfinite(x).any() else self.mean
                for x in training.T
            ],
            dtype=np.float32,
        )
        self.anchors = np.arange(history - 1, len(values) - horizon)
        day = (index.hour * 60 + index.minute).to_numpy() / 1440
        week = (index.dayofweek.to_numpy() + day) / 7
        self.calendar = np.column_stack(
            [
                np.sin(2 * np.pi * day),
                np.cos(2 * np.pi * day),
                np.sin(2 * np.pi * week),
                np.cos(2 * np.pi * week),
                index.dayofweek.to_numpy() >= 5,
            ]
        ).astype(np.float32)

    def _features(self, anchors):
        raw = self.values[anchors[:, None] + np.arange(1 - self.history, 1)]
        missing = ~np.isfinite(raw)
        filled = raw.copy()
        for k in range(1, self.history):
            filled[:, k] = np.where(np.isfinite(filled[:, k]), filled[:, k], filled[:, k - 1])
        filled = np.where(np.isfinite(filled), filled, self.medians)
        return np.stack([(filled - self.mean) / self.scale, missing], axis=-1).astype(np.float32)

    @property
    def x(self):
        """Diagnostic compatibility view; training uses bounded batches instead."""
        return self._features(self.anchors)

    def batch(self, anchors):
        anchors = np.asarray(anchors)
        if (anchors < self.history - 1).any() or (anchors + self.horizon >= len(self.values)).any():
            raise ValueError("window outside data")
        labels = self.values[anchors[:, None] + np.arange(1, self.horizon + 1)]
        return (
            self._features(anchors),
            self.calendar[anchors],
            (labels - self.mean) / self.scale,
        )

    def state(self):
        return {"mean": self.mean, "scale": self.scale, "medians": self.medians.tolist()}
