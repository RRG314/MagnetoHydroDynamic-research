# MHD System Report

## Main Code Paths

- `mhd_toolkit/research/symbolic_closures.py`: symbolic derivation engine and closure classification
- `tests/test_symbolic_closures.py`: direct symbolic verification and regression checks
- `docs/derivations/cylindrical_exact_families.md`: constant-resistivity derivation lane
- `docs/discoveries/variable_resistivity_obstructions.md`: obstruction layer
- `docs/discoveries/annular_variable_resistivity_exact_families.md`: restricted positive variable-eta lane
- `docs/discoveries/separable_variable_resistivity_extensions.md`: broader separable-family extension and failure lane
- `docs/discoveries/smooth_axis_variable_resistivity_no_go.md`: smooth-axis no-go on the supported radial families

## Validation Path

```bash
cd /Users/stevenreid/Documents/New\ project/mhd-toolkit
python3 -m pytest tests/test_symbolic_closures.py
python3 scripts/validate/run_research_checks.py
```

## Evidence Discipline

- theorem-level results come from closed-form residual formulas and exact solution of the resulting ODEs
- the new smooth-axis no-go is a direct consequence of the exact annular survivor ODEs, not a separate numerical guess
- symbolic verification is used as a cross-check, not a replacement for the derivation statements
- exploratory optimizer bridges remain separate from the main closure claims
