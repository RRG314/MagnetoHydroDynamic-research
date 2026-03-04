from __future__ import annotations

from mhd_toolkit.diagnostics import Diagnostics
from mhd_toolkit.tests.problems import brio_wu, orszag_tang


def test_diagnostics_keys_and_nonnegative_energies() -> None:
    x, U1 = brio_wu.initial_state(64, gamma=1.4)
    dx = float(x[1] - x[0])
    d1 = Diagnostics(dim=1)
    r1 = d1.observe(U1, time=0.0, dx=dx)
    for key in ["mass", "kinetic_energy", "magnetic_energy", "total_energy"]:
        assert key in r1
        assert r1[key] >= 0.0

    x, y, U2 = orszag_tang.initial_state(32, 32, gamma=5.0 / 3.0)
    d2 = Diagnostics(dim=2)
    r2 = d2.observe(U2, time=0.0, dx=float(x[1] - x[0]), dy=float(y[1] - y[0]))
    for key in ["l2_divB", "max_abs_divB", "normalized_l2_divB", "total_energy"]:
        assert key in r2
        assert r2[key] >= 0.0
