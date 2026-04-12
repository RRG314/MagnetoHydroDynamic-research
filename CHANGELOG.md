# Changelog

## Unreleased
- Added `docs/april_2026_discovery_update.md` to capture the latest symbolic closure and optimizer-facing research update.
- Added `examples/mhd_novel_experiments.py` so the April 2026 symbolic closure work lives in the toolkit as a runnable research example.
- Updated Topological Adam audit and roadmap docs to reflect the newest `J_t` / energy-regulation findings and the variable-resistivity closure direction.

## 0.1.0
- Initial public draft of `mhd-toolkit`.
- Implemented 1D and 2D finite-volume baseline solvers (Rusanov flux).
- Added divergence control tools: projection cleaning and GLM cleaning.
- Added closure sandbox: ideal, resistive, and simple viscous closures.
- Added diagnostics object for invariants, divergence metrics, and budget drift.
- Added standard test setups: Brio-Wu, Orszag-Tang, and reconnection toy.
- Added CLI workflows, runnable examples, and pytest smoke tests.
- Added residual minimization optimization demos with Adam and TopologicalAdam placeholder.
