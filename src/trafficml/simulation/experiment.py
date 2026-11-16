"""Frozen synthetic demand and matched two-agent experiments; no score tuning."""

from __future__ import annotations

import numpy as np

from trafficml.simulation.agents import FixedSignal, Observation, ResponsiveSignal
from trafficml.simulation.lwr import Physics, advance


def steps(seconds, dt):
    value = seconds / dt
    if not np.isfinite(value) or value <= 0 or abs(value - round(value)) > 1e-9:
        raise ValueError("durations must be positive multiples of dt")
    return int(round(value))


def demand_schedule(settings, scenario):
    dt = settings["dt_seconds"]
    count = steps(60 * (settings["demand_minutes"] + settings["drain_minutes"]), dt)
    minutes = np.arange(count) * dt / 60
    rate = np.zeros((count, 3))
    active = minutes < settings["demand_minutes"]
    if scenario == "balanced":
        rate[active] = [800, 200, 200]
    elif scenario == "arterial_peak":
        rate[active] = [800, 200, 200]
        rate[(minutes >= 15) & (minutes < 45) & active] = [1100, 300, 300]
    elif scenario == "side_peak":
        rate[active] = [600, 250, 250]
        rate[(minutes >= 15) & (minutes < 45) & active] = [600, 650, 650]
    elif scenario == "downstream_restriction":
        rate[active] = [900, 300, 300]
    else:
        raise ValueError("unknown scenario")
    physics = Physics(**{k: settings[k] for k in Physics.__dataclass_fields__})
    capacities = np.full(count, physics.capacity)
    if scenario == "downstream_restriction":
        capacities[(minutes >= 25) & (minutes < 40)] = 900
    return rate, capacities


def simulate(settings, arrivals, capacities, policy):
    physics = Physics(**{k: settings[k] for k in Physics.__dataclass_fields__})
    dt = physics.dt_seconds
    arrivals, capacities = np.asarray(arrivals), np.asarray(capacities)
    if arrivals.ndim != 2 or arrivals.shape[1] != 3 or capacities.shape != (len(arrivals),):
        raise ValueError("arrival/capacity time grids differ")
    if not len(arrivals):
        raise ValueError("empty time grid")
    clearance = steps(settings["clearance_seconds"], dt)
    if policy == "fixed":
        green = steps(settings["fixed_green_seconds"], dt)
        agents = [FixedSignal(green, clearance, offset) for offset in [0, green + clearance]]
    elif policy == "responsive":
        agents = [
            ResponsiveSignal(
                steps(settings["min_green_seconds"], dt),
                steps(settings["max_green_seconds"], dt),
                clearance,
                settings["switch_margin_vehicles"],
            )
            for _ in range(2)
        ]
    else:
        raise ValueError("unknown policy")
    cells = np.zeros((len(arrivals) + 1, 8))
    queues = np.zeros((len(arrivals) + 1, 3))
    phases = np.zeros((len(arrivals), 2), dtype=int)
    departures = np.zeros(len(arrivals))
    max_error, max_step_error = 0.0, 0.0
    arrived = departed = 0.0
    for t, (a, cap) in enumerate(zip(arrivals, capacities, strict=True)):
        n = cells[t]
        for j, (main, side, downstream) in enumerate([(1, 6, 2), (3, 7, 4)]):
            phases[t, j] = agents[j].act(t, Observation(n[main], n[side], n[downstream]))
        cells[t + 1], queues[t + 1], departures[t], audit = advance(
            physics, n, queues[t], a, phases[t], cap
        )
        arrived += a.sum()
        departed += departures[t]
        error = abs(arrived - departed - cells[t + 1].sum() - queues[t + 1].sum())
        max_error = max(max_error, error)
        max_step_error = max(max_step_error, abs(audit["mass_error"]))
    if max_error > 1e-7:
        raise ArithmeticError("cumulative conservation failed")
    # Trapezoidal state integration; boundary admissions occur at step boundaries.
    occupancy = cells.sum(axis=1) + queues.sum(axis=1)
    boundary = queues.sum(axis=1)
    tts = np.trapezoid(occupancy, dx=dt / 60)
    waiting = np.trapezoid(boundary, dx=dt / 60)
    switches = sum(
        np.count_nonzero((phases[1:, j] == -1) & (phases[:-1, j] != -1)) for j in range(2)
    )
    result = {
        "arrived_vehicles": float(arrived),
        "departed_vehicles": float(departed),
        "residual_vehicles": float(occupancy[-1]),
        "system_vehicle_minutes": float(tts),
        "boundary_wait_vehicle_minutes": float(waiting),
        "mean_boundary_queue_vehicles": float(waiting / (len(arrivals) * dt / 60)),
        "max_total_boundary_queue_vehicles": float(boundary.max()),
        "switches": int(switches),
        "max_conservation_error_vehicles": float(max_error),
        "max_step_conservation_error_vehicles": float(max_step_error),
        "max_cell_density_veh_km": float(cells.max() / physics.cell_km),
    }
    return result, {
        "cells": cells,
        "queues": queues,
        "phases": phases,
        "departures": departures,
        "arrivals": arrivals,
        "exit_capacity": capacities,
    }
