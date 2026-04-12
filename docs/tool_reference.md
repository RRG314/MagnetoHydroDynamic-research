# Tool Reference

This file explains what each toolkit module is for.

## Core Package Layout

### `mhd_toolkit/config.py`

- `SolverConfig`: central runtime options (closure, divergence cleaner, CFL, physical coefficients).

### `mhd_toolkit/grids/uniform.py`

- `UniformGrid1D`, `UniformGrid2D`: uniform grid helper objects.

### `mhd_toolkit/equations/`

- `mhd_ideal.py`
  - Conservative variable indexing
  - pressure, flux functions, characteristic speed estimates
  - primitive-to-conservative conversion
- `mhd_resistive.py`
  - baseline resistive source terms
- `induction.py`
  - Laplacian operators used by closure and residual tools

### `mhd_toolkit/numerics/`

- `fluxes.py`
  - Rusanov flux
- `recon.py`
  - PLM/minmod reconstruction in 1D
- `timestep.py`
  - CFL timestep helpers for 1D and 2D

### `mhd_toolkit/closures/`

- `base.py`
  - closure interface and context
- `ideal.py`
  - no-op closure
- `resistive.py`
  - magnetic diffusion source terms
- `viscous.py`
  - baseline Laplacian momentum smoothing
- `__init__.py`
  - closure factory (`make_closure`)

### `mhd_toolkit/divfree/`

- `projection.py`
  - projection cleaning with Poisson solve
- `glm.py`
  - GLM cleaner with scalar `psi`
- `metrics.py`
  - divergence field and summary metrics

### `mhd_toolkit/diagnostics/`

- `invariants.py`
  - mass/momentum/energy totals
- `budgets.py`
  - `Diagnostics` tracker with drift history + JSON export
- `cfl.py`
  - recommended timestep wrappers
- `divergence.py`
  - divergence report helpers
- `shock_sensors.py`
  - simple density-gradient shock sensors

### `mhd_toolkit/solvers/`

- `fv1d.py`
  - 1D finite-volume solver
- `fv2d.py`
  - 2D finite-volume solver with optional divergence cleaning hooks

### `mhd_toolkit/opt/`

- `adam.py`
  - NumPy Adam optimizer
- `topological_adam.py`
  - NumPy Topological Adam (experimental, stabilized)
- `topological_adam_torch.py`
  - optional loader for torch-based `topological-adam` package
- `residual.py`
  - toy steady residual objective and optimizer comparison harness

### `mhd_toolkit/tests/problems/`

- `brio_wu.py`
  - Brio-Wu initial condition helper
- `orszag_tang.py`
  - Orszag-Tang initial condition helper
- `reconnection_toy.py`
  - reconnection toy setup helper

### `mhd_toolkit/cli.py`

- Entry point for all command-line workflows.

## Example Scripts

- `examples/compare_closures.py`
  - CLI wrapper for closure comparison output generation
- `examples/residual_solve_demo.py`
  - CLI wrapper for residual optimization demo
- `examples/mhd_novel_experiments.py`
  - symbolic closure-discovery experiment imported from the April 2026 research pass
