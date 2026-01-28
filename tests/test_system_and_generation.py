from __future__ import annotations

"""Integration-style tests for system assembly and procedural generation.

These tests validate that:
- generated planets are well-formed and ordered,
- generated orbital parameters are positive,
- and stepping a SolarSystem advances planet phases.
"""


from helioforge import CentralBody, SolarSystem, generate_planets
from helioforge.constants import AU_M, DAY_S


def test_generate_planets_sorted_and_positive():
    """Generated planets should be sorted by distance and have valid parameters."""
    star = CentralBody(name="Star", mass_kg=1.0e30, radius_m=7.0e8, luminosity_w=0.0)
    planets = generate_planets(star, 10, seed=42, inner_au=0.5, outer_au=20.0)

    assert len(planets) == 10

    distances = [p.distance_m for p in planets]
    assert distances == sorted(distances)
    assert all(d > 0 for d in distances)

    assert all(p.period_s > 0 for p in planets)
    assert all(p.orbital_speed_mps > 0 for p in planets)

    # sanity: inner/outer bounds (allow jitter)
    assert distances[0] > 0.4 * AU_M
    assert distances[-1] < 25.0 * AU_M


def test_solar_system_step_moves_planets():
    """Stepping a SolarSystem should change at least one planet's phase."""
    star = CentralBody(name="Star", mass_kg=1.0e30, radius_m=7.0e8, luminosity_w=0.0)
    planets = generate_planets(star, 3, seed=1, inner_au=1.0, outer_au=2.0)
    system = SolarSystem(central_body=star, planets=planets)

    before = [p.phase_rad for p in system.planets]
    system.step(DAY_S)
    after = [p.phase_rad for p in system.planets]

    assert before != after
