from __future__ import annotations

from helioforge import CentralBody, Kepler, SolarSystem, generate_planets, make_solar_system
from helioforge.constants import AU_M, DAY_S, YEAR_S
from helioforge.export import save_json


def demo_random_system() -> None:
    star = CentralBody(name="DemoStar", mass_kg=1.2e30, radius_m=7.0e8, luminosity_w=2.0e26)

    # Check whether native module is available via wrapper behavior
    kep = Kepler(star.mass_kg)
    has_native = getattr(kep, "_native", None) is not None
    print(f"[Kepler] Native enabled: {has_native}")

    planets = generate_planets(star, 6, seed=123, inner_au=0.3, outer_au=25.0)
    system = SolarSystem(central_body=star, planets=planets)

    # Step simulation: 30 days with 1-day timestep
    dt = DAY_S
    for _ in range(30):
        system.step(dt)

    # Print a couple positions
    state = system.state_m()
    first_name = system.planets[0].name
    print(f"{first_name} position after 30 days (m): {state[first_name]}")

    # Export for later visualization
    save_json(system, "random_system.json")
    print("Saved random_system.json")


def demo_solar_system() -> None:
    sun, planets = make_solar_system()
    system = SolarSystem(central_body=sun, planets=planets)

    # Earth sanity: its orbital period should be about 1 year
    earth = next(p for p in planets if p.name == "Earth")
    print(f"Earth period (days): {earth.period_s / DAY_S:.2f}")
    print(f"Earth period (years): {earth.period_s / YEAR_S:.4f}")
    print(f"Earth distance (AU): {earth.distance_m / AU_M:.3f}")


if __name__ == "__main__":
    demo_random_system()
    print()
    demo_solar_system()
