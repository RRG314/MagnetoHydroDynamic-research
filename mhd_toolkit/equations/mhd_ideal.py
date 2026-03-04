from __future__ import annotations

from dataclasses import dataclass
import numpy as np


# Conservative variable ordering:
# [rho, mx, my, mz, Bx, By, Bz, E]
RHO = 0
MX = 1
MY = 2
MZ = 3
BX = 4
BY = 5
BZ = 6
ENE = 7
NVAR = 8


@dataclass(slots=True)
class IdealMHD:
    gamma: float = 1.4

    def pressure(self, U: np.ndarray) -> np.ndarray:
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        vy = U[MY] / rho
        vz = U[MZ] / rho
        kinetic = 0.5 * rho * (vx * vx + vy * vy + vz * vz)
        magnetic = 0.5 * (U[BX] * U[BX] + U[BY] * U[BY] + U[BZ] * U[BZ])
        p = (self.gamma - 1.0) * (U[ENE] - kinetic - magnetic)
        return np.maximum(p, 1e-9)

    def flux_x(self, U: np.ndarray) -> np.ndarray:
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        vy = U[MY] / rho
        vz = U[MZ] / rho
        bx, by, bz = U[BX], U[BY], U[BZ]
        p = self.pressure(U)
        b2 = bx * bx + by * by + bz * bz
        ptot = p + 0.5 * b2
        vdotb = vx * bx + vy * by + vz * bz

        F = np.zeros_like(U)
        F[RHO] = U[MX]
        F[MX] = U[MX] * vx + ptot - bx * bx
        F[MY] = U[MY] * vx - bx * by
        F[MZ] = U[MZ] * vx - bx * bz
        F[BX] = 0.0
        F[BY] = by * vx - bx * vy
        F[BZ] = bz * vx - bx * vz
        F[ENE] = (U[ENE] + ptot) * vx - bx * vdotb
        return F

    def flux_y(self, U: np.ndarray) -> np.ndarray:
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        vy = U[MY] / rho
        vz = U[MZ] / rho
        bx, by, bz = U[BX], U[BY], U[BZ]
        p = self.pressure(U)
        b2 = bx * bx + by * by + bz * bz
        ptot = p + 0.5 * b2
        vdotb = vx * bx + vy * by + vz * bz

        F = np.zeros_like(U)
        F[RHO] = U[MY]
        F[MX] = U[MX] * vy - by * bx
        F[MY] = U[MY] * vy + ptot - by * by
        F[MZ] = U[MZ] * vy - by * bz
        F[BX] = bx * vy - by * vx
        F[BY] = 0.0
        F[BZ] = bz * vy - by * vz
        F[ENE] = (U[ENE] + ptot) * vy - by * vdotb
        return F

    def max_speed_x(self, U: np.ndarray) -> np.ndarray:
        rho = np.maximum(U[RHO], 1e-12)
        vx = U[MX] / rho
        p = self.pressure(U)
        bx = U[BX]
        by = U[BY]
        bz = U[BZ]
        a2 = self.gamma * p / rho
        b2 = (bx * bx + by * by + bz * bz) / rho
        cax2 = bx * bx / rho
        disc = np.maximum((a2 + b2) ** 2 - 4.0 * a2 * cax2, 0.0)
        cf = np.sqrt(0.5 * (a2 + b2 + np.sqrt(disc)))
        return np.abs(vx) + cf

    def max_speed_y(self, U: np.ndarray) -> np.ndarray:
        rho = np.maximum(U[RHO], 1e-12)
        vy = U[MY] / rho
        p = self.pressure(U)
        bx = U[BX]
        by = U[BY]
        bz = U[BZ]
        a2 = self.gamma * p / rho
        b2 = (bx * bx + by * by + bz * bz) / rho
        cay2 = by * by / rho
        disc = np.maximum((a2 + b2) ** 2 - 4.0 * a2 * cay2, 0.0)
        cf = np.sqrt(0.5 * (a2 + b2 + np.sqrt(disc)))
        return np.abs(vy) + cf


def primitive_to_conservative(
    rho: np.ndarray,
    vx: np.ndarray,
    vy: np.ndarray,
    vz: np.ndarray,
    bx: np.ndarray,
    by: np.ndarray,
    bz: np.ndarray,
    p: np.ndarray,
    gamma: float = 1.4,
) -> np.ndarray:
    U = np.zeros((NVAR,) + rho.shape, dtype=float)
    U[RHO] = rho
    U[MX] = rho * vx
    U[MY] = rho * vy
    U[MZ] = rho * vz
    U[BX] = bx
    U[BY] = by
    U[BZ] = bz
    kinetic = 0.5 * rho * (vx * vx + vy * vy + vz * vz)
    magnetic = 0.5 * (bx * bx + by * by + bz * bz)
    U[ENE] = p / (gamma - 1.0) + kinetic + magnetic
    return U
