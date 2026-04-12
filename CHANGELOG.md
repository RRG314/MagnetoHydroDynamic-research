# Changelog

## v1.0.0

- Reframed the repository as a theory-first research program under the MagnetoHydroDynamic Research identity.
- Added canonical overview, proof-status, derivation, and strongest-results documents.
- Added a reusable symbolic closure module and research CLI path.
- Promoted the strongest exact-family and obstruction results into the main documentation path.
- Added reproducible symbolic validation scripts and generated reports.
- Kept the Topological Adam connection visible, but clearly secondary to the closure theory program.

## Unreleased
- Added `docs/april_2026_discovery_update.md` to capture the latest symbolic closure and optimizer-facing research update.
- Added `examples/mhd_novel_experiments.py` so the April 2026 symbolic closure work lives in the toolkit as a runnable research example.
- Updated Topological Adam audit and roadmap docs to reflect the newest `J_t` / energy-regulation findings and the variable-resistivity closure direction.
- Added a research-program layer with proof-status docs, start-here docs, symbolic closure code, validation scripts, and generated-report paths.
- Promoted the strongest symbolic findings into canonical discovery and derivation docs instead of leaving them only in a memo-style update.
- Added a `research symbolic-checks` CLI command and symbolic regression tests.
- Moved the included draft PDFs into `papers/drafts/` to make the repo read more like a research repository than a toolkit dump.

## 0.1.0
- Initial public draft of `mhd-toolkit`.
- Implemented 1D and 2D finite-volume baseline solvers (Rusanov flux).
- Added divergence control tools: projection cleaning and GLM cleaning.
- Added closure sandbox: ideal, resistive, and simple viscous closures.
- Added diagnostics object for invariants, divergence metrics, and budget drift.
- Added standard test setups: Brio-Wu, Orszag-Tang, and reconnection toy.
- Added CLI workflows, runnable examples, and pytest smoke tests.
- Added residual minimization optimization demos with Adam and TopologicalAdam placeholder.
