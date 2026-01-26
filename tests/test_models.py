from __future__ import annotations

import math
import pytest

from helioforge.models import Planet


def test_planet_position_at_phase_zero():
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
