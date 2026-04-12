# Status

## Theorem / Derivation-Level

- `alpha = f(r)`, `beta = r*theta` has exact closure under constant `eta`
- `alpha = f(r)`, `beta = z` has exact closure under constant `eta`
- `alpha = r*theta`, `beta = g(z)` has exact closure under constant `eta`
- `alpha = f(r)`, `beta = theta` is exact iff `f(r) = a*r^2 + b`

## Symbolically Verified Obstructions

- variable `eta(r)` generically breaks the smooth exact radial families above
- the earlier cylindrical bilinear case `alpha = r*theta`, `beta = r*z` becomes non-exact for `eta = eta(r)`

## Numerically Verified Toolkit Paths

- solver smoke tests
- closure comparison CLI
- divergence-cleaning demo
- residual-optimization demo

## Experimental / Bridge Work

- Topological Adam connection remains exploratory
- the bridge is documented, but it is not the core claim of this repo

## Open

- perturbative closure corrections for slowly varying resistivity
- broader classification of exact cylindrical and toroidal families
- whether useful numerical closure corrections can be built for realistic `eta(r)` profiles
