import numpy as np
import pandas as pd
import pytest

from trafficml.features.temporal import SensorFeatures
from trafficml.models.trees import fit_predict_sensor


def test_features_are_causal_and_training_fit_is_fixed():
    values = np.arange(100, dtype=float)
    index = pd.date_range("2012-01-01", periods=100, freq="5min")
    f = SensorFeatures().fit(values[:30])
    before = f.transform(values, index, np.array([20, 29]))
    changed = values.copy()
    changed[30:] = 1e6
    np.testing.assert_array_equal(before, f.transform(changed, index, np.array([20, 29])))
    assert f.median_ == 14.5
    assert before.shape == (2, len(f.names))
    assert before[0, 0] == 20 and before[0, 11] == 9
    assert before[0, 24] == 19  # trailing mean of [18,19,20]


def test_missing_fill_is_left_to_right_only_and_has_flags():
    f = SensorFeatures(3).fit(np.array([10.0, 20.0, 30.0]))
    x = f.transform(
        np.array([np.nan, 40.0, np.nan]),
        pd.date_range("2012-01-01", periods=3, freq="5min"),
        np.array([2]),
    )
    np.testing.assert_array_equal(x[0, :3], [40.0, 40.0, 20.0])
    np.testing.assert_array_equal(x[0, 3:6], [1.0, 0.0, 1.0])
    assert np.isfinite(x).all()


@pytest.mark.parametrize("kind", ["rf", "xgb"])
def test_trees_use_training_labels_only_and_save_reusable_models(kind, tmp_path):
    rng = np.random.default_rng(42)
    x = rng.normal(size=(200, 3)).astype(np.float32)
    y = np.column_stack([2 * x[:, 0], 3 * x[:, 0]]).astype(np.float32)
    y[0, 0] = np.nan
    params = {"n_estimators": 5, "max_depth": 2}
    pred, record = fit_predict_sensor(
        kind, x, y, x[:4], np.full((4, 2), 7.0), params, min_rows=10, model_dir=tmp_path / kind
    )
    assert pred.shape == (4, 2) and np.isfinite(pred).all()
    assert record["valid_training_rows"][0] == 199
    assert record["valid_training_rows"][1] == (199 if kind == "rf" else 200)
    assert len(list((tmp_path / kind).iterdir())) == (1 if kind == "rf" else 2)
    # A saved estimator must reproduce its original predictions after loading.
    if kind == "rf":
        import joblib

        restored = joblib.load(tmp_path / kind / "forest.joblib").predict(x[:4])
    else:
        from xgboost import XGBRegressor

        columns = []
        for h in [1, 2]:
            model = XGBRegressor()
            model.load_model(tmp_path / kind / f"h{h:02d}.ubj")
            columns.append(model.predict(x[:4]))
        restored = np.column_stack(columns)
    np.testing.assert_allclose(restored, pred, rtol=1e-6)


def test_sparse_training_uses_explicit_fallback():
    pred, record = fit_predict_sensor(
        "rf",
        np.ones((3, 2)),
        np.ones((3, 2)),
        np.ones((2, 2)),
        np.full((2, 2), 7.0),
        {"n_estimators": 2},
        min_rows=100,
    )
    assert np.all(pred == 7) and record["fallback_horizons"] == [1, 2]
