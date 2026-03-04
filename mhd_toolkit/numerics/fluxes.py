from __future__ import annotations

import numpy as np


def rusanov_flux(UL: np.ndarray, UR: np.ndarray, FL: np.ndarray, FR: np.ndarray, smax: np.ndarray) -> np.ndarray:
    return 0.5 * (FL + FR) - 0.5 * smax * (UR - UL)
