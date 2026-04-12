# Topological Adam Branch Audit

This note summarizes branch review of `RRG314/topological-adam` and what was integrated into `mhd-toolkit`.

## Branches Reviewed

- `origin/main`
- `origin/main1`
- `origin/paper`
- `origin/topological-adam-v2`
- `origin/steven/topological-adam-upgrade`

## What Was Found

### `main`

- Stable package structure with tests and optimizer implementations (`TopologicalAdam`, `TopologicalAdamV2`).
- Includes bounded topological correction behavior and stats tracking in current code.

### `topological-adam-v2`

- Adds `TopologicalAdamV2` path and related edge/convergence test updates.

### `steven/topological-adam-upgrade`

- Strongest hardening layer among reviewed branches.
- Adds improved optimizer safety patterns:
  - gradient sanitization and clipping
  - deterministic field initialization option
  - bounded topological correction ratio
  - additional parameter validation and stability guards

### `main1`

- Mostly README-oriented changes and a reduced code/test surface compared with `main`.

### `paper`

- Paper and notebook assets focused on manuscript context.
- Not structured as the strongest software baseline for direct toolkit dependency.

## Integration Decision for `mhd-toolkit`

The toolkit adopts the branch-audit direction from `main` plus safety ideas aligned with `steven/topological-adam-upgrade`.

Implemented in toolkit:
- `mhd_toolkit/opt/topological_adam.py`
  - bounded correction ratio
  - gradient sanitization
  - deterministic init option
  - energy-target stabilization controls
  - basic runtime stats
- `mhd_toolkit/opt/topological_adam_torch.py`
  - optional bridge loader to `topological-adam` torch package

## April 2026 Update

The latest discovery pass in the sibling `topological-adam` repository adds two points that matter for the toolkit's optimization story.

1. The coupling current `J_t` appears to track convergence strongly in the instrumented training experiment.
2. The target-energy regulation appears exact up to floating-point precision in the reported sweep.

These are still experimental findings, not production claims. But they reinforce the decision to keep Topological Adam in the toolkit as an explicitly experimental optimization path with visible field and energy diagnostics.

Immediate implication for `mhd-toolkit`:
- future residual optimization workflows should expose `J_t`, field-energy summaries, and related stopping or monitoring signals more directly.

## Scope Note

Topological Adam in this toolkit is for residual minimization experiments and is explicitly marked experimental.
