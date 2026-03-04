from __future__ import annotations

import numpy as np

from ..numerics.timestep import cfl_dt_1d, cfl_dt_2d


def recommended_dt_1d(max_speed: np.ndarray, dx: float, cfl: float) -> float:
    return cfl_dt_1d(max_speed, dx, cfl)


def recommended_dt_2d(max_speed_x: np.ndarray, max_speed_y: np.ndarray, dx: float, dy: float, cfl: float) -> float:
    return cfl_dt_2d(max_speed_x, max_speed_y, dx, dy, cfl)
