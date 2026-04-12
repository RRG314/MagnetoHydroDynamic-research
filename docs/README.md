# mhd-toolkit

`mhd-toolkit` is a Python-first research toolkit for practical MHD workflows. It is not a full production simulator. It is built to give researchers clean tools for three recurring pain points:

1. Divergence control for magnetic field (`projection` and `GLM` cleaning)
2. Closure experimentation (`ideal`, `resistive`, `viscous` sandbox modules)
3. Diagnostics and verification (invariants, budgets, divergence metrics, smoke tests)

## What This Toolkit Is

- A modular codebase to test ideas quickly and reproducibly
- A baseline 1D and 2D finite-volume implementation (Rusanov flux)
- A place to compare divergence cleaning and closure effects with consistent diagnostics

## What This Toolkit Is Not

- Not a replacement for Athena, PLUTO, FLASH, or other mature production frameworks
- Not a full high-order AMR codebase
- Not a large GUI or rendering project

## Implemented Now

- 1D finite-volume solver (`FV1DSolver`) for conservative ideal MHD baseline
- 2D finite-volume solver (`FV2DSolver`) with split sweeps
- Divergence controls:
  - Projection cleaning via Poisson solve (`FFT periodic` or `Jacobi fallback`)
  - GLM cleaning with scalar `psi`
- Closure sandbox:
  - `ideal`
  - `resistive` (diffusive magnetic terms)
  - `viscous` (simple Laplacian momentum smoothing)
- Diagnostics object with JSON output:
  - total mass, momentum, kinetic, magnetic, and total energy
  - drift tracking relative to initial state
  - divergence metrics (`l2`, `max`, normalized)
- Test setups:
  - Brio-Wu (1D)
  - Orszag-Tang (2D)
  - Reconnection toy (2D)
- CLI with command families: `run`, `compare`, `divfree`, `opt`
- Topological Adam residual optimization module (experimental)

## Roadmap Snapshot

- Add HLL/HLLD interfaces and stronger reconstruction options
- Add explicit convergence harness automation for smooth-wave order checks
- Extend residual optimization demos to larger PDE residual classes
- Optional torch-backed optimizer integrations when environment supports it

## Benchmark Snapshot

- A concrete benchmark comparison report is included at [docs/benchmark_report.md](benchmark_report.md).
- It covers:
  - projection vs GLM divergence cleaning
  - ideal vs resistive closure on Brio-Wu
  - diagnostics sample output from Orszag-Tang

## Quick Start

Install in editable mode:

```bash
pip install -e .
```

Run a 1D case:

```bash
python -m mhd_toolkit run brio-wu --nx 800 --closure resistive --divfree none
```

Run a 2D case with divergence control:

```bash
python -m mhd_toolkit run orszag-tang --nx 256 --ny 256 --divfree projection
```

Compare closures:

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive
```

Divergence cleaning demo:

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --method projection,glm
```

Residual optimization demo:

```bash
python -m mhd_toolkit opt residual-demo
```

All commands save JSON outputs under `results/` by default.

## Core Docs

- [April 2026 Discovery Update](april_2026_discovery_update.md)
- [User Guide](user_guide.md)
- [Tool Reference](tool_reference.md)
- [CLI Reference](cli_reference.md)
- [Divergence Control](divergence_control.md)
- [Closure Sandbox](closure_sandbox.md)
- [Diagnostics and Verification](diagnostics_and_verification.md)
- [Topological Adam Branch Audit](topological_adam_branch_audit.md)
- [Paper References](paper_references.md)
