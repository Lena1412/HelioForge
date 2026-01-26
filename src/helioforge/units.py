"""Tiny unit helpers (kept minimal on purpose)."""

from __future__ import annotations


def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp x to [lo, hi]."""
    return max(lo, min(hi, x))
