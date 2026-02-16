# models of the celestial bodies (stars and planets)
# initially split into two separate files for each class (sol_core and world_shard)
# later combined into one file initially named celestial_bodies
# name changed to make it shorter and simpler
# the planet types are based solely on the distance from the central star
# and only change the color of the planet when it is displayed

"""helioforge.models

Core data models for helioforge's simple heliocentric simulation.

The project intentionally models planets as moving on circular 2D orbits
to keep the system easy to understand and fast to simulate/visualize.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal, Tuple

PlanetType = Literal["rocky", "gas_giant", "ice_giant", "dwarf"]


@dataclass(frozen=True, slots=True)
class CentralBody:
    """Central body for the heliocentric model (e.g., a star).

    Luminosity is optional because not every central body has a meaningful value
    in the contexts helioforge targets (demos/simulation).

    Attributes:
        name: Human-readable identifier.
        mass_kg: Mass in kilograms.
        radius_m: Radius in meters.
        luminosity_w: Luminosity in watts (optional; defaults to 0.0).
    """

    name: str
    mass_kg: float
    radius_m: float
    luminosity_w: float = 0.0


# Convenience alias for readability in solar-system examples.
Sun = CentralBody


@dataclass(slots=True)
class Planet:
    """A planet on a circular 2D orbit around the central body.

    Orbit definition:
    - distance_m: orbital radius (semi-major axis a) in meters
    - phase_rad: current orbital angle in radians
    - period_s: orbital period in seconds
    - orbital_speed_mps: speed along the orbit in m/s

    Note:
        This model is intentionally simplified (2D + circular orbit). Consumers
        that need positions call `position_m()` and simulations advance with `step()`.

    Attributes:
        name: Planet name.
        kind: Planet type category (rocky/gas_giant/ice_giant/dwarf).
        mass_kg: Mass in kilograms.
        radius_m: Radius in meters.
        distance_m: Orbital radius in meters.
        phase_rad: Current orbital phase in radians.
        period_s: Orbital period in seconds.
        orbital_speed_mps: Orbital speed in meters per second.
    """

    name: str
    kind: PlanetType
    mass_kg: float
    radius_m: float

    distance_m: float
    phase_rad: float = 0.0

    period_s: float = field(default=0.0)
    orbital_speed_mps: float = field(default=0.0)

    def angular_speed_rad_s(self) -> float:
        """Compute angular speed in radians per second.

        Formula:
            ω = 2π / T

        Returns:
            Angular speed in rad/s.

        Raises:
            ValueError: If `period_s <= 0`.
        """
        if self.period_s <= 0.0:
            raise ValueError("Planet.period_s must be > 0")
        return (2.0 * math.pi) / self.period_s

    def position_m(self) -> Tuple[float, float]:
        """Get 2D Cartesian position in meters.

        Returns:
            Tuple (x_m, y_m) representing the current position on the orbital plane.
        """
        x = self.distance_m * math.cos(self.phase_rad)
        y = self.distance_m * math.sin(self.phase_rad)
        return (x, y)

    def step(self, dt_s: float) -> None:
        """Advance the planet's orbital phase by a time step.

        Args:
            dt_s: Time step in seconds.

        Raises:
            ValueError: If `dt_s < 0`.
        """
        if dt_s < 0:
            raise ValueError("dt_s must be >= 0")

        # Use modulo to keep phase bounded in [0, 2π), preventing growth over time.
        self.phase_rad = (self.phase_rad + self.angular_speed_rad_s() * dt_s) % (
            2.0 * math.pi
        )

    def recalc_speed_from_period(self) -> None:
        """Recompute circular-orbit speed from the stored orbital period.

        Formula:
            v = 2πr / T

        Raises:
            ValueError: If `period_s <= 0`.
        """
        if self.period_s <= 0.0:
            raise ValueError("Planet.period_s must be > 0")
        self.orbital_speed_mps = (2.0 * math.pi * self.distance_m) / self.period_s
