from __future__ import annotations

"""Tests for Kepler-law computations and the optional native backend.

These tests validate:
- the pure Python formulas,
- the Kepler wrapper class behavior,
- and (if available) the native `helioforge_native` implementation.
"""

import math
import pytest

from helioforge.constants import AU_M, G
from helioforge.kepler import Kepler


def py_period(a_m: float, M_kg: float) -> float:
    """Compute orbital period using the reference Python formula.

    Args:
        a_m: Semi-major axis (meters).
        M_kg: Central body mass (kilograms).

    Returns:
        Orbital period in seconds.
    """
    return 2.0 * math.pi * math.sqrt((a_m**3) / (G * M_kg))


def py_circular_speed(a_m: float, M_kg: float) -> float:
    """Compute circular-orbit speed using the reference Python formula.

    Args:
        a_m: Orbital radius (meters).
        M_kg: Central body mass (kilograms).

    Returns:
        Orbital speed in meters per second.
    """
    return math.sqrt((G * M_kg) / a_m)


def _native_solver_or_skip():
    """Return the native KeplerSolver class if available, otherwise skip the test.

    This helper is used to conditionally run native-backend tests only when
    `helioforge_native` is importable and exposes `KeplerSolver`.

    Returns:
        The `helioforge_native.KeplerSolver` class.

    Raises:
        pytest.SkipTest: If the native module/class is not available.
    """
    try:
        import helioforge_native  # type: ignore
    except Exception:
        pytest.skip("helioforge_native not importable")

    solver = getattr(helioforge_native, "KeplerSolver", None)
    if solver is None:
        pytest.skip("helioforge_native imported but no KeplerSolver (shadowed module)")
    return solver


def test_kepler_wrapper_matches_formula():
    """Kepler wrapper should match the analytical two-body formulas."""
    M = 1.9885e30
    a = 1.0 * AU_M
    k = Kepler(M)

    assert k.period_s(a) == pytest.approx(py_period(a, M), rel=1e-12)
    assert k.circular_speed_mps(a) == pytest.approx(py_circular_speed(a, M), rel=1e-12)


def test_kepler_native_matches_if_available():
    """Native KeplerSolver should match the analytical formulas (when present)."""
    KeplerSolver = _native_solver_or_skip()

    M = 1.9885e30
    a = 1.0 * AU_M
    native = KeplerSolver(M)

    assert native.period_from_distance(a) == pytest.approx(py_period(a, M), rel=1e-10)
    assert native.circular_speed_from_distance(a) == pytest.approx(py_circular_speed(a, M), rel=1e-10)


def test_wrapper_uses_native_if_available():
    """Kepler wrapper should initialize and store a native solver when available."""
    _native_solver_or_skip()

    k = Kepler(1.0e30)
    assert getattr(k, "_native", None) is not None
