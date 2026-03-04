from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class ClosureContext:
    dx: float
    dy: float | None = None
    dt: float = 0.0


class Closure:
    name: str = "base"

    def apply_1d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        return np.zeros_like(U)

    def apply_2d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        return np.zeros_like(U)
