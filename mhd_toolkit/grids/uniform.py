from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class UniformGrid1D:
    nx: int
    xmin: float
    xmax: float

    @property
    def dx(self) -> float:
        return (self.xmax - self.xmin) / self.nx

    @property
    def x(self) -> np.ndarray:
        dx = self.dx
        return np.linspace(self.xmin + 0.5 * dx, self.xmax - 0.5 * dx, self.nx)


@dataclass(slots=True)
class UniformGrid2D:
    nx: int
    ny: int
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    @property
    def dx(self) -> float:
        return (self.xmax - self.xmin) / self.nx

    @property
    def dy(self) -> float:
        return (self.ymax - self.ymin) / self.ny

    @property
    def x(self) -> np.ndarray:
        dx = self.dx
        return np.linspace(self.xmin + 0.5 * dx, self.xmax - 0.5 * dx, self.nx)

    @property
    def y(self) -> np.ndarray:
        dy = self.dy
        return np.linspace(self.ymin + 0.5 * dy, self.ymax - 0.5 * dy, self.ny)
