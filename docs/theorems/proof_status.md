# Proof Status

| ID | Statement | Status | Evidence | Key Files | Next Step |
| --- | --- | --- | --- | --- | --- |
| MHD-T1 | `alpha = f(r), beta = r*theta` is exact for constant `eta` | THEOREM | direct derivation + symbolic verification | `mhd_toolkit/research/symbolic_closures.py`, `docs/derivations/cylindrical_exact_families.md` | extend beyond cylindrical radial ansatz |
| MHD-T2 | `alpha = f(r), beta = z` is exact for constant `eta` | THEOREM | direct derivation + symbolic verification | same | classify relation to field-component structure |
| MHD-T3 | `alpha = r*theta, beta = g(z)` is exact for constant `eta` | THEOREM | direct derivation + symbolic verification | same | determine whether broader mixed separable classes survive |
| MHD-T4 | `alpha = f(r), beta = theta` is exact iff `f(r) = a*r^2 + b` | THEOREM | residual formula solved directly | same | test analogous conditional families |
| MHD-O1 | nonconstant `eta(r)` breaks smooth exactness for `alpha = f(r), beta = r*theta`, but annular exactness survives for `f(r) = a*sqrt(r) + b` | THEOREM | explicit residual formula + solved ODE + symbolic verification | `mhd_toolkit/research/symbolic_closures.py`, `docs/discoveries/annular_variable_resistivity_exact_families.md` | classify broader annular families |
| MHD-O2 | nonconstant `eta(r)` breaks smooth exactness for `alpha = f(r), beta = z`, but annular exactness survives for `f(r) = a*log(r) + b` | THEOREM | explicit residual formula + solved ODE + symbolic verification | same | classify broader annular families |
| MHD-O3 | nonconstant `eta(r)` leaves only trivial constant-`g` survivors in `alpha = r*theta, beta = g(z)` | THEOREM | explicit residual formula + symbolic verification | same | classify mixed families beyond this ansatz |
| MHD-B1 | Topological Adam is a useful bridge application of the structure | EXPERIMENTAL | sibling repo diagnostics | `docs/discoveries/topological_adam_bridge.md` | keep secondary and honest |
