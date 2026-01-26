from __future__ import annotations

import math
import pytest

from helioforge.constants import AU_M, G
from helioforge.kepler import Kepler


def py_period(a_m: float, M_kg: float) -> float:
    return 2.0 * math.pi * math.sqrt((a_m**3) / (G * M_kg))


def py_circular_speed(a_m: float, M_kg: float) -> float:
    return math.sqrt((G * M_kg) / a_m)


def _native_solver_or_skip():
    try:
        import helioforge_native  # type: ignore
    except Exception:
        pytest.skip("helioforge_native not importable")

    solver = getattr(helioforge_native, "KeplerSolver", None)
    if solver is None:
        pytest.skip("helioforge_native imported but no KeplerSolver (shadowed module)")
    return solver


def test_kepler_wrapper_matches_formula():
    M = 1.9885e30
    a = 1.0 * AU_M
    k = Kepler(M)

    assert k.period_s(a) == pytest.approx(py_period(a, M), rel=1e-12)
    assert k.circular_speed_mps(a) == pytest.approx(py_circular_speed(a, M), rel=1e-12)


def test_kepler_native_matches_if_available():
    KeplerSolver = _native_solver_or_skip()

    M = 1.9885e30
    a = 1.0 * AU_M
    native = KeplerSolver(M)

    assert native.period_from_distance(a) == pytest.approx(py_period(a, M), rel=1e-10)
    assert native.circular_speed_from_distance(a) == pytest.approx(py_circular_speed(a, M), rel=1e-10)


def test_wrapper_uses_native_if_available():
    _native_solver_or_skip()

    k = Kepler(1.0e30)
    assert getattr(k, "_native", None) is not None
