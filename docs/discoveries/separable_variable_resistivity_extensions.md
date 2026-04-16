# Separable Variable-Resistivity Extensions

## Main point

The current variable-resistivity program now extends beyond the special linear `z` family in one direction, and fails cleanly in another.

## Positive extension: `alpha=f(r)`, `beta=g(z)`

For nonconstant `eta(r)`, the residual is

$$
R = \frac{2(r f''(r) + f'(r))\,\eta'(r)\,g'(z)}{r}\,e_\theta.
$$

So if `eta'(r)` is nonzero on an interval and `g'(z)` is not identically zero, exactness requires

$$
r f''(r) + f'(r) = 0,
$$

with annular exact survivor

$$
f(r)=a\log r+b.
$$

This enlarges the earlier `beta=z` annular exact family to a broader separable `g(z)` branch.

## Negative extension: `alpha=f(r)`, `beta=r\theta g(z)`

For this family the residual has an `e_r` component proportional to

$$
\frac{2\eta(r) f'(r) g'(z)}{r}.
$$

So if `g'(z)` is not identically zero and `eta(r)` is positive, exactness forces `f'(r)=0`. Then `alpha` is constant and the magnetic field is trivial.

That means the only nontrivial exact survivors are the `g(z)=const` reductions of the previously known `beta=r\theta` family.

## Honest status

This is a real strengthening of the separable cylindrical program:
- one broader annular exact family survives
- one tempting broader extension dies cleanly

Neither statement is promoted beyond the supported cylindrical separable ansätze.
