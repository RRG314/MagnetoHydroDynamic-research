from __future__ import annotations

import numpy as np

from ...equations.mhd_ideal import primitive_to_conservative


def initial_state(nx: int, ny: int, *, gamma: float = 5.0 / 3.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-1.0, 1.0, nx, endpoint=False) + 1.0 / nx
    y = np.linspace(-1.0, 1.0, ny, endpoint=False) + 1.0 / ny
    X, Y = np.meshgrid(x, y, indexing="ij")

    rho = np.ones_like(X)
    p = 0.2 * np.ones_like(X)
    vx = np.zeros_like(X)
    vy = np.zeros_like(X)
    vz = np.zeros_like(X)

    bx = np.tanh(Y / 0.1)
    by = 0.05 * np.sin(2.0 * np.pi * X)
    bz = np.zeros_like(X)

    U = primitive_to_conservative(rho, vx, vy, vz, bx, by, bz, p, gamma=gamma)
    return x, y, U
