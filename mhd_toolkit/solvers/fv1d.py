from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from ..closures import ClosureContext, make_closure
from ..config import SolverConfig
from ..equations.mhd_ideal import IdealMHD
from ..numerics.fluxes import rusanov_flux
from ..numerics.recon import plm_reconstruct_1d
from ..numerics.timestep import cfl_dt_1d


@dataclass
class FV1DSolver:
    config: SolverConfig
    x: np.ndarray
    U: np.ndarray

    def __post_init__(self) -> None:
        self.eqn = IdealMHD(gamma=self.config.gamma)
        self.closure = make_closure(self.config.closure, eta=self.config.eta, nu=self.config.nu)
        self.dx = float(self.x[1] - self.x[0])
        self.time = 0.0

    def step(self, dt: float | None = None) -> float:
        U = self.U
        uL_cell, uR_cell = plm_reconstruct_1d(U)

        UL = uR_cell
        UR = np.roll(uL_cell, -1, axis=1)

        FL = self.eqn.flux_x(UL)
        FR = self.eqn.flux_x(UR)
        smax = np.maximum(self.eqn.max_speed_x(UL), self.eqn.max_speed_x(UR))[None, :]
        F = rusanov_flux(UL, UR, FL, FR, smax)

        max_speed = self.eqn.max_speed_x(U)
        if dt is None:
            dt = cfl_dt_1d(max_speed, self.dx, self.config.cfl)

        self.U = U - (dt / self.dx) * (F - np.roll(F, 1, axis=1))

        src = self.closure.apply_1d(self.U, ClosureContext(dx=self.dx, dt=dt))
        self.U = self.U + dt * src
        self.time += dt
        return dt

    def run(self, *, t_end: float | None = None, steps: int | None = None, diagnostics=None) -> dict:
        if t_end is None and steps is None:
            raise ValueError("Either t_end or steps must be provided")
        n = 0
        dts: list[float] = []
        while True:
            if steps is not None and n >= steps:
                break
            if t_end is not None and self.time >= t_end:
                break
            dt = self.step()
            dts.append(dt)
            n += 1
            if diagnostics is not None:
                diagnostics.observe(self.U, self.time, self.dx)
        return {
            "num_steps": n,
            "time": self.time,
            "dt_min": float(np.min(dts)) if dts else 0.0,
            "dt_max": float(np.max(dts)) if dts else 0.0,
        }
