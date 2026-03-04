from __future__ import annotations

import numpy as np

from ...equations.mhd_ideal import primitive_to_conservative


def initial_state(nx: int, ny: int, *, gamma: float = 5.0 / 3.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(0.0, 1.0, nx, endpoint=False) + 0.5 / nx
    y = np.linspace(0.0, 1.0, ny, endpoint=False) + 0.5 / ny
    X, Y = np.meshgrid(x, y, indexing="ij")

    rho = np.full_like(X, 25.0 / (36.0 * np.pi))
    p = np.full_like(X, 5.0 / (12.0 * np.pi))
    vx = -np.sin(2.0 * np.pi * Y)
    vy = np.sin(2.0 * np.pi * X)
    vz = np.zeros_like(X)
    bx = -np.sin(2.0 * np.pi * Y) / np.sqrt(4.0 * np.pi)
    by = np.sin(4.0 * np.pi * X) / np.sqrt(4.0 * np.pi)
    bz = np.zeros_like(X)

    U = primitive_to_conservative(rho, vx, vy, vz, bx, by, bz, p, gamma=gamma)
    return x, y, U
