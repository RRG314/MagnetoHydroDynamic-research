from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SolverConfig:
    gamma: float = 1.4
    cfl: float = 0.35
    closure: str = "ideal"
    divfree: str = "none"
    eta: float = 1e-3
    nu: float = 0.0
    glm_ch: float = 1.0
    glm_cp: float = 0.1
    periodic: bool = True
    output_dir: str = "results"
