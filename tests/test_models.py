

"""Tests for core data models.

These tests focus on `Planet` behavior:
- converting phase + distance to a 2D position,
- advancing phase over time,
- and validating time-step input.
"""
from __future__ import annotations

import math

import pytest

from helioforge.models import Planet


def test_planet_position_at_phase_zero():
    """At phase 0, the planet should lie on the +X axis at (distance, 0)."""
    p = Planet(
        name="P",
        kind="rocky",
        mass_kg=1.0,
        radius_m=1.0,
        distance_m=10.0,
        phase_rad=0.0,
        period_s=100.0,
        orbital_speed_mps=0.0,
    )
    x, y = p.position_m()
    assert x == pytest.approx(10.0)
    assert y == pytest.approx(0.0)


def test_planet_step_advances_phase():
    """`step()` should advance phase by ω * dt for the stored period."""
    p = Planet(
        name="P",
        kind="rocky",
        mass_kg=1.0,
        radius_m=1.0,
        distance_m=10.0,
        phase_rad=0.0,
        period_s=100.0,
        orbital_speed_mps=0.0,
    )

    dt = 5.0
    omega = 2.0 * math.pi / 100.0
    p.step(dt)
    assert p.phase_rad == pytest.approx(omega * dt)


def test_planet_step_rejects_negative_dt():
    """`step()` should reject negative time steps with a ValueError."""
    p = Planet(
        name="P",
        kind="rocky",
        mass_kg=1.0,
        radius_m=1.0,
        distance_m=10.0,
        phase_rad=0.0,
        period_s=100.0,
        orbital_speed_mps=0.0,
    )
    with pytest.raises(ValueError):
        p.step(-1.0)
