from __future__ import annotations

import numpy as np


def cfl_dt_1d(max_speed: np.ndarray, dx: float, cfl: float) -> float:
    s = float(np.max(max_speed))
    if s <= 1e-14:
        return 1e-6
    return cfl * dx / s


def cfl_dt_2d(max_speed_x: np.ndarray, max_speed_y: np.ndarray, dx: float, dy: float, cfl: float) -> float:
    sx = float(np.max(max_speed_x))
    sy = float(np.max(max_speed_y))
    denom = sx / dx + sy / dy
    if denom <= 1e-14:
        return 1e-6
    return cfl / denom
