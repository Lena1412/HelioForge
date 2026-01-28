from __future__ import annotations

"""helioforge.system

Defines the SolarSystem container and serialization helpers.

The SolarSystem class owns:
- one `CentralBody`,
- a list of orbiting `Planet` objects,
and provides stepping + a JSON-friendly representation.
"""

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple

from .models import CentralBody, Planet


@dataclass(slots=True)
class SolarSystem:
    """A simple heliocentric system: one central body and orbiting planets.

    Attributes:
        central_body: The star/central mass.
        planets: A list of planets orbiting the central body.
    """

    central_body: CentralBody
    planets: List[Planet]

    def step(self, dt_s: float) -> None:
        """Advance all planets by `dt_s` seconds.

        Args:
            dt_s: Time step in seconds.
        """
        for p in self.planets:
            p.step(dt_s)

    def state_m(self) -> Dict[str, Tuple[float, float]]:
        """Get current planet positions in meters.

        Returns:
            Dict mapping `planet_name -> (x_m, y_m)`.
        """
        return {p.name: p.position_m() for p in self.planets}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SolarSystem":
        """Construct a SolarSystem from a JSON-friendly dict produced by `to_dict()`.

        Args:
            data: Dictionary representation of a SolarSystem.

        Returns:
            A SolarSystem instance.

        Raises:
            KeyError: If expected keys are missing.
        """
        from .models import (  # local import to avoid cycles in some setups
            CentralBody,
            Planet,
        )

        cb = data["central_body"]
        central = CentralBody(
            name=cb["name"],
            mass_kg=cb["mass_kg"],
            radius_m=cb["radius_m"],
            luminosity_w=cb.get("luminosity_w", 0.0),
        )

        planets = []
        for p in data["planets"]:
            planets.append(
                Planet(
                    name=p["name"],
                    kind=p["kind"],
                    mass_kg=p["mass_kg"],
                    radius_m=p["radius_m"],
                    distance_m=p["distance_m"],
                    phase_rad=p.get("phase_rad", 0.0),
                    period_s=p.get("period_s", 0.0),
                    orbital_speed_mps=p.get("orbital_speed_mps", 0.0),
                )
            )

        return SolarSystem(central_body=central, planets=planets)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the system to a JSON-friendly dictionary.

        Returns:
            A dict containing central body properties and a list of planet dicts.
        """
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
    def from_planets(
        central_body: CentralBody, planets: Iterable[Planet]
    ) -> "SolarSystem":
        """Construct a SolarSystem from any iterable of planets.

        Args:
            central_body: The star/central mass.
            planets: Any iterable producing `Planet` objects.

        Returns:
            A SolarSystem containing `central_body` and a list of planets.
        """
        return SolarSystem(central_body=central_body, planets=list(planets))
