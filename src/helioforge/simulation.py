from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Dict, Tuple

from .system import SolarSystem


@dataclass(slots=True)
class Simulation:
    """
    Minimal simulation driver.

    Advances a SolarSystem and yields states for consumers (cosmoview/export).
    """
    system: SolarSystem
    time_s: float = 0.0

    def step(self, dt_s: float) -> None:
        self.system.step(dt_s)
        self.time_s += dt_s

    def iter_steps(self, dt_s: float) -> Iterator[Dict[str, Tuple[float, float]]]:
        """Infinite iterator producing planet positions each step."""
        while True:
            self.step(dt_s)
            yield self.system.state_m()
