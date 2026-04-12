# Cylindrical Exact Families

## Setup

Work in cylindrical physical components with

```text
B = grad(alpha) x grad(beta)
```

and compare

```text
eta * Lap(B)
```

against the naive closure built from `eta * Lap(alpha)` and `eta * Lap(beta)`.

## Family 1: `alpha = f(r), beta = r*theta`

Then

```text
grad(alpha) = (f'(r), 0, 0)
grad(beta) = (theta, 1, 0)
B = (0, 0, f'(r))
```

The magnetic field has only a `z` component, so the cylindrical vector Laplacian reduces to the scalar Laplacian of `f'(r)`, and the naive closure reproduces it exactly.

## Family 2: `alpha = f(r), beta = z`

Then

```text
B = (0, -f'(r), 0)
```

Again the cylindrical vector Laplacian and the naive closure align exactly.

## Conditional family: `alpha = f(r), beta = theta`

The residual simplifies to a scalar multiple of

```text
-r*f''(r) + f'(r)
```

So exactness holds iff

```text
r*f''(r) = f'(r)
```

which integrates to

```text
f(r) = a*r^2 + b
```

This is why the quadratic case survives while generic higher powers do not in this family.
