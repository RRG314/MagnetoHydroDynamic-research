from __future__ import annotations

import numpy as np

from ..equations.mhd_ideal import BX, BY, BZ, ENE, MX, MY, MZ, RHO


def totals_1d(U: np.ndarray, dx: float) -> dict[str, float]:
    rho = np.maximum(U[RHO], 1e-12)
    vx = U[MX] / rho
    vy = U[MY] / rho
    vz = U[MZ] / rho
    kinetic = 0.5 * rho * (vx * vx + vy * vy + vz * vz)
    magnetic = 0.5 * (U[BX] * U[BX] + U[BY] * U[BY] + U[BZ] * U[BZ])
    return {
        "mass": float(np.sum(U[RHO]) * dx),
        "momentum_x": float(np.sum(U[MX]) * dx),
        "momentum_y": float(np.sum(U[MY]) * dx),
        "momentum_z": float(np.sum(U[MZ]) * dx),
        "kinetic_energy": float(np.sum(kinetic) * dx),
        "magnetic_energy": float(np.sum(magnetic) * dx),
        "total_energy": float(np.sum(U[ENE]) * dx),
    }


def totals_2d(U: np.ndarray, dx: float, dy: float) -> dict[str, float]:
    rho = np.maximum(U[RHO], 1e-12)
    vx = U[MX] / rho
    vy = U[MY] / rho
    vz = U[MZ] / rho
    kinetic = 0.5 * rho * (vx * vx + vy * vy + vz * vz)
    magnetic = 0.5 * (U[BX] * U[BX] + U[BY] * U[BY] + U[BZ] * U[BZ])
    cell = dx * dy
    return {
        "mass": float(np.sum(U[RHO]) * cell),
        "momentum_x": float(np.sum(U[MX]) * cell),
        "momentum_y": float(np.sum(U[MY]) * cell),
        "momentum_z": float(np.sum(U[MZ]) * cell),
        "kinetic_energy": float(np.sum(kinetic) * cell),
        "magnetic_energy": float(np.sum(magnetic) * cell),
        "total_energy": float(np.sum(U[ENE]) * cell),
    }
