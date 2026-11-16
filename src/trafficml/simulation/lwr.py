"""Conservative Godunov/CTM dynamics for an illustrative two-merge corridor.

Six main cells 0..5, side cells 6/7. Signal A controls 1/6 -> 2;
signal B controls 3/7 -> 4. Inputs and parameters are synthetic, not calibrated.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Physics:
    cell_km: float = 0.25
    dt_seconds: float = 5.0
    free_speed_kmh: float = 60.0
    wave_speed_kmh: float = 20.0
    jam_density_veh_km: float = 150.0

    def __post_init__(self):
        if not all(np.isfinite(x) and x > 0 for x in vars(self).values()):
            raise ValueError("physics parameters must be positive and finite")
        if max(self.free_speed_kmh, self.wave_speed_kmh) * self.dt_hours / self.cell_km > 1:
            raise ValueError("CFL condition violated")

    @property
    def dt_hours(self):
        return self.dt_seconds / 3600

    @property
    def capacity(self):
        v, w = self.free_speed_kmh, self.wave_speed_kmh
        return v * w * self.jam_density_veh_km / (v + w)

    def demand_supply(self, vehicles):
        n = np.asarray(vehicles, dtype=float)
        if not np.isfinite(n).all() or (n < -1e-9).any():
            raise ValueError("invalid cell occupancy")
        jam = self.cell_km * self.jam_density_veh_km
        if (n > jam + 1e-9).any():
            raise ValueError("occupancy exceeds jam storage")
        density = np.maximum(n, 0) / self.cell_km
        demand = np.minimum(self.free_speed_kmh * density, self.capacity)
        supply = np.minimum(
            self.capacity, self.wave_speed_kmh * (self.jam_density_veh_km - density)
        )
        return demand, np.maximum(supply, 0)


def advance(physics, vehicles, queues, arrivals, phases, exit_capacity=None):
    """One simultaneous step; phase 0=main, 1=side, -1=all-red.

    Returns state, boundary queues, exited vehicles and a flow audit (veh/h).
    Arrivals are vehicles in this time step. Fractional occupancy is macroscopic.
    """
    n, q, a = [np.asarray(x, dtype=float) for x in (vehicles, queues, arrivals)]
    if n.shape != (8,) or q.shape != (3,) or a.shape != (3,):
        raise ValueError("expected eight cells and three source queues/arrivals")
    if not np.isfinite(q).all() or not np.isfinite(a).all() or (q < 0).any() or (a < 0).any():
        raise ValueError("invalid source queues/arrivals")
    if len(phases) != 2 or any(p not in [-1, 0, 1] for p in phases):
        raise ValueError("expected two mutually exclusive signal phases")
    cap = physics.capacity if exit_capacity is None else exit_capacity
    if not np.isfinite(cap) or not 0 <= cap <= physics.capacity:
        raise ValueError("exit capacity outside physical range")
    demand, supply = physics.demand_supply(n)
    inflow, outflow = np.zeros(8), np.zeros(8)
    audit = []
    edges = [(0, 1), (2, 3), (4, 5)]
    for phase, main, side, downstream in zip(phases, [1, 3], [6, 7], [2, 4], strict=True):
        if phase != -1:
            edges.append(((main if phase == 0 else side), downstream))
    for upstream, downstream in edges:
        flow = min(demand[upstream], supply[downstream])
        inflow[downstream] += flow
        outflow[upstream] += flow
        audit.append((upstream, downstream, flow))
    waiting = q + a
    admitted = np.minimum(waiting, supply[[0, 6, 7]] * physics.dt_hours)
    inflow[[0, 6, 7]] += admitted / physics.dt_hours
    outflow[5] = min(demand[5], cap)
    next_n = n + physics.dt_hours * (inflow - outflow)
    next_q = waiting - admitted
    departed = physics.dt_hours * outflow[5]
    jam = physics.cell_km * physics.jam_density_veh_km
    if not np.isfinite(next_n).all() or (next_n < -1e-8).any() or (next_n > jam + 1e-8).any():
        raise ArithmeticError("CTM state left physical bounds")
    if (next_q < -1e-8).any():
        raise ArithmeticError("negative external queue")
    if not np.all(outflow <= demand + 1e-8) or not np.all(inflow <= supply + 1e-8):
        raise ArithmeticError("sending/receiving capacity exceeded")
    mass_error = n.sum() + q.sum() + a.sum() - next_n.sum() - next_q.sum() - departed
    if abs(mass_error) > 1e-8:
        raise ArithmeticError("vehicle conservation violated")
    return (
        next_n,
        next_q,
        departed,
        {
            "edges": audit,
            "inflow": inflow,
            "outflow": outflow,
            "mass_error": float(mass_error),
            "source_admissions": admitted,
        },
    )
