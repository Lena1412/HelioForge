from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Dict, Any, Tuple

from .models import CentralBody, Planet


@dataclass(slots=True)
class SolarSystem:
    """A simple heliocentric system: one central body and a set of orbiting planets."""
    central_body: CentralBody
    planets: List[Planet]

    def step(self, dt_s: float) -> None:
        """Advance all planets by dt seconds."""
        for p in self.planets:
            p.step(dt_s)

    def state_m(self) -> Dict[str, Tuple[float, float]]:
        """
        Current positions in meters.
        Returns mapping planet_name -> (x_m, y_m)
        """
        return {p.name: p.position_m() for p in self.planets}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-friendly dict."""
        cb = self.central_body
        return {
            "central_body": {
                "name": cb.name,
                "mass_kg": cb.mass_kg,
                "radius_m": cb.radius_m,
                "luminosity_w": cb.luminosity_w,
            },
            "planets": [
                {
                    "name": p.name,
                    "kind": p.kind,
                    "mass_kg": p.mass_kg,
                    "radius_m": p.radius_m,
                    "distance_m": p.distance_m,
                    "phase_rad": p.phase_rad,
                    "period_s": p.period_s,
                    "orbital_speed_mps": p.orbital_speed_mps,
                }
                for p in self.planets
            ],
        }

    @staticmethod
    def from_planets(central_body: CentralBody, planets: Iterable[Planet]) -> "SolarSystem":
        """Convenience constructor to accept any iterable."""
        return SolarSystem(central_body=central_body, planets=list(planets))
