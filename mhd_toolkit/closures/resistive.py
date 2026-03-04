from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .base import Closure, ClosureContext
from ..equations.induction import laplacian_1d, laplacian_2d
from ..equations.mhd_ideal import BY, BZ, ENE


@dataclass(slots=True)
class ResistiveClosure(Closure):
    eta: float = 1e-3
    name: str = "resistive"

    def apply_1d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        src = np.zeros_like(U)
        lap_by = laplacian_1d(U[BY], context.dx)
        lap_bz = laplacian_1d(U[BZ], context.dx)
        src[BY] = self.eta * lap_by
        src[BZ] = self.eta * lap_bz
        src[ENE] = self.eta * (lap_by * lap_by + lap_bz * lap_bz)
        return src

    def apply_2d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        if context.dy is None:
            raise ValueError("dy is required for 2D resistive closure")
        src = np.zeros_like(U)
        lap_by = laplacian_2d(U[BY], context.dx, context.dy)
        lap_bz = laplacian_2d(U[BZ], context.dx, context.dy)
        src[BY] = self.eta * lap_by
        src[BZ] = self.eta * lap_bz
        src[ENE] = self.eta * (lap_by * lap_by + lap_bz * lap_bz)
        return src
