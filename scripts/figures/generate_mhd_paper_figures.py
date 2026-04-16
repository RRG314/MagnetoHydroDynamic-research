#!/usr/bin/env python3
"""Generate publication figures for mhd_paper_upgraded.md."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "figures" / "mhd"
METRICS_PATH = ROOT / "data/generated/figures/mhd_publication_figure_metrics.json"


def setup_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 300, "font.size": 11})


def save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def mixed_remainder_abs(r: np.ndarray, eta: np.ndarray, eta_prime: np.ndarray, a: float = 1.0, q0: float = 1.0, kappa: float = 0.5) -> np.ndarray:
    num = a * (kappa * r**2 * eta_prime + 2.0 * q0 * r * eta_prime + 4.0 * q0 * eta)
    return np.abs(num / r**4)


def main() -> None:
    setup_style()
    metrics: dict[str, object] = {}

    r = np.linspace(0.05, 2.0, 800)
    eta_const = np.ones_like(r)
    eta_const_prime = np.zeros_like(r)
    eta_var = r**2
    eta_var_prime = 2.0 * r

    r_const = mixed_remainder_abs(r, eta_const, eta_const_prime)
    r_var = mixed_remainder_abs(r, eta_var, eta_var_prime)

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(r, r_const, color="#264653", linewidth=2.2, label="constant η = 1")
    ax.plot(r, r_var, color="#e76f51", linewidth=2.2, label="variable η = r²")
    ax.set_yscale("log")
    ax.set_xlabel("r")
    ax.set_ylabel("|R(r)|")
    ax.set_title("Closure-defect magnitude for constant vs variable resistivity")
    ax.legend(loc="upper right")
    save(fig, "mhd_remainder_constant_vs_variable_eta")

    r_small = np.logspace(-4, -1, 500)
    curves = {
        "η=1": mixed_remainder_abs(r_small, np.ones_like(r_small), np.zeros_like(r_small)),
        "η=r": mixed_remainder_abs(r_small, r_small, np.ones_like(r_small)),
        "η=r²": mixed_remainder_abs(r_small, r_small**2, 2.0 * r_small),
        "η=r³": mixed_remainder_abs(r_small, r_small**3, 3.0 * r_small**2),
    }
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    for label, vals in curves.items():
        ax.loglog(r_small, vals, linewidth=2.0, label=label)
    ax.set_xlabel("r")
    ax.set_ylabel("|R(r)|")
    ax.set_title("Near-axis singular behavior of the closure remainder")
    ax.legend(loc="upper right")
    save(fig, "mhd_singularity_near_axis")

    eta0 = 1.0
    eps = 0.02
    r0 = 1.0
    deltas = np.array([0.40, 0.30, 0.22, 0.16, 0.12, 0.09, 0.07, 0.05])
    r_grid = np.linspace(0.60, 1.40, 3000)

    max_vals = []
    for d in deltas:
        eta = eta0 + eps * np.tanh((r_grid - r0) / d)
        sech2 = 1.0 / np.cosh((r_grid - r0) / d) ** 2
        eta_prime = eps * sech2 / d
        max_vals.append(float(np.max(mixed_remainder_abs(r_grid, eta, eta_prime, q0=0.0, kappa=1.0))))
    max_vals = np.array(max_vals)

    x = 1.0 / deltas
    slope, intercept = np.polyfit(x, max_vals, 1)

    fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.2))
    axs[0].plot(x, max_vals, "o-", color="#1d3557", label="computed maxima")
    axs[0].plot(x, slope * x + intercept, "--", color="#e76f51", label=f"linear fit (slope={slope:.3f})")
    axs[0].set_xlabel("1/δ")
    axs[0].set_ylabel("max |R|")
    axs[0].set_title("Sheet-thinning scaling (gradient-dominated lane)")
    axs[0].legend(loc="upper left")

    normalized = max_vals * deltas / eps
    axs[1].plot(deltas, normalized, "o-", color="#2a9d8f")
    axs[1].set_xlabel("δ")
    axs[1].set_ylabel("max|R| · δ / ε")
    axs[1].set_title("Normalization check for ~ ε/δ behavior")
    axs[1].invert_xaxis()
    save(fig, "mhd_sheet_thinning_scaling")

    r_min = np.logspace(-4, -0.15, 250)
    l2_log = np.sqrt(1.0 / r_min - 1.0)
    l2_sqrt = np.sqrt(0.25 * np.log(1.0 / r_min))

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.loglog(r_min, l2_log, color="#e63946", linewidth=2.2, label="f(r)=log r survivor profile")
    ax.loglog(r_min, l2_sqrt, color="#457b9d", linewidth=2.2, label="f(r)=sqrt(r) survivor profile")
    ax.axvline(0.2, color="black", linestyle="--", linewidth=1.2, label="example annular cutoff r_min=0.2")
    ax.set_xlabel("inner radius r_min")
    ax.set_ylabel("||f'(r)||_{L2([r_min,1])}")
    ax.set_title("Axis-touching limit vs annular regularization")
    ax.legend(loc="upper right")
    save(fig, "mhd_axis_vs_annular_behavior")

    metrics["sheet_scaling"] = {
        "deltas": deltas.tolist(),
        "max_values": max_vals.tolist(),
        "fit_slope": float(slope),
        "fit_intercept": float(intercept),
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
