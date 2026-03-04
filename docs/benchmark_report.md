# Benchmark Report

Generated from local runs on 2026-03-04 using the current `mhd-toolkit` implementation.

## 1) Divergence Cleaning: Projection vs GLM

Command:

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --method projection,glm --nx 96 --ny 96 --output-dir results
```

Source data: `results/divfree_demo_orszag_tang.json`

| Method | L2(divB) Before | L2(divB) After | Reduction Factor | Max |divB| Before | Max |divB| After | Energy Change |
|---|---:|---:|---:|---:|---:|---:|
| Projection | 9.5905e-01 | 6.9091e-01 | 0.7204x | 3.9935e+00 | 2.6254e+00 | -2.1523e-05 |
| GLM | 9.5905e-01 | 7.9382e-02 | 0.0828x | 3.9935e+00 | 3.0228e-01 | -4.8363e-05 |

Observed behavior:
- Both methods reduced divergence from the same perturbed baseline.
- In this setup, GLM gave stronger divergence reduction than one-shot projection.
- Both methods introduced small magnetic energy changes, with GLM slightly larger magnitude in this run.

## 2) Closure Comparison: Ideal vs Resistive

Command:

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive --nx 512 --steps 60 --output-dir results
```

Source data: `results/compare_closures_brio_wu.json`

| Closure | Steps | Final Sim Time | Drift Total Energy | Drift Magnetic Energy | L2(divB) |
|---|---:|---:|---:|---:|---:|
| ideal | 60 | 1.1237e-02 | 0.0000e+00 | -3.2798e-02 | 0.0000e+00 |
| resistive (`eta=1e-3`) | 60 | 5.6490e-04 | 9.0649e+00 | 4.5150e-03 | 0.0000e+00 |

Observed behavior:
- Ideal closure preserved total energy in this baseline finite-volume setup (within reported precision).
- The current resistive closure model is intentionally simple and introduces strong energy drift at this parameter choice.
- This confirms the sandbox utility: closure variants are easy to compare, and problematic behavior is visible in diagnostics.

## 3) Diagnostics Sample Output

Command:

```bash
python -m mhd_toolkit run orszag-tang --nx 96 --ny 96 --steps 20 --divfree projection --closure ideal --output-dir results
```

Source data: `results/run_orszag_tang.json`

Selected final diagnostics:

- `mass`: 2.2105e-01
- `kinetic_energy`: 1.0934e-01
- `magnetic_energy`: 3.8644e-02
- `total_energy`: 4.8189e-01
- `l2_divB`: 1.8157e-04
- `max_abs_divB`: 2.8304e-03
- `normalized_l2_divB`: 6.5311e-04
- `drift_total_energy`: 0.0000e+00
- `drift_kinetic_energy`: -1.1181e-03
- `drift_magnetic_energy`: -1.0890e-03

This run shows the intended output style for verification workflows: budgets, divergence, and drift are all tracked in machine-readable form.

## Notes

- These are baseline finite-volume results with Rusanov flux and lightweight closures.
- The divergence cleaning and closure APIs are designed for extension, not final production-grade accuracy claims.
