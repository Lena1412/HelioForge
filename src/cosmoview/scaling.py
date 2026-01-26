# src/cosmoview/scaling.py
from __future__ import annotations

import math


class ScaleModel:
    def __init__(self, pixels_per_log_unit: float = 180.0, base_m: float = 1.0e9):
        if pixels_per_log_unit <= 0:
            raise ValueError("pixels_per_log_unit must be > 0")
        if base_m <= 0:
            raise ValueError("base_m must be > 0")

        self.pixels_per_log_unit = float(pixels_per_log_unit)
        self.base_m = float(base_m)

    def meters_to_pixels_radius(self, r_m: float, zoom: float) -> float:
        if r_m < 0:
            raise ValueError("r_m must be >= 0")
        if zoom <= 0:
            raise ValueError("zoom must be > 0")

        v = math.log1p(r_m / self.base_m)
        return v * self.pixels_per_log_unit * zoom

    @staticmethod
    def clamp_radius_px(r_px: float, min_px: float, max_px: float) -> float:
        return max(min_px, min(max_px, r_px))
