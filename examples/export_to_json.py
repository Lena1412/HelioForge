from helioforge import SolarSystem, make_solar_system
from helioforge.export import save_json

"""
Purpose: JSON export

Shows:
- exporting a system
- zero visualization dependencies
"""

sun, planets = make_solar_system()
system = SolarSystem(sun, planets)

save_json(system, "solar_system.json")
