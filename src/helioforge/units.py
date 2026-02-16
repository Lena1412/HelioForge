# named helper initially and meant to hold many helper functions
# changed to only contain the unit helper

"""helioforge.units

Tiny unit/math helpers (kept minimal on purpose).

The project avoids a large units dependency; small numeric helpers live here.
"""

from __future__ import annotations


def clamp(x: float, lo: float, hi: float) -> float:
    """Clamp a value to a closed interval.

    Args:
        x: Input value.
        lo: Lower bound.
        hi: Upper bound.

    Returns:
        `x` clamped to the range [lo, hi].
    """
    return max(lo, min(hi, x))
