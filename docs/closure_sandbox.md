# Closure Sandbox

Closures are swappable modules used by the same solver API.

## Interface

Each closure implements:

- `apply_1d(U, context) -> source_terms`
- `apply_2d(U, context) -> source_terms`

`context` includes `dx`, optional `dy`, and `dt`.

## Included Closures

- `ideal`
  - No extra source terms
- `resistive`
  - Adds diffusive magnetic terms using Laplacians on `By`, `Bz`
- `viscous`
  - Simple Laplacian smoothing on momentum channels

## Compare Closures

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive,viscous
```

Output includes final energy drift and divergence metrics per closure.
