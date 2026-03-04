from __future__ import annotations

import numpy as np

from mhd_toolkit.config import SolverConfig
from mhd_toolkit.solvers.fv1d import FV1DSolver
from mhd_toolkit.solvers.fv2d import FV2DSolver
from mhd_toolkit.tests.problems import brio_wu, orszag_tang


def test_fv1d_runs_without_nans() -> None:
    x, U = brio_wu.initial_state(128, gamma=1.4)
    solver = FV1DSolver(SolverConfig(closure="ideal", divfree="none", gamma=1.4), x, U)
    summary = solver.run(steps=5)
    assert summary["num_steps"] == 5
    assert np.isfinite(solver.U).all()


def test_fv2d_runs_without_nans() -> None:
    x, y, U = orszag_tang.initial_state(48, 48, gamma=5.0 / 3.0)
    solver = FV2DSolver(SolverConfig(closure="ideal", divfree="glm", gamma=5.0 / 3.0), x, y, U)
    summary = solver.run(steps=5)
    assert summary["num_steps"] == 5
    assert np.isfinite(solver.U).all()
