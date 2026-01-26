from __future__ import annotations

from typing import List, Tuple

from .constants import AU_M
from .kepler import Kepler
from .models import CentralBody, Planet


def make_solar_system() -> Tuple[CentralBody, List[Planet]]:
    """
    Return a simple, consistent example resembling our Solar System.

    Not a precision dataset — it exists for demos, notebooks, and sanity tests.
    """
    sun = CentralBody(
        name="Sun",
        mass_kg=1.9885e30,
        radius_m=6.9634e8,
        luminosity_w=3.828e26,
    )

    kep = Kepler(sun.mass_kg)

    # distance in AU; masses/radii are approximate
    specs = [
        ("Mercury", "rocky", 0.0553 * 5.972e24, 0.383 * 6.371e6, 0.387),
        ("Venus",   "rocky", 0.815  * 5.972e24, 0.949 * 6.371e6, 0.723),
        ("Earth",   "rocky", 1.0    * 5.972e24, 1.0   * 6.371e6, 1.000),
        ("Mars",    "rocky", 0.107  * 5.972e24, 0.532 * 6.371e6, 1.524),
        ("Jupiter", "gas_giant", 1.0 * 1.898e27, 1.0 * 6.9911e7, 5.204),
        ("Saturn",  "gas_giant", 0.299 * 1.898e27, 0.843 * 6.9911e7, 9.582),
        ("Uranus",  "ice_giant", 8.681e25, 2.5362e7, 19.201),
        ("Neptune", "ice_giant", 1.024e26, 2.4622e7, 30.047),
    ]

    planets: List[Planet] = []
    for name, kind, mass_kg, radius_m, distance_au in specs:
        distance_m = distance_au * AU_M
        period_s = kep.period_s(distance_m)
        speed_mps = kep.circular_speed_mps(distance_m)

        planets.append(
            Planet(
                name=name,
                kind=kind,  # type: ignore[arg-type]
                mass_kg=mass_kg,
                radius_m=radius_m,
                distance_m=distance_m,
                phase_rad=0.0,
                period_s=period_s,
                orbital_speed_mps=speed_mps,
            )
        )

    return sun, planets
