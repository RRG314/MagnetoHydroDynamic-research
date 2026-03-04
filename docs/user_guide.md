# User Guide

This guide explains how to use each major toolkit capability in practice.

## 1) Installation

```bash
pip install -e .
```

Optional plotting support:

```bash
pip install -e .[viz]
```

## 2) Running Standard Problems

### Brio-Wu (1D)

```bash
python -m mhd_toolkit run brio-wu --nx 512 --steps 80 --closure ideal
```

Expected output:
- `results/run_brio_wu.json`
- `results/run_brio_wu_diagnostics.json`

### Orszag-Tang (2D)

```bash
python -m mhd_toolkit run orszag-tang --nx 128 --ny 128 --steps 40 --divfree projection
```

Expected output:
- `results/run_orszag_tang.json`
- `results/run_orszag_tang_diagnostics.json`

## 3) Divergence Control Workflows

### Direct comparison of projection vs GLM

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --method projection,glm --nx 96 --ny 96
```

Output:
- `results/divfree_demo_orszag_tang.json`
- optional `results/divfree_demo_l2.png`

Interpreting fields in JSON:
- `before_l2_divB`, `after_l2_divB`
- `before_max_abs_divB`, `after_max_abs_divB`
- `energy_change`
- `runtime_seconds`

## 4) Closure Sandbox Workflows

### Compare ideal and resistive closure

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive --steps 60
```

Output:
- `results/compare_closures_brio_wu.json`
- optional `results/compare_closures_brio_wu_energy.png`

Interpretation:
- Compare `drift_total_energy`, `drift_magnetic_energy`, and `l2_divB` across closures.

## 5) Residual Optimization Workflow

### Adam vs Topological Adam on a steady toy residual

```bash
python -m mhd_toolkit opt residual-demo --nx 40 --ny 40 --steps 300
```

Output:
- `results/residual_demo.json`
- optional `results/residual_demo.png`

## 6) Programmatic Usage

### Solver API

```python
from mhd_toolkit.config import SolverConfig
from mhd_toolkit.solvers import FV1DSolver
from mhd_toolkit.tests.problems import brio_wu

x, U0 = brio_wu.initial_state(256, gamma=1.4)
solver = FV1DSolver(SolverConfig(closure="ideal", divfree="none"), x, U0)
summary = solver.run(steps=20)
print(summary)
```

### Diagnostics API

```python
from mhd_toolkit.diagnostics import Diagnostics

diag = Diagnostics(dim=1)
diag.observe(solver.U, solver.time, solver.dx)
print(diag.latest())
```

## 7) Reproducibility Tips

- Keep all benchmark outputs in `results/`
- Record CLI command strings used to generate each report
- Commit JSON outputs for paper-ready runs when needed
- Use fixed seeds in custom experiments when random perturbations are applied

## 8) Known Limits

- The current numerical core is intentionally lightweight.
- Resistive and viscous closures are baseline models intended for experimentation and comparison.
- For production-grade studies, treat this toolkit as a prototyping and validation layer.
