# src/cosmoview/scaling.py
from __future__ import annotations

"""cosmoview.scaling

World-to-screen scaling helpers.

CosmoView renders astronomical distances on a finite screen. To keep the view
usable across very different orbit sizes, it uses a logarithmic mapping:
    px = log(1 + r/base) * pixels_per_log_unit * zoom

This preserves visual separation for inner orbits while still allowing very
large outer orbits to fit on screen.
"""

import math


class ScaleModel:
    """Logarithmic scaling model for mapping meters to pixels.

    Attributes:
        pixels_per_log_unit: Multiplier for the log-scaled value.
        base_m: Base distance (in meters) that controls where the log curve
            starts to compress distances.
    """

    def __init__(self, pixels_per_log_unit: float = 180.0, base_m: float = 1.0e9):
        """Create a ScaleModel.

        Args:
            pixels_per_log_unit: Controls how quickly distances expand in pixels.
            base_m: Base distance in meters used inside `log1p(r/base_m)`.

        Raises:
            ValueError: If `pixels_per_log_unit <= 0` or `base_m <= 0`.
        """
        if pixels_per_log_unit <= 0:
            raise ValueError("pixels_per_log_unit must be > 0")
        if base_m <= 0:
            raise ValueError("base_m must be > 0")

        self.pixels_per_log_unit = float(pixels_per_log_unit)
        self.base_m = float(base_m)

    def meters_to_pixels_radius(self, r_m: float, zoom: float) -> float:
        """Convert a world-space radius (meters) to a screen-space radius (pixels).

        Args:
            r_m: Radius/distance in meters.
            zoom: User zoom multiplier.

        Returns:
            Radius in pixels.

        Raises:
            ValueError: If `r_m < 0` or `zoom <= 0`.
        """
        if r_m < 0:
            raise ValueError("r_m must be >= 0")
        if zoom <= 0:
            raise ValueError("zoom must be > 0")

        v = math.log1p(r_m / self.base_m)
        return v * self.pixels_per_log_unit * zoom

    @staticmethod
    def clamp_radius_px(r_px: float, min_px: float, max_px: float) -> float:
        """Clamp a pixel radius to a sensible drawing range.

        This is used to keep bodies visible even when zoomed far out and to
        avoid comically large circles when zoomed far in.

        Args:
            r_px: Input radius in pixels.
            min_px: Minimum allowed radius in pixels.
            max_px: Maximum allowed radius in pixels.

        Returns:
            Clamped radius in pixels.
        """
        return max(min_px, min(max_px, r_px))
