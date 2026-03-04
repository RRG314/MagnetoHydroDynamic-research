from __future__ import annotations

import numpy as np


def minmod(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a)
    mask = a * b > 0.0
    out[mask] = np.sign(a[mask]) * np.minimum(np.abs(a[mask]), np.abs(b[mask]))
    return out


def plm_reconstruct_1d(u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return left/right interface states for cell-centered array u[nvar, nx]."""
    du_l = u - np.roll(u, 1, axis=1)
    du_r = np.roll(u, -1, axis=1) - u
    slope = minmod(du_l, du_r)
    uL = u + 0.5 * slope
    uR = u - 0.5 * slope
    return uL, uR
