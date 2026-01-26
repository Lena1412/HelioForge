from __future__ import annotations

"""helioforge.kepler

Keplerian orbital helpers with an optional native backend.

If `helioforge_native` is importable at runtime, this module will use a native
(C++-backed) solver for performance. Otherwise, it falls back to pure Python
formulas (sufficient for demos and small simulations).
"""

import math
from typing import Optional

from .constants import G


class Kepler:
    """Kepler computations with optional native acceleration.

    The class wraps two operations commonly used by the rest of the package:

    - orbital period from semi-major axis (distance)
    - circular orbit speed from orbital radius

    If `helioforge_native` is available, calls are delegated to the native
    solver for speed. Otherwise, pure Python math is used.

    Attributes:
        central_mass_kg: Mass of the central body in kilograms.
    """

    def __init__(self, central_mass_kg: float):
        """Create a Kepler helper for a given central mass.

        Args:
            central_mass_kg: Mass of the central body in kilograms.

        Raises:
            ValueError: If `central_mass_kg <= 0`.
        """
        if central_mass_kg <= 0:
            raise ValueError("central_mass_kg must be > 0")

        self.central_mass_kg = float(central_mass_kg)
        self._native: Optional[object] = None

        # Optional native acceleration. Any failure simply disables the native path.
        try:
            from helioforge_native import KeplerSolver  # type: ignore

            self._native = KeplerSolver(self.central_mass_kg)
        except Exception:
            self._native = None

    def period_s(self, semi_major_axis_m: float) -> float:
        """Compute orbital period for a given semi-major axis.

        Args:
            semi_major_axis_m: Semi-major axis in meters (for circular orbit, radius).

        Returns:
            Orbital period in seconds.

        Raises:
            ValueError: If `semi_major_axis_m <= 0`.
        """
        if semi_major_axis_m <= 0:
            raise ValueError("semi_major_axis_m must be > 0")

        if self._native is not None:
            return float(self._native.period_from_distance(float(semi_major_axis_m)))

        return 2.0 * math.pi * math.sqrt((semi_major_axis_m**3) / (G * self.central_mass_kg))

    def circular_speed_mps(self, distance_m: float) -> float:
        """Compute circular orbit speed at a given orbital radius.

        Args:
            distance_m: Orbital radius in meters.

        Returns:
            Orbital speed in meters per second.

        Raises:
            ValueError: If `distance_m <= 0`.
        """
        if distance_m <= 0:
            raise ValueError("distance_m must be > 0")

        if self._native is not None:
            return float(self._native.circular_speed_from_distance(float(distance_m)))

        # Circular orbit: v = sqrt(G*M/r)
        return math.sqrt((G * self.central_mass_kg) / distance_m)
