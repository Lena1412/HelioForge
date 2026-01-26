from __future__ import annotations

import math
from typing import Optional

from .constants import G


class Kepler:
    """
    Kepler computations with optional native acceleration.

    - If helioforge_native is available, uses KeplerSolver (C++).
    - Otherwise falls back to pure Python formulas.
    """

    def __init__(self, central_mass_kg: float):
        if central_mass_kg <= 0:
            raise ValueError("central_mass_kg must be > 0")

        self.central_mass_kg = float(central_mass_kg)
        self._native: Optional[object] = None

        try:
            from helioforge_native import KeplerSolver  # type: ignore
            self._native = KeplerSolver(self.central_mass_kg)
        except Exception:
            self._native = None

    def period_s(self, semi_major_axis_m: float) -> float:
        if semi_major_axis_m <= 0:
            raise ValueError("semi_major_axis_m must be > 0")

        if self._native is not None:
            return float(self._native.period_from_distance(float(semi_major_axis_m)))

        return 2.0 * math.pi * math.sqrt((semi_major_axis_m**3) / (G * self.central_mass_kg))

    def circular_speed_mps(self, distance_m: float) -> float:
        if distance_m <= 0:
            raise ValueError("distance_m must be > 0")

        if self._native is not None:
            return float(self._native.circular_speed_from_distance(float(distance_m)))

        # Circular orbit: v = sqrt(G*M/r)
        return math.sqrt((G * self.central_mass_kg) / distance_m)
