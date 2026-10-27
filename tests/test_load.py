import os
import pickle

import pytest

from trafficml.data.load import load_dcrnn_adj


class _Evil:
    def __reduce__(self):
        return (os.getcwd, ())


def test_unpickler_blocks_non_numpy_globals(tmp_path):
    path = tmp_path / "evil.pkl"
    path.write_bytes(pickle.dumps(_Evil()))
    with pytest.raises(pickle.UnpicklingError, match="blocked"):
        load_dcrnn_adj(path)


def test_real_speed_shape_frequency_and_sensor_order():
    from conftest import GRAPH_DIR, SPEED_H5, require

    from trafficml.data.load import load_sensor_ids, load_speed

    ids = load_sensor_ids(require(GRAPH_DIR / "graph_sensor_ids.txt"))
    speed = load_speed(require(SPEED_H5), ids)
    assert speed.shape == (34272, 207)
    assert speed.index.is_unique and speed.index.is_monotonic_increasing
    with pytest.raises(ValueError, match="sensor_ids"):
        load_speed(SPEED_H5, ids[::-1])
