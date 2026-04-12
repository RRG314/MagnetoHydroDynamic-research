# Variable Resistivity Obstructions

The most important current negative result is not a corner case. It is a program boundary.

## Main point

For nonconstant `eta(r)`, the smooth exact cylindrical families that survive under constant resistivity are generically broken.

Examples from the symbolic report:
- `alpha = f(r)`, `beta = r*theta`
- `alpha = f(r)`, `beta = z`
- `alpha = r*theta`, `beta = g(z)`

Each acquires explicit residual terms proportional to `eta'(r)`.

## Why this matters

This is the point where the current exact-closure story stops scaling cleanly toward realistic resistivity profiles.

That does not kill the program. It tells us where the exact theory ends and where perturbative or numerical closure corrections need to begin.
