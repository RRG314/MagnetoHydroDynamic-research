from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .base import Closure, ClosureContext
from ..equations.induction import laplacian_1d, laplacian_2d
from ..equations.mhd_ideal import MX, MY, MZ, RHO


@dataclass(slots=True)
class ViscousClosure(Closure):
    """Simple Laplacian viscosity over velocity components, mapped back to momentum."""

    nu: float = 0.0
    name: str = "viscous"

    def apply_1d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        src = np.zeros_like(U)
        if self.nu <= 0.0:
            return src
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        vy = U[MY] / rho
        vz = U[MZ] / rho
        src[MX] = self.nu * rho * laplacian_1d(vx, context.dx)
        src[MY] = self.nu * rho * laplacian_1d(vy, context.dx)
        src[MZ] = self.nu * rho * laplacian_1d(vz, context.dx)
        return src

    def apply_2d(self, U: np.ndarray, context: ClosureContext) -> np.ndarray:
        src = np.zeros_like(U)
        if self.nu <= 0.0:
            return src
        if context.dy is None:
            raise ValueError("dy is required for 2D viscous closure")
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        vy = U[MY] / rho
        vz = U[MZ] / rho
        src[MX] = self.nu * rho * laplacian_2d(vx, context.dx, context.dy)
        src[MY] = self.nu * rho * laplacian_2d(vy, context.dx, context.dy)
        src[MZ] = self.nu * rho * laplacian_2d(vz, context.dx, context.dy)
        return src
