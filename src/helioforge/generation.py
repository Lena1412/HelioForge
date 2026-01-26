from __future__ import annotations

import math
import random
from typing import List, Optional

from .constants import G, AU_M
from .models import CentralBody, Planet, PlanetType
from .kepler import Kepler


def kepler_period_s(semi_major_axis_m: float, central_mass_kg: float) -> float:
    """
    Kepler's third law (two-body approximation, orbiting mass negligible):
        T = 2π * sqrt(a^3 / (G * M))
    """
    if semi_major_axis_m <= 0:
        raise ValueError("semi_major_axis_m must be > 0")
    if central_mass_kg <= 0:
        raise ValueError("central_mass_kg must be > 0")
    return 2.0 * math.pi * math.sqrt((semi_major_axis_m**3) / (G * central_mass_kg))


def circular_orbit_speed_mps(distance_m: float, period_s: float) -> float:
    """Circular orbit speed v = 2πr / T."""
    if distance_m <= 0:
        raise ValueError("distance_m must be > 0")
    if period_s <= 0:
        raise ValueError("period_s must be > 0")
    return (2.0 * math.pi * distance_m) / period_s


def _pick_kind(distance_au: float) -> PlanetType:
    # Very simple rule of thumb; keep it minimal.
    if distance_au < 2.0:
        return "rocky"
    if distance_au < 8.0:
        return "gas_giant"
    if distance_au < 30.0:
        return "ice_giant"
    return "dwarf"


def _rand_range(rng: random.Random, lo: float, hi: float) -> float:
    return lo + (hi - lo) * rng.random()


def generate_planets(
    central_body: CentralBody,
    n_planets: int,
    *,
    seed: Optional[int] = None,
    inner_au: float = 0.4,
    outer_au: float = 40.0,
) -> List[Planet]:
    """
    Generate a list of planets with increasing orbital distances.

    Minimal rules:
    - distances increasing between inner_au and outer_au (log-spaced-ish)
    - kind determined by distance range
    - period from Kepler
    - speed from Kepler (circular orbit)
    """
    if n_planets < 0:
        raise ValueError("n_planets must be >= 0")
    if inner_au <= 0 or outer_au <= 0 or outer_au <= inner_au:
        raise ValueError("inner_au and outer_au must be > 0 and outer_au > inner_au")

    rng = random.Random(seed)

    if n_planets == 0:
        return []

    kep = Kepler(central_body.mass_kg)

    # Log-spaced baseline + small jitter keeps ordering stable and varied.
    log_inner = math.log(inner_au)
    log_outer = math.log(outer_au)

    planets: List[Planet] = []
    for i in range(n_planets):
        t = i / max(1, n_planets - 1)
        base_au = math.exp(log_inner + t * (log_outer - log_inner))
        jitter = _rand_range(rng, 0.93, 1.07)
        distance_au = base_au * jitter
        distance_m = distance_au * AU_M

        kind = _pick_kind(distance_au)

        # Simple mass/radius heuristics by type (intentionally rough).
        if kind == "rocky":
            mass_kg = _rand_range(rng, 0.05, 5.0) * 5.972e24
            radius_m = _rand_range(rng, 0.3, 1.5) * 6.371e6
        elif kind == "gas_giant":
            mass_kg = _rand_range(rng, 0.1, 3.0) * 1.898e27
            radius_m = _rand_range(rng, 0.7, 1.3) * 6.9911e7
        elif kind == "ice_giant":
            mass_kg = _rand_range(rng, 0.5, 2.0) * 8.681e25
            radius_m = _rand_range(rng, 0.7, 1.2) * 2.5362e7
        else:  # dwarf
            mass_kg = _rand_range(rng, 0.0001, 0.01) * 5.972e24
            radius_m = _rand_range(rng, 0.05, 0.3) * 6.371e6

        # Prefer native Kepler if available, fallback to Python inside Kepler wrapper.
        period_s = kep.period_s(distance_m)
        speed_mps = kep.circular_speed_mps(distance_m)

        phase_rad = _rand_range(rng, 0.0, 2.0 * math.pi)
        planets.append(
            Planet(
                name=f"Planet {i+1}",
                kind=kind,
                mass_kg=mass_kg,
                radius_m=radius_m,
                distance_m=distance_m,
                phase_rad=phase_rad,
                period_s=period_s,
                orbital_speed_mps=speed_mps,
            )
        )

    # Ensure sorted by orbital distance (jitter can cause tiny neighbor swaps).
    planets.sort(key=lambda p: p.distance_m)
    return planets
