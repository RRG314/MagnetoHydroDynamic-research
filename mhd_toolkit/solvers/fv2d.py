from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from ..closures import ClosureContext, make_closure
from ..config import SolverConfig
from ..divfree.glm import clean_B_glm
from ..divfree.projection import clean_B_projection
from ..equations.mhd_ideal import BX, BY, IdealMHD
from ..numerics.fluxes import rusanov_flux
from ..numerics.timestep import cfl_dt_2d


@dataclass
class FV2DSolver:
    config: SolverConfig
    x: np.ndarray
    y: np.ndarray
    U: np.ndarray

    def __post_init__(self) -> None:
        self.eqn = IdealMHD(gamma=self.config.gamma)
        self.closure = make_closure(self.config.closure, eta=self.config.eta, nu=self.config.nu)
        self.dx = float(self.x[1] - self.x[0])
        self.dy = float(self.y[1] - self.y[0])
        self.time = 0.0
        self.psi = np.zeros_like(self.U[BX])

    def _x_sweep(self, U: np.ndarray, dt: float) -> np.ndarray:
        UL = U
        UR = np.roll(U, -1, axis=1)
        FL = self.eqn.flux_x(UL)
        FR = self.eqn.flux_x(UR)
        sL = self.eqn.max_speed_x(UL)
        sR = self.eqn.max_speed_x(UR)
        smax = np.maximum(sL, sR)[None, :, :]
        Fx = rusanov_flux(UL, UR, FL, FR, smax)
        return U - (dt / self.dx) * (Fx - np.roll(Fx, 1, axis=1))

    def _y_sweep(self, U: np.ndarray, dt: float) -> np.ndarray:
        UL = U
        UR = np.roll(U, -1, axis=2)
        FL = self.eqn.flux_y(UL)
        FR = self.eqn.flux_y(UR)
        sL = self.eqn.max_speed_y(UL)
        sR = self.eqn.max_speed_y(UR)
        smax = np.maximum(sL, sR)[None, :, :]
        Fy = rusanov_flux(UL, UR, FL, FR, smax)
        return U - (dt / self.dy) * (Fy - np.roll(Fy, 1, axis=2))

    def _divfree_clean(self, U: np.ndarray, dt: float) -> tuple[np.ndarray, dict[str, float] | None]:
        mode = self.config.divfree.lower()
        if mode == "projection":
            bx_new, by_new, report = clean_B_projection(U[BX], U[BY], self.dx, self.dy, periodic=self.config.periodic)
            U[BX] = bx_new
            U[BY] = by_new
            return U, report
        if mode == "glm":
            bx_new, by_new, psi_new, report = clean_B_glm(
                U[BX],
                U[BY],
                self.psi,
                self.dx,
                self.dy,
                dt,
                ch=self.config.glm_ch,
                cp=self.config.glm_cp,
            )
            U[BX] = bx_new
            U[BY] = by_new
            self.psi = psi_new
            return U, report
        return U, None

    def step(self, dt: float | None = None) -> tuple[float, dict[str, float] | None]:
        speed_x = self.eqn.max_speed_x(self.U)
        speed_y = self.eqn.max_speed_y(self.U)
        if dt is None:
            dt = cfl_dt_2d(speed_x, speed_y, self.dx, self.dy, self.config.cfl)

        U_half = self._x_sweep(self.U, 0.5 * dt)
        U_new = self._y_sweep(U_half, dt)
        U_new = self._x_sweep(U_new, 0.5 * dt)

        src = self.closure.apply_2d(U_new, ClosureContext(dx=self.dx, dy=self.dy, dt=dt))
        U_new = U_new + dt * src

        U_new, clean_report = self._divfree_clean(U_new, dt)
        self.U = U_new
        self.time += dt
        return dt, clean_report

    def run(self, *, t_end: float | None = None, steps: int | None = None, diagnostics=None) -> dict:
        if t_end is None and steps is None:
            raise ValueError("Either t_end or steps must be provided")
        n = 0
        dts: list[float] = []
        clean_reports = []
        while True:
            if steps is not None and n >= steps:
                break
            if t_end is not None and self.time >= t_end:
                break
            dt, report = self.step()
            dts.append(dt)
            if report is not None:
                clean_reports.append(report)
            n += 1
            if diagnostics is not None:
                diagnostics.observe(self.U, self.time, self.dx, self.dy)

        return {
            "num_steps": n,
            "time": self.time,
            "dt_min": float(np.min(dts)) if dts else 0.0,
            "dt_max": float(np.max(dts)) if dts else 0.0,
            "divfree_reports": clean_reports,
        }
