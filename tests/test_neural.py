"""Causal preprocessing, graph direction, missing loss and checkpoint contracts."""

import numpy as np
import pandas as pd
import pytest

from trafficml.data.neural import NeuralWindows


@pytest.fixture(scope="module")
def torch():
    """Keep preprocessing tests runnable without the neural model stack."""
    return pytest.importorskip("torch")


def test_training_only_scaling_and_causal_fill():
    index = pd.date_range("2012-01-01", periods=36, freq="5min")
    a = np.arange(72, dtype=np.float32).reshape(36, 2) + 1
    a[0:2, 0] = np.nan
    first = NeuralWindows(a, index, 15)
    a[20:] = 9000
    second = NeuralWindows(a, index, 15)
    assert first.state() == second.state()
    np.testing.assert_equal(first.x[0], second.x[0])
    restored = first.x[0, :, 0, 0] * first.scale + first.mean
    np.testing.assert_allclose(restored[:2], first.medians[0], rtol=1e-6)
    assert first.x[0, :2, 0, 1].tolist() == [1, 1]


def test_internal_fill_and_targets_not_imputed():
    a = np.ones((36, 2), dtype=np.float32) * 60
    a[5, 0], a[13, 0] = np.nan, np.nan
    d = NeuralWindows(a, pd.date_range("2012", periods=36, freq="5min"), 15)
    x, _, y = d.batch(np.array([11]))
    assert np.isfinite(x).all()
    assert np.isnan(y[0, 1, 0])
    assert x[0, 5, 0, 1] == 1


def test_attention_direction_and_self_loop(torch):
    from trafficml.models.neural import GraphAttention

    mask = torch.tensor([[1, 0], [1, 1]], dtype=torch.bool)
    layer = GraphAttention(4, 2, mask, dropout=0).eval()
    x = torch.randn(1, 2, 4)
    _, attention = layer(x, return_attention=True)
    assert torch.equal(attention[:, :, 0, 1], torch.zeros(1, 2))
    torch.testing.assert_close(attention.sum(-1), torch.ones(1, 2, 2))
    altered = x.clone()
    altered[:, 1] += 100
    torch.testing.assert_close(layer(x)[:, 0], layer(altered)[:, 0])
    assert not torch.allclose(layer(x)[:, 1], layer(altered)[:, 1])


def test_uniform_attention_is_exact_neighbour_average(torch):
    from trafficml.models.neural import GraphAttention

    mask = torch.tensor([[1, 0], [1, 1]], dtype=torch.bool)
    layer = GraphAttention(4, 2, mask, uniform=True, dropout=0).eval()
    x = torch.randn(1, 2, 4)
    _, attention = layer(x, return_attention=True)
    torch.testing.assert_close(attention[0, 0], torch.tensor([[1.0, 0.0], [0.5, 0.5]]))


def test_future_observations_do_not_change_current_features():
    index = pd.date_range("2012", periods=36, freq="5min")
    first = np.arange(72, dtype=np.float32).reshape(36, 2) + 1
    second = first.copy()
    second[20:] = 99999
    a = NeuralWindows(first, index, 15)
    b = NeuralWindows(second, index, 15)
    for left, right in zip(a.batch(np.array([18]))[:2], b.batch(np.array([18]))[:2], strict=True):
        np.testing.assert_array_equal(left, right)


def test_constructor_storage_does_not_expand_all_history_windows():
    values = np.full((2000, 8), 60, dtype=np.float32)
    index = pd.date_range("2012", periods=len(values), freq="5min")
    data = NeuralWindows(values, index, 1500)
    stored_bytes = sum(x.nbytes for x in vars(data).values() if isinstance(x, np.ndarray))
    assert stored_bytes < 6 * values.nbytes
    before = stored_bytes
    assert data.batch(np.array([11, 25]))[0].shape == (2, 12, 8, 2)
    assert sum(x.nbytes for x in vars(data).values() if isinstance(x, np.ndarray)) == before


@pytest.mark.parametrize("mode", ["temporal", "graph", "self", "uniform", "no_dropout"])
def test_shapes_gradient_and_checkpoint(mode, tmp_path, torch):
    from trafficml.models.neural import TrafficGRU, masked_loss

    model = TrafficGRU(3, hidden=8, mask=torch.ones(3, 3), mode=mode, dropout=0).eval()
    x, c = torch.randn(2, 12, 3, 2), torch.randn(2, 5)
    pred = model(x, c)
    assert pred.shape == (2, 12, 3)
    target = torch.randn_like(pred)
    target[0, 0, 0] = float("nan")
    loss = masked_loss(pred, target)
    loss.backward()
    assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
    path = tmp_path / "state.pt"
    torch.save(model.state_dict(), path)
    model.load_state_dict(torch.load(path, weights_only=True))
    torch.testing.assert_close(pred, model(x, c), rtol=0, atol=0)


def test_masked_loss_ignores_missing_and_empty(torch):
    from trafficml.models.neural import masked_loss

    p = torch.tensor([1.0, 4.0], requires_grad=True)
    assert masked_loss(p, torch.tensor([2.0, float("nan")])).item() == 1
    assert masked_loss(p, torch.full((2,), float("nan"))) is None


def test_csv_history_inference_matches_window_pipeline(torch):
    from predict_phase2 import predict_history

    from trafficml.models.neural import TrafficGRU

    torch.set_num_threads(1)
    rng = np.random.default_rng(7)
    values = rng.uniform(10, 70, (36, 3)).astype(np.float32)
    values[:2, 0] = np.nan
    values[5, 1] = np.nan
    index = pd.date_range("2012-03-01", periods=36, freq="5min")
    data = NeuralWindows(values, index, 15)
    model = TrafficGRU(3, hidden=8, mask=torch.ones(3, 3), mode="graph", dropout=0).eval()
    with torch.no_grad():
        model.head.weight.normal_(std=0.1)
    settings = {"history": 12, "horizon": 12, "hidden": 8, "heads": 2, "dropout": 0}
    manifest = {"sensor_ids": ["a", "b", "c"], "settings": settings, "normalization": data.state()}
    checkpoint = {"mode": "graph", "model": model.state_dict(), "normalization": data.state()}
    frame = pd.DataFrame(values[:12], index=index[:12], columns=manifest["sensor_ids"])
    inferred = predict_history(checkpoint, manifest, frame)
    x, c, _ = data.batch(np.array([11]))
    with torch.no_grad():
        expected = model(torch.from_numpy(x), torch.from_numpy(c))[0].numpy()
    np.testing.assert_allclose(inferred.values, expected * data.scale + data.mean, atol=2e-5)
    with pytest.raises(ValueError, match="order"):
        predict_history(checkpoint, manifest, frame.iloc[:, ::-1])
