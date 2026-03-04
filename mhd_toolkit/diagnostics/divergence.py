from __future__ import annotations

import numpy as np

from ..divfree.metrics import div_metrics


def divergence_report_2d(Bx: np.ndarray, By: np.ndarray, dx: float, dy: float) -> dict[str, float]:
    return div_metrics(Bx, By, dx, dy)
