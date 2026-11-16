"""Two local rule-based signal agents; no learned policy or stability guarantee."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    main_vehicles: float
    side_vehicles: float
    downstream_vehicles: float


class FixedSignal:
    def __init__(self, green_steps, clearance_steps, offset=0):
        if green_steps < 1 or clearance_steps < 1:
            raise ValueError("positive green and clearance required")
        self.green, self.clearance, self.offset = green_steps, clearance_steps, offset

    def act(self, step, observation):
        cycle = 2 * (self.green + self.clearance)
        t = (step + self.offset) % cycle
        if t < self.green:
            return 0
        if t < self.green + self.clearance:
            return -1
        return 1 if t < 2 * self.green + self.clearance else -1


class ResponsiveSignal:
    def __init__(self, minimum_steps, maximum_steps, clearance_steps, margin=2.0):
        if not 1 <= minimum_steps <= maximum_steps or clearance_steps < 1 or margin < 0:
            raise ValueError("invalid timing/margin")
        self.minimum, self.maximum, self.clearance = minimum_steps, maximum_steps, clearance_steps
        self.margin = margin
        self.phase, self.age, self.remaining = 0, 0, 0

    def act(self, step, observation):
        if self.remaining:
            self.remaining -= 1
            return -1
        own = [observation.main_vehicles, observation.side_vehicles]
        pressure = [max(x - observation.downstream_vehicles, 0.0) for x in own]
        other = 1 - self.phase
        request = pressure[other] > pressure[self.phase] + self.margin
        request |= own[self.phase] < 1e-9 and own[other] > 1e-9
        switch = self.age >= self.maximum or (self.age >= self.minimum and request)
        if switch:
            self.phase, self.age = other, 0
            self.remaining = self.clearance - 1
            return -1
        self.age += 1
        return self.phase
