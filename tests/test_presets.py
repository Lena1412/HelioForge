from __future__ import annotations

"""Tests for preset system builders (e.g., a rough Solar System)."""

import pytest

from helioforge import SolarSystem, make_solar_system
from helioforge.constants import DAY_S, YEAR_S


def test_make_solar_system_has_earth_and_reasonable_period():
    """The Solar System preset should include Earth with an ~1-year period."""
    sun, planets = make_solar_system()
    system = SolarSystem(central_body=sun, planets=planets)

    earth = next(p for p in system.planets if p.name == "Earth")
    # Earth ~ 1 year (allow some tolerance since we use simplified constants/model)
    assert earth.period_s == pytest.approx(YEAR_S, rel=0.02)

    # and stepping changes phase
    phase0 = earth.phase_rad
    system.step(DAY_S)
    assert earth.phase_rad != phase0
