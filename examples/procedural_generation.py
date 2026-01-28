from helioforge import CentralBody
from helioforge.constants import AU_M
from helioforge.generation import generate_planets

"""
Purpose: Demonstrate deterministic procedural generation

Shows:
- seed usage
- inner/outer bounds
- planet metadata
"""

star = CentralBody(
    name="ProceduralStar",
    mass_kg=1.2e30,
    radius_m=7.0e8,
    luminosity_w=0.0,
)

planets = generate_planets(
    star,
    n_planets=6,
    seed=42,
    inner_au=0.5,
    outer_au=25.0,
)

for p in planets:
    print(
        f"{p.name:8} | " f"type={p.kind:10} | " f"distance={p.distance_m / AU_M:.2f} AU"
    )
