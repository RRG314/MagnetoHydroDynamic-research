from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class TopologicalAdam:
    """Experimental NumPy Topological Adam optimizer for residual minimization.

    Design intent:
    - Keep Adam-compatible behavior when `w_topo=0`.
    - Add bounded topology-aware correction terms.
    - Avoid numerical failure with NaN/Inf gradients.
    """

    lr: float = 1e-2
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8
    eta: float = 0.05
    mu0: float = 1.0
    w_topo: float = 0.05
    target_energy: float = 1e-3
    max_energy_factor: float = 10.0
    max_topo_ratio: float = 0.25
    weight_decay: float = 0.0
    grad_clip_value: float = 1e6
    deterministic_init: bool = True

    def __post_init__(self) -> None:
        if self.lr <= 0.0:
            raise ValueError("lr must be > 0")
        if not (0.0 <= self.beta1 < 1.0 and 0.0 <= self.beta2 < 1.0):
            raise ValueError("betas must satisfy 0 <= beta < 1")
        if self.eps <= 0.0:
            raise ValueError("eps must be > 0")
        if self.eta < 0.0:
            raise ValueError("eta must be >= 0")
        if self.mu0 <= 0.0:
            raise ValueError("mu0 must be > 0")
        if self.max_topo_ratio < 0.0:
            raise ValueError("max_topo_ratio must be >= 0")
        if self.target_energy < 0.0:
            raise ValueError("target_energy must be >= 0")
        if self.max_energy_factor <= 1.0:
            raise ValueError("max_energy_factor must be > 1")
        if self.grad_clip_value < 0.0:
            raise ValueError("grad_clip_value must be >= 0")
        if self.weight_decay < 0.0:
            raise ValueError("weight_decay must be >= 0")

        self.m = None
        self.v = None
        self.alpha = None
        self.beta = None
        self.t = 0
        self._energy = 0.0
        self._coupling = 0.0
        self._num_steps = 0

    def _deterministic_field(self, x: np.ndarray, phase: float) -> np.ndarray:
        idx = np.arange(x.size, dtype=float)
        mean = float(np.mean(x)) if x.size else 0.0
        base = np.sin(idx * 12.9898 + mean * 78.233 + phase) * 43758.5453
        frac = base - np.floor(base)
        noise = (frac * 2.0 - 1.0).reshape(x.shape)
        scale = 1e-2
        return scale * noise

    def _sanitize_grad(self, grad: np.ndarray) -> np.ndarray:
        g = np.nan_to_num(
            grad,
            nan=0.0,
            posinf=self.grad_clip_value,
            neginf=-self.grad_clip_value,
        )
        if self.grad_clip_value > 0.0:
            g = np.clip(g, -self.grad_clip_value, self.grad_clip_value)
        return g

    def step(self, x: np.ndarray, grad: np.ndarray) -> np.ndarray:
        g = self._sanitize_grad(grad)
        if self.weight_decay != 0.0:
            g = g + self.weight_decay * x

        if self.m is None:
            self.m = np.zeros_like(x)
            self.v = np.zeros_like(x)
            if self.deterministic_init:
                self.alpha = self._deterministic_field(x, phase=0.13)
                self.beta = self._deterministic_field(x, phase=1.37)
            else:
                self.alpha = 1e-2 * np.random.standard_normal(size=x.shape)
                self.beta = 1e-2 * np.random.standard_normal(size=x.shape)

        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * g
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (g * g)
        mhat = self.m / (1.0 - self.beta1 ** self.t)
        vhat = self.v / (1.0 - self.beta2 ** self.t)
        adam_dir = mhat / (np.sqrt(vhat) + self.eps)

        g_norm = float(np.linalg.norm(g))
        if np.isfinite(g_norm) and g_norm > 1e-12:
            g_dir = g / (g_norm + 1e-12)
            j = float(np.sum((self.alpha - self.beta) * g_dir))
            alpha_prev = self.alpha.copy()
            coupling = self.eta / (self.mu0 + 1e-12)
            self.alpha = (1.0 - self.eta) * self.alpha + (coupling * j) * self.beta
            self.beta = (1.0 - self.eta) * self.beta - (coupling * j) * alpha_prev
        else:
            j = 0.0

        energy = 0.5 * float(np.mean(self.alpha * self.alpha + self.beta * self.beta))
        if self.target_energy > 0.0 and energy > 0.0:
            if energy < self.target_energy:
                scale = np.sqrt(self.target_energy / (energy + 1e-12))
                self.alpha *= scale
                self.beta *= scale
                energy = self.target_energy
            elif energy > self.target_energy * self.max_energy_factor:
                damp = np.sqrt((self.target_energy * self.max_energy_factor) / (energy + 1e-12))
                self.alpha *= damp
                self.beta *= damp
                energy = self.target_energy * self.max_energy_factor

        topo = np.tanh(self.alpha - self.beta)
        # Remove mean drift to keep correction centered.
        topo = topo - float(np.mean(topo))

        n_adam = float(np.linalg.norm(adam_dir)) + 1e-12
        n_topo = float(np.linalg.norm(topo))
        if n_topo > 0.0 and self.max_topo_ratio > 0.0:
            topo = topo * min(1.0, self.max_topo_ratio * n_adam / (n_topo + 1e-12))
        else:
            topo = np.zeros_like(x)

        self._energy = energy
        self._coupling = abs(j)
        self._num_steps += 1

        return x - self.lr * (adam_dir + self.w_topo * topo)

    def stats(self) -> dict[str, float]:
        return {
            "energy": float(self._energy),
            "coupling": float(self._coupling),
            "steps": float(self._num_steps),
        }
