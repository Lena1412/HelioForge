from helioforge import CentralBody, SolarSystem
from helioforge.constants import DAY_S
from helioforge.generation import generate_planets
from helioforge.simulation import Simulation

'''
Purpose: Smallest possible end-to-end HelioForge usage

Shows:
- manual system creation
- simulation stepping
- reading positions
'''

star = CentralBody(
    name="DemoStar",
    mass_kg=1.0e30,
    radius_m=7.0e8,
    luminosity_w=0.0,
)

planets = generate_planets(star, 4, seed=1)
system = SolarSystem(star, planets)
sim = Simulation(system)

for day in range(5):
    sim.step(DAY_S)
    print(f"Day {day + 1}")
    for name, pos in sim.system.state_m().items():
        print(f"  {name}: {pos}")
