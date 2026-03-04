# Diagnostics and Verification

## Diagnostics Object

Attach `Diagnostics(dim=1 or 2)` to solver runs.

Tracked values:

- `mass`, `momentum_x`, `momentum_y`, `momentum_z`
- `kinetic_energy`, `magnetic_energy`, `total_energy`
- `drift_*` values relative to initial state
- 2D divergence metrics:
  - `l2_divB`
  - `max_abs_divB`
  - `normalized_l2_divB`

## CFL Helpers

- `recommended_dt_1d`
- `recommended_dt_2d`

These are used internally by default stepping logic and also exposed for external workflows.

## Standardized Test Problems

- Brio-Wu (1D)
- Orszag-Tang (2D)
- Reconnection toy (2D)

## Verification in This Repo

- Pytest suite checks solver stability for short runs
- Divergence cleaning tests assert reduction of `||divB||` in controlled settings
- Closure tests verify deterministic outputs and shape stability
- CLI smoke tests validate command paths with small step counts
