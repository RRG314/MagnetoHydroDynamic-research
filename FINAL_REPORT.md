# MHD Final Report

## What This Repo Is

A theorem-first MHD closure research repository centered on Euler-potential exactness, variable-resistivity obstruction theory, symbolic verification, and honest separation between theorem-level structure and exploratory bridge work.

## Strongest Current Results

### Proved
- constant-resistivity cylindrical exact families:
  - `alpha=f(r), beta=r*theta`
  - `alpha=f(r), beta=z`
  - `alpha=r*theta, beta=g(z)`
- conditional exactness for `alpha=f(r), beta=theta` iff `f(r)=a*r^2+b`

### Newly sharpened in this pass
- for nonconstant `eta(r)`, the radial-`r*theta` family is exact only if `2 r f'' + f' = 0`, giving the annular exact family `f(r)=a*sqrt(r)+b`
- for nonconstant `eta(r)`, the radial-`z` family is exact only if `r f'' + f' = 0`, giving the annular exact family `f(r)=a*log(r)+b`
- for nonconstant `eta(r)`, `alpha=r*theta, beta=g(z)` has only trivial constant-`g` survivors when `eta'(r)` is nonzero on an interval

These survivors are not smooth axis-touching families. They are annular/singular survivors, which sharpens the obstruction boundary without pretending variable resistivity is hopeless in every setting.

## Strongest Honest Novelty Assessment

- the constant-resistivity cylindrical exact families are repo-real and mathematically clean; literature distinctness remains to be checked carefully before any stronger claim
- the annular/singular variable-resistivity survivors are sharper than the earlier generic-obstruction statement and are worth keeping as a real restricted positive/negative classification boundary
- broad physical claims about reconnection or tokamak relevance remain unsupported unless derived more carefully

## Best Next Targets

1. prove or kill broader annular exact families beyond the current cylindrical radial ansatz
2. classify whether any smooth nonconstant-eta exact family survives on axis-touching domains
3. build perturbative correction theory for `eta(r)=eta0+eps*eta1(r)` beyond first-order obstruction terms
4. test spherical/toroidal analogues under the same falsification standard
