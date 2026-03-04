from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class Adam:
    lr: float = 1e-2
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8

    def __post_init__(self) -> None:
        self.m = None
        self.v = None
        self.t = 0

    def step(self, x: np.ndarray, grad: np.ndarray) -> np.ndarray:
        if self.m is None:
            self.m = np.zeros_like(x)
            self.v = np.zeros_like(x)
        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (grad * grad)
        mhat = self.m / (1.0 - self.beta1 ** self.t)
        vhat = self.v / (1.0 - self.beta2 ** self.t)
        return x - self.lr * mhat / (np.sqrt(vhat) + self.eps)
