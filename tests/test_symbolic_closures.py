from __future__ import annotations

import pytest

sp = pytest.importorskip("sympy")

from mhd_toolkit.research.symbolic_closures import (
    build_axis_touching_smooth_no_go_report,
    build_symbolic_report,
    build_variable_eta_classification_report,
    constant_eta_residual,
    first_order_eta_perturbation_residual,
    solve_variable_eta_radial_gz_family,
    solve_variable_eta_radial_rtheta_gz_family,
    solve_variable_eta_radial_rtheta_family,
    solve_variable_eta_radial_z_family,
    variable_eta_residual,
)


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


def test_first_order_variable_eta_obstructions_match_exact_linearization() -> None:
    r, theta, z, eta = sp.symbols("r theta z eta", real=True, positive=True)
    eta1 = sp.Function("eta1")(r)
    f = sp.Function("f")
    exact = variable_eta_residual(f(r), r * theta, eta + eta1)
    perturbative = first_order_eta_perturbation_residual(f(r), r * theta, eta, eta1)
    assert sp.simplify(exact - perturbative) == sp.zeros(3, 1)


def test_variable_eta_has_annular_exact_radial_rtheta_survivor() -> None:
    r, theta, z = sp.symbols("r theta z", real=True, positive=True)
    a, b = sp.symbols("a b", real=True)
    eta_r = sp.Function("eta")(r)
    residual = variable_eta_residual(a * sp.sqrt(r) + b, r * theta, eta_r)
    assert sp.simplify(residual) == sp.zeros(3, 1)
    summary = solve_variable_eta_radial_rtheta_family()
    assert "sqrt(r)" in str(summary["general_solution_on_annulus"])


def test_variable_eta_has_annular_exact_radial_z_survivor() -> None:
    r, theta, z = sp.symbols("r theta z", real=True, positive=True)
    a, b = sp.symbols("a b", real=True)
    eta_r = sp.Function("eta")(r)
    residual = variable_eta_residual(a * sp.log(r) + b, z, eta_r)
    assert sp.simplify(residual) == sp.zeros(3, 1)
    summary = solve_variable_eta_radial_z_family()
    assert "log(r)" in str(summary["general_solution_on_annulus"])


def test_variable_eta_classification_report_records_annular_survivors() -> None:
    report = build_variable_eta_classification_report()
    assert report["annular_exact_families"]["alpha=f(r), beta=r*theta"]["solution"] == "f(r) = a*sqrt(r) + b"
    assert report["annular_exact_families"]["alpha=f(r), beta=z"]["solution"] == "f(r) = a*log(r) + b"


def test_nonconstant_polynomial_axis_touching_profiles_are_not_exact_under_variable_eta() -> None:
    r, theta, z = sp.symbols("r theta z", real=True, positive=True)
    eta_r = sp.Function("eta")(r)
    for expr in (r, r**2, r**3):
        assert sp.simplify(variable_eta_residual(expr, r * theta, eta_r)) != sp.zeros(3, 1)
        assert sp.simplify(variable_eta_residual(expr, z, eta_r)) != sp.zeros(3, 1)


def test_axis_touching_smooth_no_go_report_keeps_only_constants() -> None:
    report = build_axis_touching_smooth_no_go_report()
    assert report["families"]["alpha=f(r), beta=r*theta"]["smooth_axis_touching_survivors"] == "f(r) = b only"
    assert report["families"]["alpha=f(r), beta=z"]["smooth_axis_touching_survivors"] == "f(r) = b only"


def test_variable_eta_extends_log_family_to_general_g_of_z() -> None:
    r, theta, z = sp.symbols("r theta z", real=True, positive=True)
    eta_r = sp.Function("eta")(r)
    g = sp.Function("g")
    residual = variable_eta_residual(sp.log(r), g(z), eta_r)
    assert sp.simplify(residual) == sp.zeros(3, 1)
    summary = solve_variable_eta_radial_gz_family()
    assert "log(r)" in str(summary["general_solution_on_annulus"])


def test_variable_eta_blocks_nontrivial_rtheta_gz_extension() -> None:
    summary = solve_variable_eta_radial_rtheta_gz_family()
    assert "only nontrivial exact survivors are the g(z)=const reductions" in summary["exactness_note"]


def test_variable_eta_classification_report_records_general_gz_family() -> None:
    report = build_variable_eta_classification_report()
    assert report["annular_exact_families"]["alpha=f(r), beta=g(z)"]["solution"] == "f(r) = a*log(r) + b"
