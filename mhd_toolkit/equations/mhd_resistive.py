from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .induction import laplacian_1d, laplacian_2d
from .mhd_ideal import BY, BZ, ENE, IdealMHD


@dataclass(slots=True)
class ResistiveMHD:
    gamma: float = 1.4
    eta: float = 1e-3

    def ideal(self) -> IdealMHD:
        return IdealMHD(gamma=self.gamma)

    def source_1d(self, U: np.ndarray, dx: float) -> np.ndarray:
        src = np.zeros_like(U)
        lap_by = laplacian_1d(U[BY], dx)
        lap_bz = laplacian_1d(U[BZ], dx)
        src[BY] = self.eta * lap_by
        src[BZ] = self.eta * lap_bz
        src[ENE] = self.eta * (lap_by * lap_by + lap_bz * lap_bz)
        return src

    def source_2d(self, U: np.ndarray, dx: float, dy: float) -> np.ndarray:
        src = np.zeros_like(U)
        lap_by = laplacian_2d(U[BY], dx, dy)
        lap_bz = laplacian_2d(U[BZ], dx, dy)
        src[BY] = self.eta * lap_by
        src[BZ] = self.eta * lap_bz
        src[ENE] = self.eta * (lap_by * lap_by + lap_bz * lap_bz)
        return src
