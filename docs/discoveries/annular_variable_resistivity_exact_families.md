# Annular Variable-Resistivity Exact Families

## Main result

The earlier variable-resistivity story was:
- nonconstant `eta(r)` generically breaks the smooth exact cylindrical families.

That statement is still true, but it was incomplete.

A sharper classification now survives repeated symbolic checking:

### Family 1
For `alpha=f(r)`, `beta=r*theta`, the variable-resistivity residual is

$$
R = -\frac{(2 r f''(r) + f'(r))\,\eta'(r)}{r}\,e_z.
$$

So if `eta'(r)` is nonzero on an interval, exactness requires

$$
2 r f''(r) + f'(r) = 0,
$$

whose general solution is

$$
f(r) = a\sqrt{r} + b.
$$

This is exact on annular domains excluding the axis, but not smooth at `r=0`.

### Family 2
For `alpha=f(r)`, `beta=z`, the variable-resistivity residual is

$$
R = \frac{2(r f''(r) + f'(r))\,\eta'(r)}{r}\,e_\theta.
$$

So exactness under nonconstant `eta(r)` requires

$$
r f''(r) + f'(r) = 0,
$$

with general solution

$$
f(r) = a\log r + b.
$$

Again, this is annular/singular rather than smooth on axis-touching domains.

### Family 3
For `alpha=r*theta`, `beta=g(z)`, the residual carries both `g'(z)` and `g''(z)` terms multiplied by `eta'(r)`. If `eta'(r)` is nonzero on an interval, exactness forces only trivial constant `g`.

## Honest interpretation

This does not rescue the smooth variable-resistivity closure program.
It sharpens it.

What survives is not a broad smooth family but a narrow annular exact class. That is exactly the kind of restricted positive result worth keeping because it defines the true boundary instead of blurring it.

## Smooth axis-touching consequence

The same exact ODEs immediately force a sharper no-go on axis-touching domains for the supported radial families.

- For `alpha=f(r)`, `beta=r*theta`, the exact solutions are `f(r)=a*sqrt(r)+b`.
- For `alpha=f(r)`, `beta=z`, the exact solutions are `f(r)=a*log(r)+b`.

So if we additionally require the family to be smooth up to the axis, the only survivors are the trivial constants.

That means the current variable-resistivity picture is now genuinely two-sided:
- annular domains admit narrow singular exact survivors
- axis-touching smooth domains do not admit nonconstant survivors on these supported radial families
