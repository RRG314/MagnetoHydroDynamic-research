# MHD Final Report

## Final Structure

- `README.md`: theory-first repository overview
- `STATUS.md`: current classification of exact, symbolic, numerical, and open results
- `RESEARCH_MAP.md`: research-program map
- `FILE_INDEX.md`: key-file index
- `ROADMAP.md`: main next directions
- `docs/overview/`: start-here and strongest-results layer
- `docs/discoveries/`: canonical discovery notes
- `docs/theorems/`: proof-status map
- `docs/derivations/`: compact derivation notes
- `docs/limitations/`: current boundaries
- `mhd_toolkit/research/`: symbolic closure program code
- `scripts/validate/`: reproducibility entry points
- `data/generated/validation/`: generated symbolic reports
- `papers/drafts/`: included draft PDFs

## What Changed

- Reframed the repository from "toolkit with scattered research notes" into a clearer theory-first research program.
- Added a symbolic closure module with reusable residual and report-generation functions.
- Added a research CLI path: `python -m mhd_toolkit research symbolic-checks`.
- Added symbolic regression tests for exact families and obstruction cases.
- Added start-here, strongest-results, proof-status, derivation, and limitations docs.
- Moved included draft PDFs into `papers/drafts/`.
- Kept the Topological Adam connection, but clearly as a secondary bridge topic.

## Canonical Versions Chosen

- canonical symbolic source: `mhd_toolkit/research/symbolic_closures.py`
- canonical symbolic report: `data/generated/validation/symbolic_closure_report.json`
- canonical start document: `docs/overview/start-here.md`
- canonical proof-status document: `docs/theorems/proof_status.md`

## What Was Archived or Repositioned

- the April 2026 memo-style update remains, but it is no longer the canonical presentation of the results
- draft PDFs were moved from `docs/papers/` to `papers/drafts/`
- the broad experiment script remains in `examples/mhd_novel_experiments.py`, but the canonical regression path is now the symbolic research module plus validation scripts

## Strongest Results Highlighted

1. Under constant resistivity, the cylindrical families
   - `alpha = f(r), beta = r*theta`
   - `alpha = f(r), beta = z`
   - `alpha = r*theta, beta = g(z)`
   are exact in the implemented symbolic framework.
2. For `alpha = f(r), beta = theta`, exactness holds iff `f(r) = a*r^2 + b`.
3. For nonconstant `eta(r)`, the broad smooth exact radial families are generically broken by explicit residual terms proportional to `eta'(r)`.
4. The earlier power-family memo result is now understood as a special case of a broader radial exact class.

## Tests Run

- `python -m pytest -q` -> `18 passed`
- `bash scripts/validate/run_all.sh` -> passed
- generated reports:
  - `data/generated/validation/symbolic_closure_report.json`
  - `data/generated/validation/cli_symbolic_report.json`

## Reproducibility Status

Working direct entry points:
- `python scripts/validate/run_research_checks.py`
- `python -m mhd_toolkit research symbolic-checks`
- `python -m mhd_toolkit compare closures ...`
- `python -m mhd_toolkit divfree demo ...`
- `python -m mhd_toolkit opt residual-demo ...`

## Remaining Open Issues

- perturbative closure corrections for slowly varying `eta(r)` are not yet built
- toroidal work remains exploratory relative to the cylindrical proofs
- the numerical toolkit remains baseline-grade, not a production MHD simulator

## Recommended Next Steps

1. develop the perturbative `eta = eta_0 + epsilon * eta_1(r)` correction program
2. search for broader exact-family criteria tied to magnetic-field component structure
3. test numerical closure corrections against the explicit symbolic obstruction formulas
4. expand toroidal cases only after the cylindrical classification is fully consolidated
