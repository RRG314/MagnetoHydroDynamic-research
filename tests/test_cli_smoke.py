from __future__ import annotations

import subprocess
import sys


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "mhd_toolkit", *args], capture_output=True, text=True)


def test_cli_smoke_run_brio(tmp_path) -> None:
    p = run_cmd(["run", "brio-wu", "--nx", "64", "--steps", "5", "--output-dir", str(tmp_path)])
    assert p.returncode == 0, p.stderr


def test_cli_smoke_run_orszag(tmp_path) -> None:
    p = run_cmd([
        "run",
        "orszag-tang",
        "--nx",
        "32",
        "--ny",
        "32",
        "--steps",
        "5",
        "--divfree",
        "projection",
        "--output-dir",
        str(tmp_path),
    ])
    assert p.returncode == 0, p.stderr


def test_cli_smoke_compare_and_opt(tmp_path) -> None:
    p1 = run_cmd([
        "compare",
        "closures",
        "--problem",
        "brio-wu",
        "--closures",
        "ideal,resistive",
        "--steps",
        "5",
        "--nx",
        "64",
        "--output-dir",
        str(tmp_path),
    ])
    assert p1.returncode == 0, p1.stderr

    p2 = run_cmd([
        "divfree",
        "demo",
        "--problem",
        "orszag-tang",
        "--nx",
        "32",
        "--ny",
        "32",
        "--output-dir",
        str(tmp_path),
    ])
    assert p2.returncode == 0, p2.stderr

    p3 = run_cmd(["opt", "residual-demo", "--steps", "40", "--output-dir", str(tmp_path)])
    assert p3.returncode == 0, p3.stderr
