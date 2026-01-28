from helioforge.constants import AU_M
from helioforge.kepler import Kepler

"""
Purpose: Low-level Kepler usage (Python or native)

Shows:
- direct Kepler computations
- no system or planets involved
"""

k = Kepler(1.9885e30)
period = k.period_s(1.0 * AU_M)
speed = k.circular_speed_mps(1.0 * AU_M)

print("Period (s):", period)
print("Speed (m/s):", speed)
