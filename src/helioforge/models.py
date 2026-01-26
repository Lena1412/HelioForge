from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Literal, Tuple


PlanetType = Literal["rocky", "gas_giant", "ice_giant", "dwarf"]


@dataclass(frozen=True, slots=True)
class CentralBody:
    """
    Central body for the heliocentric model (star, etc.).

    Luminosity is optional because not every central body has a meaningful value.
    """
    name: str
    mass_kg: float
    radius_m: float
    luminosity_w: float = 0.0


# Convenience alias for readability in solar-system examples.
Sun = CentralBody


@dataclass(slots=True)
class Planet:
    """
    A planet on a circular 2D orbit around the central body.

    Orbit definition:
    - distance_m: orbital radius (semi-major axis a) in meters
    - phase_rad: current angle in radians
    - period_s: orbital period in seconds
    - orbital_speed_mps: speed along the orbit in m/s
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
        """Angular speed ω = 2π / T (rad/s)."""
        if self.period_s <= 0.0:
            raise ValueError("Planet.period_s must be > 0")
        return (2.0 * math.pi) / self.period_s

    def position_m(self) -> Tuple[float, float]:
        """2D Cartesian position (x, y) in meters."""
        x = self.distance_m * math.cos(self.phase_rad)
        y = self.distance_m * math.sin(self.phase_rad)
        return (x, y)

    def step(self, dt_s: float) -> None:
        """Advance the planet by dt seconds."""
        if dt_s < 0:
            raise ValueError("dt_s must be >= 0")
        self.phase_rad = (self.phase_rad + self.angular_speed_rad_s() * dt_s) % (2.0 * math.pi)

    def recalc_speed_from_period(self) -> None:
        """Set orbital_speed_mps for a circular orbit using v = 2πr / T."""
        if self.period_s <= 0.0:
            raise ValueError("Planet.period_s must be > 0")
        self.orbital_speed_mps = (2.0 * math.pi * self.distance_m) / self.period_s
