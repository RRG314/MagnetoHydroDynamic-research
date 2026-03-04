from __future__ import annotations

import numpy as np

from ...equations.mhd_ideal import primitive_to_conservative


def initial_state(nx: int, *, gamma: float = 2.0) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(0.0, 1.0, nx, endpoint=False) + 0.5 / nx
    left = x < 0.5

    rho = np.where(left, 1.0, 0.125)
    p = np.where(left, 1.0, 0.1)
    vx = np.zeros_like(x)
    vy = np.zeros_like(x)
    vz = np.zeros_like(x)
    bx = np.full_like(x, 0.75)
    by = np.where(left, 1.0, -1.0)
    bz = np.zeros_like(x)

    U = primitive_to_conservative(rho, vx, vy, vz, bx, by, bz, p, gamma=gamma)
    return x, U
