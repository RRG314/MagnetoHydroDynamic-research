from __future__ import annotations

import numpy as np

from mhd_toolkit.opt.topological_adam import TopologicalAdam


def quad_grad(x: np.ndarray, target: np.ndarray) -> np.ndarray:
    return 2.0 * (x - target)


def test_topological_adam_reduces_quadratic_loss() -> None:
    target = np.array([3.0, -2.0])
    x = np.array([0.0, 0.0])
    opt = TopologicalAdam(lr=0.05, w_topo=0.05)

    def loss(z: np.ndarray) -> float:
        d = z - target
        return float(np.dot(d, d))

    l0 = loss(x)
    for _ in range(300):
        g = quad_grad(x, target)
        x = opt.step(x, g)
    l1 = loss(x)

    assert l1 < l0
    assert l1 < 1e-2


def test_topological_adam_sanitizes_nonfinite_gradients() -> None:
    x = np.array([1.0, -1.0, 0.5])
    g = np.array([np.nan, np.inf, -np.inf])
    opt = TopologicalAdam(lr=0.01)
    x2 = opt.step(x, g)
    assert np.isfinite(x2).all()


def test_topological_adam_deterministic_init_for_same_input() -> None:
    x0 = np.array([0.2, -0.4, 0.7, 1.1])
    g0 = np.array([0.1, -0.2, 0.05, -0.03])

    opt1 = TopologicalAdam(lr=0.01, deterministic_init=True)
    opt2 = TopologicalAdam(lr=0.01, deterministic_init=True)

    x1 = opt1.step(x0.copy(), g0.copy())
    x2 = opt2.step(x0.copy(), g0.copy())
    assert np.allclose(x1, x2)


def test_topological_adam_stats_keys() -> None:
    x = np.array([1.0, 2.0])
    g = np.array([0.1, -0.1])
    opt = TopologicalAdam()
    _ = opt.step(x, g)
    stats = opt.stats()
    for k in ["energy", "coupling", "steps"]:
        assert k in stats
        assert np.isfinite(stats[k])
