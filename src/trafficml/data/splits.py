"""Chronological windows with purged targets at every split boundary.

Input history may use previously observed timestamps across a boundary. Targets
from an earlier partition must end by the first anchor of the next partition.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Splits:
    train: np.ndarray
    val_tune: np.ndarray
    val_stack: np.ndarray
    test: np.ndarray

    def items(self) -> list[tuple[str, np.ndarray]]:
        return [(name, getattr(self, name)) for name in ("train", "val_tune", "val_stack", "test")]


def anchor_indices(num_steps: int, history: int = 12, horizon: int = 12) -> np.ndarray:
    """Anchors with full observed input and future-target windows inside the series."""
    if any(
        not isinstance(x, (int, np.integer)) or isinstance(x, bool) or x < 1
        for x in (num_steps, history, horizon)
    ):
        raise ValueError("num_steps, history and horizon must be positive integers")
    if num_steps < history + horizon:
        raise ValueError("series is too short for a full input and target window")
    return np.arange(history - 1, num_steps - horizon)


def chronological_split(
    num_steps: int,
    history: int = 12,
    horizon: int = 12,
    train_frac: float = 0.7,
    test_frac: float = 0.2,
) -> Splits:
    """Provisional 70/10/20 anchor partition, purged by horizon-1 at each boundary.

    Preserve nominal partition starts; discard the last horizon-1 anchors of
    train, val_tune and val_stack. This is NOT the unpurged DCRNN protocol.
    The validation-half allocation remains a prototype setting, not approval
    of a future stacking methodology.
    """
    if not (0 < train_frac < 1 and 0 < test_frac < 1 and train_frac + test_frac < 1):
        raise ValueError("fractions must be positive and leave nonempty validation")
    anchors = anchor_indices(num_steps, history, horizon)
    n = len(anchors)
    n_test, n_train = round(n * test_frac), round(n * train_frac)
    n_val = n - n_test - n_train
    half = n_val // 2
    parts = [
        anchors[:n_train],
        anchors[n_train : n_train + half],
        anchors[n_train + half : n_train + n_val],
        anchors[n_train + n_val :],
    ]
    gap = horizon - 1
    parts = [a[:-gap] if gap else a for a in parts[:-1]] + parts[-1:]
    if any(len(a) == 0 for a in parts):
        raise ValueError("series/split is too small after target-boundary purging")
    return Splits(*parts)


def make_windows(
    data: np.ndarray, anchors: np.ndarray, history: int = 12, horizon: int = 12
) -> tuple[np.ndarray, np.ndarray]:
    """Slice (T,N) observations into (S,history,N) inputs and (S,horizon,N) targets."""
    data, anchors = np.asarray(data), np.asarray(anchors)
    anchor_indices(len(data), history, horizon)
    if data.ndim != 2 or anchors.ndim != 1 or not np.issubdtype(anchors.dtype, np.integer):
        raise ValueError("expected 2D data and a 1D integer anchor array")
    if np.any(anchors < history - 1) or np.any(anchors + horizon >= len(data)):
        raise ValueError("window anchors are outside valid series bounds")
    x_offsets, y_offsets = np.arange(-(history - 1), 1), np.arange(1, horizon + 1)
    return data[anchors[:, None] + x_offsets], data[anchors[:, None] + y_offsets]


def split_time_ranges(index: pd.DatetimeIndex, splits: Splits, horizon: int = 12) -> pd.DataFrame:
    """Record both anchor and target boundaries, so overlap is visible in audits."""
    return pd.DataFrame(
        [
            {
                "split": name,
                "first_anchor": index[a[0]],
                "last_anchor": index[a[-1]],
                "first_target": index[a[0] + 1],
                "last_target": index[a[-1] + horizon],
                "samples": len(a),
            }
            for name, a in splits.items()
        ]
    )
