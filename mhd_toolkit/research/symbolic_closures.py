from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _sp():
    try:
        import sympy as sp
    except Exception as exc:  # pragma: no cover - handled in CLI / scripts
        raise ImportError(
            "SymPy is required for the symbolic closure program. Install `mhd-toolkit[research]` "
            "or add `sympy` to the environment."
        ) from exc
    return sp


def cylindrical_symbols():
    sp = _sp()
    r, theta, z = sp.symbols("r theta z", real=True, positive=True)
    eta = sp.symbols("eta", real=True, positive=True)
    return sp, r, theta, z, eta


def grad_cyl(expr, r, theta, z):
    sp = _sp()
    return sp.Matrix([
        sp.diff(expr, r),
        (1 / r) * sp.diff(expr, theta),
        sp.diff(expr, z),
    ])


def cross_phys(a, b):
    sp = _sp()
    return sp.Matrix([
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ])


def laplacian_cyl(expr, r, theta, z):
    sp = _sp()
    return (
        sp.diff(expr, r, 2)
        + (1 / r) * sp.diff(expr, r)
        + (1 / r**2) * sp.diff(expr, theta, 2)
        + sp.diff(expr, z, 2)
    )


def vector_laplacian_cyl(vec, r, theta, z):
    sp = _sp()
    a_r, a_theta, a_z = vec
    return sp.Matrix([
        laplacian_cyl(a_r, r, theta, z) - a_r / r**2 - (2 / r**2) * sp.diff(a_theta, theta),
        laplacian_cyl(a_theta, r, theta, z) - a_theta / r**2 + (2 / r**2) * sp.diff(a_r, theta),
        laplacian_cyl(a_z, r, theta, z),
    ])


def curl_cyl(vec, r, theta, z):
    sp = _sp()
    a_r, a_theta, a_z = vec
    return sp.Matrix([
        (1 / r) * (sp.diff(a_z, theta) - sp.diff(r * a_theta, z)),
        sp.diff(a_r, z) - sp.diff(a_z, r),
        (1 / r) * (sp.diff(r * a_theta, r) - sp.diff(a_r, theta)),
    ])


def magnetic_field(alpha, beta):
    sp, r, theta, z, _ = cylindrical_symbols()
    return sp.simplify(cross_phys(grad_cyl(alpha, r, theta, z), grad_cyl(beta, r, theta, z)))


def constant_eta_residual(alpha, beta):
    sp, r, theta, z, eta = cylindrical_symbols()
    grad_alpha = grad_cyl(alpha, r, theta, z)
    grad_beta = grad_cyl(beta, r, theta, z)
    lap_alpha = laplacian_cyl(alpha, r, theta, z)
    lap_beta = laplacian_cyl(beta, r, theta, z)
    naive = cross_phys(grad_cyl(eta * lap_alpha, r, theta, z), grad_beta) + cross_phys(
        grad_alpha, grad_cyl(eta * lap_beta, r, theta, z)
    )
    true = eta * vector_laplacian_cyl(magnetic_field(alpha, beta), r, theta, z)
    return sp.simplify(true - naive)


def variable_eta_residual(alpha, beta, eta_expr):
    sp, r, theta, z, _ = cylindrical_symbols()
    grad_alpha = grad_cyl(alpha, r, theta, z)
    grad_beta = grad_cyl(beta, r, theta, z)
    lap_alpha = laplacian_cyl(alpha, r, theta, z)
    lap_beta = laplacian_cyl(beta, r, theta, z)
    bfield = magnetic_field(alpha, beta)
    naive = cross_phys(grad_cyl(eta_expr * lap_alpha, r, theta, z), grad_beta) + cross_phys(
        grad_alpha, grad_cyl(eta_expr * lap_beta, r, theta, z)
    )
    true = eta_expr * vector_laplacian_cyl(bfield, r, theta, z) + cross_phys(
        grad_cyl(eta_expr, r, theta, z), curl_cyl(bfield, r, theta, z)
    )
    return sp.simplify(true - naive)


def build_symbolic_report(max_power: int = 6) -> dict[str, Any]:
    sp, r, theta, z, eta = cylindrical_symbols()
    f = sp.Function("f")
    g = sp.Function("g")
    eta_r = sp.Function("eta")(r)

    radial_rtheta_res = constant_eta_residual(f(r), r * theta)
    radial_z_res = constant_eta_residual(f(r), z)
    radial_theta_res = constant_eta_residual(f(r), theta)
    rtheta_gz_res = constant_eta_residual(r * theta, g(z))

    radial_rtheta_var = variable_eta_residual(f(r), r * theta, eta_r)
    radial_z_var = variable_eta_residual(f(r), z, eta_r)
    rtheta_gz_var = variable_eta_residual(r * theta, g(z), eta_r)

    power_family = []
    for n in range(1, max_power + 1):
        residual = sp.simplify(constant_eta_residual(r**n, r * theta))
        power_family.append({"n": n, "residual": str(residual.T), "exact": residual == sp.zeros(3, 1)})

    return {
        "exact_families": {
            "alpha=f(r), beta=r*theta": str(radial_rtheta_res.T),
            "alpha=f(r), beta=z": str(radial_z_res.T),
            "alpha=r*theta, beta=g(z)": str(rtheta_gz_res.T),
        },
        "conditional_family": {
            "alpha=f(r), beta=theta": str(radial_theta_res.T),
            "exact_condition": "r*f''(r) = f'(r), so f(r) = a*r**2 + b",
        },
        "variable_eta_obstructions": {
            "alpha=f(r), beta=r*theta": str(radial_rtheta_var.T),
            "alpha=f(r), beta=z": str(radial_z_var.T),
            "alpha=r*theta, beta=g(z)": str(rtheta_gz_var.T),
            "smoothness_note": (
                "For nonconstant eta(r), exactness forces singular or trivial solutions in the tested radial families."
            ),
        },
        "sample_checks": {
            "power_family_alpha=r**n_beta=r*theta": power_family,
            "quadratic_case_alpha=r**2_beta=theta": str(constant_eta_residual(r**2, theta).T),
            "cubic_case_alpha=r**3_beta=theta": str(constant_eta_residual(r**3, theta).T),
            "variable_eta_alpha=r*theta_beta=r*z_eta=r": str(variable_eta_residual(r * theta, r * z, r).T),
        },
    }


def write_symbolic_report(path: str | Path, max_power: int = 6) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_symbolic_report(max_power=max_power)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
