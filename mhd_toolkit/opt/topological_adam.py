from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class TopologicalAdam:
    """Experimental numpy optimizer with optional topology-aware correction.

    This is a lightweight placeholder API compatible with Adam-style residual minimization.
    Set `w_topo=0` to recover Adam-like behavior.
    """

    lr: float = 1e-2
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8
    eta: float = 0.05
    w_topo: float = 0.05

    def __post_init__(self) -> None:
        self.m = None
        self.v = None
        self.alpha = None
        self.beta = None
        self.t = 0

    def step(self, x: np.ndarray, grad: np.ndarray) -> np.ndarray:
        if self.m is None:
            self.m = np.zeros_like(x)
            self.v = np.zeros_like(x)
            self.alpha = np.zeros_like(x)
            self.beta = np.zeros_like(x)

        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (grad * grad)
        mhat = self.m / (1.0 - self.beta1 ** self.t)
        vhat = self.v / (1.0 - self.beta2 ** self.t)
        adam_dir = mhat / (np.sqrt(vhat) + self.eps)

        j = np.sum((self.alpha - self.beta) * grad)
        self.alpha = (1.0 - self.eta) * self.alpha + self.eta * j
        self.beta = (1.0 - self.eta) * self.beta - self.eta * j

        topo = np.tanh(self.alpha - self.beta)
        n_adam = np.linalg.norm(adam_dir) + 1e-12
        n_topo = np.linalg.norm(topo)
        if n_topo > 0.0:
            topo = topo * min(1.0, 0.25 * n_adam / n_topo)

        return x - self.lr * (adam_dir + self.w_topo * topo)
