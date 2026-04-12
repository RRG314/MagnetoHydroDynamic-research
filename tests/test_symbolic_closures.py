from __future__ import annotations

import pytest

sp = pytest.importorskip("sympy")

from mhd_toolkit.research.symbolic_closures import build_symbolic_report, constant_eta_residual, variable_eta_residual


def test_constant_eta_exact_radial_rtheta_family() -> None:
    r, theta, z, eta = sp.symbols("r theta z eta", real=True, positive=True)
    f = sp.Function("f")
    residual = constant_eta_residual(f(r), r * theta)
    assert residual == sp.zeros(3, 1)


def test_constant_eta_exact_radial_z_family() -> None:
    r, theta, z, eta = sp.symbols("r theta z eta", real=True, positive=True)
    f = sp.Function("f")
    residual = constant_eta_residual(f(r), z)
    assert residual == sp.zeros(3, 1)


def test_constant_eta_radial_theta_is_not_generically_exact() -> None:
    r, theta, z, eta = sp.symbols("r theta z eta", real=True, positive=True)
    assert constant_eta_residual(r**2, theta) == sp.zeros(3, 1)
    assert constant_eta_residual(r**3, theta) != sp.zeros(3, 1)


def test_variable_eta_breaks_cylindrical_case() -> None:
    r, theta, z, eta = sp.symbols("r theta z eta", real=True, positive=True)
    residual = variable_eta_residual(r * theta, r * z, r)
    assert residual != sp.zeros(3, 1)


def test_symbolic_report_marks_power_samples_exact() -> None:
    report = build_symbolic_report(max_power=4)
    samples = report["sample_checks"]["power_family_alpha=r**n_beta=r*theta"]
    assert all(item["exact"] for item in samples)
