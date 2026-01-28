from helioforge import SolarSystem, make_solar_system
from helioforge.constants import DAY_S

'''
Purpose: Show built-in Solar System preset

Shows:
- using make_solar_system
- stepping the system
- accessing planet objects
'''

sun, planets = make_solar_system()
system = SolarSystem(sun, planets)

system.step(DAY_S)

for p in system.planets:
    print(p.name, p.position_m())