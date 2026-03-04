from __future__ import annotations

import numpy as np


def laplacian_1d(f: np.ndarray, dx: float) -> np.ndarray:
    return (np.roll(f, -1) - 2.0 * f + np.roll(f, 1)) / (dx * dx)


def laplacian_2d(f: np.ndarray, dx: float, dy: float) -> np.ndarray:
    dxx = (np.roll(f, -1, axis=0) - 2.0 * f + np.roll(f, 1, axis=0)) / (dx * dx)
    dyy = (np.roll(f, -1, axis=1) - 2.0 * f + np.roll(f, 1, axis=1)) / (dy * dy)
    return dxx + dyy
