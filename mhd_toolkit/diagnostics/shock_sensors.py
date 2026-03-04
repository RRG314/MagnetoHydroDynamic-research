from __future__ import annotations

import numpy as np

from ..equations.mhd_ideal import RHO


def density_gradient_sensor_1d(U: np.ndarray, dx: float) -> np.ndarray:
    rho = U[RHO]
    return np.abs(np.roll(rho, -1) - np.roll(rho, 1)) / (2.0 * dx)


def density_gradient_sensor_2d(U: np.ndarray, dx: float, dy: float) -> np.ndarray:
    rho = U[RHO]
    gx = (np.roll(rho, -1, axis=0) - np.roll(rho, 1, axis=0)) / (2.0 * dx)
    gy = (np.roll(rho, -1, axis=1) - np.roll(rho, 1, axis=1)) / (2.0 * dy)
    return np.sqrt(gx * gx + gy * gy)
