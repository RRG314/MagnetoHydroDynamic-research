from __future__ import annotations

import numpy as np


def divergence_2d(Bx: np.ndarray, By: np.ndarray, dx: float, dy: float) -> np.ndarray:
    dBx = (np.roll(Bx, -1, axis=0) - np.roll(Bx, 1, axis=0)) / (2.0 * dx)
    dBy = (np.roll(By, -1, axis=1) - np.roll(By, 1, axis=1)) / (2.0 * dy)
    return dBx + dBy


def div_metrics(Bx: np.ndarray, By: np.ndarray, dx: float, dy: float) -> dict[str, float]:
    divB = divergence_2d(Bx, By, dx, dy)
    l2 = float(np.sqrt(np.mean(divB * divB)))
    mx = float(np.max(np.abs(divB)))
    bmag = np.sqrt(np.mean(Bx * Bx + By * By) + 1e-12)
    return {
        "l2_divB": l2,
        "max_abs_divB": mx,
        "normalized_l2_divB": float(l2 / bmag),
    }
