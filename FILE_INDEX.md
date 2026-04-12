# File Index

## Core symbolic research

- `mhd_toolkit/research/symbolic_closures.py`
  - symbolic closure identities, obstruction formulas, and report generation
- `tests/test_symbolic_closures.py`
  - symbolic regression tests for the strongest exact and non-exact claims

## Reproducibility

- `scripts/validate/run_research_checks.py`
  - writes the canonical symbolic report JSON
- `scripts/validate/run_all.sh`
  - full local validation entry point
- `experiments/symbolic/generate_symbolic_report.py`
  - direct symbolic report generator

## Theory and discovery docs

- `docs/overview/start-here.md`
- `docs/overview/strongest-results.md`
- `docs/overview/reproduce-key-checks.md`
- `docs/derivations/cylindrical_exact_families.md`
- `docs/theorems/proof_status.md`
- `docs/discoveries/non_bilinear_exact_families.md`
- `docs/discoveries/variable_resistivity_obstructions.md`
- `docs/discoveries/topological_adam_bridge.md`

## Toolkit code

- `mhd_toolkit/cli.py`
  - main CLI including solver, comparison, optimization, and symbolic report commands
- `mhd_toolkit/closures/`
  - ideal, resistive, and viscous closure sandbox
- `mhd_toolkit/solvers/`
  - finite-volume baselines
- `mhd_toolkit/divfree/`
  - projection and GLM divergence control
- `mhd_toolkit/opt/`
  - residual optimization and Topological Adam bridge utilities
