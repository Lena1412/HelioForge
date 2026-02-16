# this file did not exist initially
# it was added in order not to define the constants multiple times
# and to make the project seem more professional

"""helioforge.constants

Defines physical constants used across helioforge.

These values are kept in a dedicated module to:
- avoid duplication,
- provide a single source of truth for shared constants,
- keep formulas readable in other modules.
"""

# Gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Astronomical Unit (m) - used for convenience in examples/generation
AU_M = 1.495978707e11

# Day and year in seconds (for convenience)
DAY_S = 86_400.0
YEAR_S = 365.25 * DAY_S
