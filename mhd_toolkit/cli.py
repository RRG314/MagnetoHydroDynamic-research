from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
from typing import Any

import numpy as np

from .config import SolverConfig
from .diagnostics import Diagnostics
from .divfree.glm import clean_B_glm
from .divfree.metrics import div_metrics
from .divfree.projection import clean_B_projection
from .equations.mhd_ideal import BX, BY
from .opt.residual import residual_demo
from .research import write_symbolic_report
from .solvers.fv1d import FV1DSolver
from .solvers.fv2d import FV2DSolver
from .tests.problems import brio_wu, orszag_tang, reconnection_toy


def _try_plot(series: dict[str, list[float]], out_png: Path, title: str, ylabel: str) -> bool:
    try:
        import matplotlib.pyplot as plt  # type: ignore

        plt.figure(figsize=(6, 4))
        for name, vals in series.items():
            plt.plot(vals, label=name)
        plt.title(title)
        plt.xlabel("sample")
        plt.ylabel(ylabel)
        if len(series) > 1:
            plt.legend()
        plt.tight_layout()
        out_png.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_png)
        plt.close()
        return True
    except Exception:
        return False


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _args_payload(args: argparse.Namespace) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, val in vars(args).items():
        if key == "func":
            continue
        if callable(val):
            continue
        out[key] = val
    return out


def run_problem(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = SolverConfig(
        gamma=args.gamma,
        cfl=args.cfl,
        closure=args.closure,
        divfree=args.divfree,
        eta=args.eta,
        nu=args.nu,
        glm_ch=args.glm_ch,
        glm_cp=args.glm_cp,
    )

    t0 = time.perf_counter()
    if args.problem == "brio-wu":
        x, U0 = brio_wu.initial_state(args.nx, gamma=args.gamma)
        solver = FV1DSolver(cfg, x, U0)
        diag = Diagnostics(dim=1)
        summary = solver.run(steps=args.steps, diagnostics=diag)
        last = diag.latest()
        payload = {
            "problem": args.problem,
            "config": _args_payload(args),
            "summary": summary,
            "diagnostics_last": last,
            "wall_seconds": time.perf_counter() - t0,
        }
        _write_json(out_dir / "run_brio_wu.json", payload)
        diag.to_json(out_dir / "run_brio_wu_diagnostics.json")
        print(f"Completed {args.problem}: steps={summary['num_steps']} t={summary['time']:.4e}")
        print(f"Saved {out_dir / 'run_brio_wu.json'}")
        return 0

    if args.problem == "orszag-tang":
        x, y, U0 = orszag_tang.initial_state(args.nx, args.ny, gamma=args.gamma)
    elif args.problem == "reconnection-toy":
        x, y, U0 = reconnection_toy.initial_state(args.nx, args.ny, gamma=args.gamma)
    else:
        raise ValueError(f"Unknown problem: {args.problem}")

    solver = FV2DSolver(cfg, x, y, U0)
    diag = Diagnostics(dim=2)
    summary = solver.run(steps=args.steps, diagnostics=diag)
    last = diag.latest()
    payload = {
        "problem": args.problem,
        "config": _args_payload(args),
        "summary": summary,
        "diagnostics_last": last,
        "wall_seconds": time.perf_counter() - t0,
    }
    base = args.problem.replace("-", "_")
    _write_json(out_dir / f"run_{base}.json", payload)
    diag.to_json(out_dir / f"run_{base}_diagnostics.json")
    print(f"Completed {args.problem}: steps={summary['num_steps']} t={summary['time']:.4e}")
    if summary["divfree_reports"]:
        final_clean = summary["divfree_reports"][-1]
        print(
            "Final div-clean report: "
            f"l2(divB) {final_clean['before_l2_divB']:.3e}->{final_clean['after_l2_divB']:.3e}, "
            f"dE={final_clean['energy_change']:.3e}"
        )
    print(f"Saved {out_dir / f'run_{base}.json'}")
    return 0


def compare_closures(args: argparse.Namespace) -> int:
    closures = [c.strip() for c in args.closures.split(",") if c.strip()]
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for closure in closures:
        cfg = SolverConfig(
            gamma=args.gamma,
            cfl=args.cfl,
            closure=closure,
            divfree=args.divfree,
            eta=args.eta,
            nu=args.nu,
        )

        t0 = time.perf_counter()
        if args.problem == "brio-wu":
            x, U0 = brio_wu.initial_state(args.nx, gamma=args.gamma)
            solver = FV1DSolver(cfg, x, U0)
            diag = Diagnostics(dim=1)
            summary = solver.run(steps=args.steps, diagnostics=diag)
        elif args.problem == "orszag-tang":
            x, y, U0 = orszag_tang.initial_state(args.nx, args.ny, gamma=args.gamma)
            solver = FV2DSolver(cfg, x, y, U0)
            diag = Diagnostics(dim=2)
            summary = solver.run(steps=args.steps, diagnostics=diag)
        else:
            raise ValueError(f"Unsupported compare problem: {args.problem}")

        last = diag.latest()
        results.append(
            {
                "closure": closure,
                "summary": summary,
                "diagnostics_last": last,
                "wall_seconds": time.perf_counter() - t0,
            }
        )

    payload = {
        "task": "compare_closures",
        "problem": args.problem,
        "closures": closures,
        "results": results,
    }
    _write_json(out_dir / f"compare_closures_{args.problem.replace('-', '_')}.json", payload)

    energy_drift_series = {r["closure"]: [r["diagnostics_last"].get("drift_total_energy", 0.0)] for r in results}
    _try_plot(
        energy_drift_series,
        out_dir / f"compare_closures_{args.problem.replace('-', '_')}_energy.png",
        f"Closure Compare: {args.problem}",
        "final total energy drift",
    )

    print(f"Compared closures on {args.problem}: {', '.join(closures)}")
    for row in results:
        d = row["diagnostics_last"]
        print(
            f"  {row['closure']}: drift_total_energy={d.get('drift_total_energy', 0.0):.3e}, "
            f"l2_divB={d.get('l2_divB', 0.0):.3e}, wall={row['wall_seconds']:.3f}s"
        )
    return 0


def divfree_demo(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.problem != "orszag-tang":
        raise ValueError("divfree demo currently supports problem=orszag-tang")

    x, y, U = orszag_tang.initial_state(args.nx, args.ny, gamma=args.gamma)
    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])

    rng = np.random.default_rng(args.seed)
    Bx0 = U[BX].copy() + args.perturb * rng.standard_normal(size=U[BX].shape)
    By0 = U[BY].copy() + args.perturb * rng.standard_normal(size=U[BY].shape)

    base = div_metrics(Bx0, By0, dx, dy)

    methods = [m.strip() for m in args.method.split(",") if m.strip()]
    reports: dict[str, Any] = {"baseline": base}
    e0 = float(np.mean(0.5 * (Bx0 * Bx0 + By0 * By0)))

    for m in methods:
        if m == "projection":
            bxp, byp, rep = clean_B_projection(Bx0, By0, dx, dy, periodic=True)
            after = div_metrics(bxp, byp, dx, dy)
            e_after = float(np.mean(0.5 * (bxp * bxp + byp * byp)))
            reports[m] = {
                **rep,
                "before_l2_divB": base["l2_divB"],
                "before_max_abs_divB": base["max_abs_divB"],
                "after_l2_divB": after["l2_divB"],
                "after_max_abs_divB": after["max_abs_divB"],
                "energy_change": e_after - e0,
                "after": after,
            }
        elif m == "glm":
            psi = np.zeros_like(Bx0)
            bx, by = Bx0.copy(), By0.copy()
            t_glm = time.perf_counter()
            for _ in range(args.glm_steps):
                bx, by, psi, _ = clean_B_glm(bx, by, psi, dx, dy, dt=args.glm_dt, ch=args.glm_ch, cp=args.glm_cp)
            glm_runtime = time.perf_counter() - t_glm
            after = div_metrics(bx, by, dx, dy)
            e_after = float(np.mean(0.5 * (bx * bx + by * by)))
            reports[m] = {
                "before_l2_divB": base["l2_divB"],
                "before_max_abs_divB": base["max_abs_divB"],
                "after_l2_divB": after["l2_divB"],
                "after_max_abs_divB": after["max_abs_divB"],
                "energy_change": e_after - e0,
                "runtime_seconds": glm_runtime,
                "after": after,
            }
        else:
            raise ValueError(f"Unknown method: {m}")

    payload = {
        "task": "divfree_demo",
        "problem": args.problem,
        "methods": methods,
        "reports": reports,
    }
    out_json = out_dir / f"divfree_demo_{args.problem.replace('-', '_')}.json"
    _write_json(out_json, payload)

    series = {"baseline": [base["l2_divB"]]}
    for m in methods:
        series[m] = [reports[m]["after"]["l2_divB"]]
    _try_plot(series, out_dir / "divfree_demo_l2.png", "Divergence Cleaning Demo", "l2(divB)")

    print(f"Saved {out_json}")
    for m in methods:
        print(
            f"  {m}: l2(divB) {reports[m]['before_l2_divB']:.3e}->{reports[m]['after_l2_divB']:.3e}, "
            f"dE={reports[m]['energy_change']:.3e}"
        )
    return 0


def run_opt_demo(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    res = residual_demo(nx=args.nx, ny=args.ny, eta=args.eta, steps=args.steps)

    out_json = out_dir / "residual_demo.json"
    _write_json(out_json, res)

    series = {
        "adam": [row["residual_l2"] for row in res["adam"]["history"]],
        "topological_adam": [row["residual_l2"] for row in res["topological_adam"]["history"]],
    }
    _try_plot(series, out_dir / "residual_demo.png", "Residual Minimization", "residual L2")

    print(f"Saved {out_json}")
    print(
        "Residual L2 final: "
        f"adam={res['adam']['final_residual_l2']:.3e}, "
        f"topological_adam={res['topological_adam']['final_residual_l2']:.3e}"
    )
    return 0


def run_symbolic_checks(args: argparse.Namespace) -> int:
    out_path = Path(args.output)
    try:
        write_symbolic_report(out_path, max_power=args.max_power)
    except ImportError as exc:
        raise SystemExit(str(exc))
    print(f"Saved {out_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mhd", description="mhd-toolkit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run a standard test problem")
    run.add_argument("problem", choices=["brio-wu", "orszag-tang", "reconnection-toy"])
    run.add_argument("--nx", type=int, default=256)
    run.add_argument("--ny", type=int, default=256)
    run.add_argument("--steps", type=int, default=50)
    run.add_argument("--closure", default="ideal")
    run.add_argument("--divfree", default="none", choices=["none", "projection", "glm"])
    run.add_argument("--gamma", type=float, default=1.4)
    run.add_argument("--cfl", type=float, default=0.35)
    run.add_argument("--eta", type=float, default=1e-3)
    run.add_argument("--nu", type=float, default=0.0)
    run.add_argument("--glm-ch", type=float, default=1.0)
    run.add_argument("--glm-cp", type=float, default=0.1)
    run.add_argument("--output-dir", default="results")
    run.set_defaults(func=run_problem)

    compare = sub.add_parser("compare", help="Comparison commands")
    compare_sub = compare.add_subparsers(dest="compare_command", required=True)
    cmp_closures = compare_sub.add_parser("closures", help="Compare closure models")
    cmp_closures.add_argument("--problem", default="brio-wu", choices=["brio-wu", "orszag-tang"])
    cmp_closures.add_argument("--closures", default="ideal,resistive")
    cmp_closures.add_argument("--nx", type=int, default=256)
    cmp_closures.add_argument("--ny", type=int, default=256)
    cmp_closures.add_argument("--steps", type=int, default=40)
    cmp_closures.add_argument("--divfree", default="none", choices=["none", "projection", "glm"])
    cmp_closures.add_argument("--gamma", type=float, default=1.4)
    cmp_closures.add_argument("--cfl", type=float, default=0.35)
    cmp_closures.add_argument("--eta", type=float, default=1e-3)
    cmp_closures.add_argument("--nu", type=float, default=0.0)
    cmp_closures.add_argument("--output-dir", default="results")
    cmp_closures.set_defaults(func=compare_closures)

    divfree = sub.add_parser("divfree", help="Divergence cleaning tools")
    div_sub = divfree.add_subparsers(dest="divfree_command", required=True)
    div_demo = div_sub.add_parser("demo", help="Run projection vs GLM demo")
    div_demo.add_argument("--problem", default="orszag-tang", choices=["orszag-tang"])
    div_demo.add_argument("--method", default="projection,glm")
    div_demo.add_argument("--nx", type=int, default=128)
    div_demo.add_argument("--ny", type=int, default=128)
    div_demo.add_argument("--gamma", type=float, default=5.0 / 3.0)
    div_demo.add_argument("--perturb", type=float, default=1e-2)
    div_demo.add_argument("--seed", type=int, default=1729)
    div_demo.add_argument("--glm-steps", type=int, default=30)
    div_demo.add_argument("--glm-dt", type=float, default=0.002)
    div_demo.add_argument("--glm-ch", type=float, default=1.0)
    div_demo.add_argument("--glm-cp", type=float, default=0.1)
    div_demo.add_argument("--output-dir", default="results")
    div_demo.set_defaults(func=divfree_demo)

    opt = sub.add_parser("opt", help="Optimization demos")
    opt_sub = opt.add_subparsers(dest="opt_command", required=True)
    residual = opt_sub.add_parser("residual-demo", help="Compare Adam vs Topological Adam on residual minimization")
    residual.add_argument("--nx", type=int, default=32)
    residual.add_argument("--ny", type=int, default=32)
    residual.add_argument("--eta", type=float, default=0.1)
    residual.add_argument("--steps", type=int, default=300)
    residual.add_argument("--output-dir", default="results")
    residual.set_defaults(func=run_opt_demo)

    research = sub.add_parser("research", help="Research-program utilities")
    research_sub = research.add_subparsers(dest="research_command", required=True)
    symbolic = research_sub.add_parser("symbolic-checks", help="Write the symbolic closure status report")
    symbolic.add_argument("--max-power", type=int, default=6)
    symbolic.add_argument("--output", default="data/generated/validation/symbolic_closure_report.json")
    symbolic.set_defaults(func=run_symbolic_checks)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
