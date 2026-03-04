from __future__ import annotations

import numpy as np

from mhd_toolkit.closures import ClosureContext, make_closure
from mhd_toolkit.equations.mhd_ideal import NVAR


def test_closure_shape_and_determinism() -> None:
    U = np.ones((NVAR, 32), dtype=float)
    ctx = ClosureContext(dx=0.01, dt=0.001)

    for name in ["ideal", "resistive", "viscous", "resistive+viscous"]:
        cl = make_closure(name, eta=1e-3, nu=1e-3)
        a = cl.apply_1d(U, ctx)
        b = cl.apply_1d(U, ctx)
        assert a.shape == U.shape
        assert np.allclose(a, b)
