from __future__ import annotations

"""helioforge.simulation

High-level simulation driver.

This module provides a small wrapper around `SolarSystem` that:
- advances time,
- exposes an iterator interface for consumers like viewers/exporters.
"""

from dataclasses import dataclass
from typing import Iterator, Dict, Tuple

from .system import SolarSystem


@dataclass(slots=True)
class Simulation:
    """Minimal simulation driver.

    This class advances a SolarSystem in fixed timesteps and provides an iterator
    for consumers that want a stream of states (e.g., visualization, export).

    Attributes:
        system: The SolarSystem being simulated.
        time_s: Current simulation time in seconds.
    """

    system: SolarSystem
    time_s: float = 0.0

    def step(self, dt_s: float) -> None:
        """Advance the simulation by `dt_s` seconds.

        Args:
            dt_s: Time step in seconds.
        """
        self.system.step(dt_s)
        self.time_s += dt_s

    def iter_steps(self, dt_s: float) -> Iterator[Dict[str, Tuple[float, float]]]:
        """Iterate indefinitely, yielding planet positions each step.

        This is intended for "pull-based" consumers (e.g., a render loop)
        that want the latest state on demand.

        Args:
            dt_s: Time step in seconds used for each iteration.

        Yields:
            A mapping from planet name to `(x_m, y_m)` position in meters.
        """
        while True:
            self.step(dt_s)
            yield self.system.state_m()
