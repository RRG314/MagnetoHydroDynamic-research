# April 2026 Discovery Update

This note records the new MHD-facing results and related optimizer observations added from the April 2026 discovery pass.

## What Was Added

- `examples/mhd_novel_experiments.py`
  - symbolic closure experiments carried over from the latest discovery work
- documentation updates in the toolkit README, docs index, roadmap, and Topological Adam audit note

## MHD Closure Findings Added Here

The symbolic experiment script now captures two concrete closure results that matter for the toolkit's research direction.

### 1. New exactly-closed non-bilinear family

The script verifies a new cylindrical family of Euler potentials of the form

```text
alpha = r^n, beta = r theta
```

for positive integers `n`, where the residual closure term vanishes in the tested symbolic setup.

Why this matters:
- it expands the currently visible exact-closure landscape beyond the bilinear cases emphasized in the existing draft
- it gives the toolkit a cleaner test case for exact closure behavior in cylindrical coordinates
- it points toward a classification problem rather than a one-off example

### 2. Variable-resistivity obstruction

The same discovery pass shows that when the cylindrical bilinear case

```text
alpha = r theta, beta = r z
```

is paired with a simple variable resistivity profile

```text
eta = eta0 r,
```

a nonzero residual appears and the smooth analytic closure attempt breaks down.

Why this matters:
- it marks a clear boundary on where the current closure story stops being exact
- it pushes the toolkit toward perturbative or numerical closure corrections for realistic non-constant `eta`
- it gives a useful regression target for future symbolic and numerical closure experiments

## Topological Adam Update Relevant To This Toolkit

The sibling `topological-adam` repository now includes a matching discovery note and an instrumented training experiment.

Key optimizer-facing observations:
- the coupling current `J_t` tracks convergence strongly in the tested training run
- the target-energy regulation appears exact up to floating-point precision in the reported sweep
- the optimizer shows a reconnection-style three-phase trajectory in the logged experiments

These findings do not turn the optimizer into a physical plasma model. They do, however, strengthen the case for exposing `J_t`, energy regulation, and related diagnostics more explicitly in residual-optimization workflows.

## Practical Toolkit Implications

Near-term consequences for `mhd-toolkit`:
- keep exact and experimental closure results clearly separated in docs and examples
- add more symbolic closure examples before promoting any broader closure claim
- expose richer optimizer diagnostics in the residual optimization path
- treat variable-resistivity closure as an active research problem, not a solved feature

## How To Use The New Example

From the repository root:

```bash
python3 examples/mhd_novel_experiments.py
```

This script is a research example, not a production solver component. It is included so the new symbolic work is preserved in the toolkit repo in a runnable form.
