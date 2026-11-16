"""Numerical/behavioural invariants for synthetic LWR and local agents."""

import numpy as np
import pytest

from trafficml.simulation.agents import Observation, ResponsiveSignal
from trafficml.simulation.experiment import simulate
from trafficml.simulation.lwr import Physics, advance


def test_cfl_and_invalid_physics():
    with pytest.raises(ValueError, match="CFL"):
        Physics(dt_seconds=60)
    with pytest.raises(ValueError, match="positive"):
        Physics(wave_speed_kmh=-1)
    assert Physics().capacity == 2250


def test_red_blocks_both_competing_movements():
    p = Physics()
    n = np.array([0, 10, 0, 10, 0, 0, 10, 10], float)
    updated, q, departed, audit = advance(p, n, np.zeros(3), np.zeros(3), [-1, -1])
    np.testing.assert_array_equal(updated, n)
    assert q.sum() == departed == 0
    assert audit["mass_error"] == 0


def test_single_green_and_downstream_spillback():
    p = Physics()
    n = np.zeros(8)
    n[[1, 6]] = 10
    updated, _, _, audit = advance(p, n, np.zeros(3), np.zeros(3), [0, -1])
    assert updated[1] < n[1] and updated[6] == n[6]
    n[2] = p.cell_km * p.jam_density_veh_km
    _, _, _, blocked = advance(p, n, np.zeros(3), np.zeros(3), [0, -1])
    assert blocked["outflow"][1] == 0
    assert audit["outflow"][6] == 0


def test_full_source_retains_arrivals_without_loss():
    p = Physics()
    n = np.full(8, p.cell_km * p.jam_density_veh_km)
    updated, queued, departed, audit = advance(p, n, np.zeros(3), np.array([4, 3, 2]), [-1, -1], 0)
    np.testing.assert_allclose(updated, n)
    np.testing.assert_allclose(queued, [4, 3, 2])
    assert departed == 0 and abs(audit["mass_error"]) < 1e-9


def test_closed_system_conservation_and_bounds_over_many_steps():
    p = Physics()
    rng = np.random.default_rng(44)
    n = rng.uniform(0, p.cell_km * p.jam_density_veh_km, 8)
    q = np.zeros(3)
    total = n.sum()
    for t in range(200):
        n, q, departed, _ = advance(p, n, q, np.zeros(3), [t % 2, (t + 1) % 2], 0)
        assert departed == 0
        assert abs(n.sum() + q.sum() - total) < 1e-9
        assert (n >= -1e-9).all() and n.max() <= 37.5 + 1e-9


def test_responsive_min_max_green_and_clearance():
    agent = ResponsiveSignal(4, 12, 2)
    actions = [agent.act(t, Observation(1, 20, 0)) for t in range(50)]
    assert actions[:4] == [0] * 4
    assert actions[4:6] == [-1, -1]
    assert actions[6:18] == [1] * 12
    assert actions[18:20] == [-1, -1]
    # Even a perpetually preferred side approach cannot suppress the other indefinitely.
    assert actions[20:24] == [0] * 4


def test_empty_network_and_reproducible_matched_run():
    cfg = {
        **vars(Physics()),
        "fixed_green_seconds": 40,
        "clearance_seconds": 5,
        "min_green_seconds": 20,
        "max_green_seconds": 60,
        "switch_margin_vehicles": 2,
    }
    a = np.zeros((120, 3))
    cap = np.full(120, Physics().capacity)
    for policy in ["fixed", "responsive"]:
        result, trace = simulate(cfg, a, cap, policy)
        assert result["system_vehicle_minutes"] == result["departed_vehicles"] == 0
        assert not trace["cells"].any()
    a[:40] = np.random.default_rng(3).poisson(1, (40, 3))
    first, x = simulate(cfg, a, cap, "responsive")
    second, y = simulate(cfg, a, cap, "responsive")
    assert first == second
    np.testing.assert_array_equal(x["cells"], y["cells"])
    assert first["max_conservation_error_vehicles"] < 1e-7
