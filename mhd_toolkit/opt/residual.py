from __future__ import annotations

import time
import numpy as np

from .adam import Adam
from .topological_adam import TopologicalAdam


def laplacian_periodic_2d(u: np.ndarray) -> np.ndarray:
    return (
        np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=1)
        + np.roll(u, 1, axis=1)
        - 4.0 * u
    )


def residual(u: np.ndarray, source: np.ndarray, eta: float) -> np.ndarray:
    return eta * laplacian_periodic_2d(u) - source


def objective_and_grad(u: np.ndarray, source: np.ndarray, eta: float) -> tuple[float, np.ndarray]:
    r = residual(u, source, eta)
    obj = 0.5 * float(np.mean(r * r))
    grad = eta * laplacian_periodic_2d(r)
    return obj, grad


def solve_with_optimizer(
    optimizer_name: str,
    source: np.ndarray,
    eta: float,
    steps: int = 400,
    lr: float = 1e-2,
    seed: int = 1729,
) -> dict:
    rng = np.random.default_rng(seed)
    u = 0.01 * rng.standard_normal(size=source.shape)

    if optimizer_name == "adam":
        opt = Adam(lr=lr)
    elif optimizer_name == "topological_adam":
        opt = TopologicalAdam(lr=lr)
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_name}")

    t0 = time.perf_counter()
    history = []
    for k in range(steps):
        obj, grad = objective_and_grad(u, source, eta)
        u = opt.step(u, grad)
        if k % 10 == 0 or k == steps - 1:
            history.append({"iter": k, "objective": obj, "residual_l2": float(np.sqrt(2.0 * obj))})
    elapsed = time.perf_counter() - t0

    final_obj, _ = objective_and_grad(u, source, eta)
    return {
        "optimizer": optimizer_name,
        "steps": steps,
        "time_seconds": elapsed,
        "final_objective": final_obj,
        "final_residual_l2": float(np.sqrt(2.0 * final_obj)),
        "history": history,
    }


def residual_demo(nx: int = 32, ny: int = 32, eta: float = 0.1, steps: int = 400) -> dict:
    x = np.linspace(0.0, 2.0 * np.pi, nx, endpoint=False)
    y = np.linspace(0.0, 2.0 * np.pi, ny, endpoint=False)
    X, Y = np.meshgrid(x, y, indexing="ij")
    source = np.sin(X) * np.cos(Y)

    adam_res = solve_with_optimizer("adam", source=source, eta=eta, steps=steps, lr=3e-2)
    topo_res = solve_with_optimizer("topological_adam", source=source, eta=eta, steps=steps, lr=3e-2)
    return {
        "grid": {"nx": nx, "ny": ny},
        "eta": eta,
        "adam": adam_res,
        "topological_adam": topo_res,
    }
