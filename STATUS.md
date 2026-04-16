# Status

## Theorem / Derivation-Level

- `alpha = f(r)`, `beta = r*theta` has exact closure under constant `eta`
- `alpha = f(r)`, `beta = z` has exact closure under constant `eta`
- `alpha = r*theta`, `beta = g(z)` has exact closure under constant `eta`
- `alpha = f(r)`, `beta = theta` is exact iff `f(r) = a*r^2 + b`

## Symbolically Verified Obstructions

- variable `eta(r)` generically breaks the smooth exact radial families above
- nonconstant `eta(r)` admits only annular/singular exact survivors `f(r)=a*sqrt(r)+b` in the `beta=r*theta` family
- nonconstant `eta(r)` admits only annular/singular exact survivors `f(r)=a*log(r)+b` in the `beta=z` family
- the same logarithmic annular survivor extends to the broader separable family `alpha=f(r), beta=g(z)`
- the extension `alpha=f(r), beta=r*theta*g(z)` has no nontrivial exact survivors unless `g` is constant
- nonconstant `eta(r)` leaves only trivial constant survivors in the `alpha=r*theta, beta=g(z)` family
- on the supported radial families, nonconstant `eta(r)` leaves no nonconstant smooth exact survivors on axis-touching domains
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
- whether the smooth-axis no-go extends to broader separable cylindrical families
- whether useful numerical closure corrections can be built for realistic `eta(r)` profiles
