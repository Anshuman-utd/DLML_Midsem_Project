import numpy as np
import pandas as pd
import pytest

from trafficml.data.splits import anchor_indices, chronological_split, make_windows


def test_purged_partition_sizes():
    s = chronological_split(34272)
    assert len(anchor_indices(34272)) == 34249
    assert [len(a) for _, a in s.items()] == [23963, 1701, 1702, 6850]
    assert sum(len(a) for _, a in s.items()) == 34249 - 3 * 11


@pytest.mark.parametrize("horizon", [1, 3, 12, 24])
def test_every_partition_target_ends_before_next_forecast(horizon):
    parts = [a for _, a in chronological_split(1000, horizon=horizon).items()]
    for earlier, later in zip(parts, parts[1:], strict=False):
        assert earlier[-1] + horizon <= later[0]
        early_targets = set((earlier[:, None] + np.arange(1, horizon + 1)).ravel())
        late_targets = set((later[:, None] + np.arange(1, horizon + 1)).ravel())
        assert not early_targets & late_targets


@pytest.mark.parametrize(
    "kw",
    [
        dict(test_frac=0),
        dict(test_frac=1),
        dict(train_frac=0),
        dict(train_frac=0.9, test_frac=0.2),
        dict(history=0),
        dict(horizon=-1),
        dict(num_steps=25),
    ],
)
def test_invalid_partition_settings_fail(kw):
    params = {"num_steps": 1000, **kw}
    with pytest.raises(ValueError):
        chronological_split(**params)


def test_targets_and_history_are_bounded_and_causal():
    data = np.arange(100, dtype=float)[:, None]
    x, y = make_windows(data, np.array([11, 50]))
    assert x.shape == (2, 12, 1) and y.shape == (2, 12, 1)
    np.testing.assert_array_equal(x[1, :, 0], np.arange(39, 51))
    np.testing.assert_array_equal(y[1, :, 0], np.arange(51, 63))
    for invalid in [np.array([-1]), np.array([99]), np.array([11.5])]:
        with pytest.raises(ValueError):
            make_windows(data, invalid)


def test_future_validation_changes_cannot_change_fitted_profile(monkeypatch):
    from run_baselines import fit_training_profile

    values = np.arange(1000, dtype=float)[:, None] + 1
    index = pd.date_range("2012-03-01", periods=1000, freq="5min")
    splits = chronological_split(1000)
    before = fit_training_profile(values, index, splits, 12).table_
    # Mutate every observation after the first validation forecast origin.
    changed = values.copy()
    changed[splits.val_tune[0] + 1 :] = 1e6
    after = fit_training_profile(changed, index, splits, 12).table_
    np.testing.assert_array_equal(before, after)
