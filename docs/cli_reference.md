# CLI Reference

The main entry point is:

```bash
python -m mhd_toolkit ...
```

If installed as script:

```bash
mhd ...
```

## `run`

Run a standard problem.

```bash
mhd run brio-wu --nx 800 --closure resistive --divfree none
mhd run orszag-tang --nx 256 --ny 256 --divfree projection
mhd run reconnection-toy --nx 256 --ny 256 --divfree glm
```

Key flags:
- `--steps`
- `--closure`
- `--divfree`
- `--eta`, `--nu`
- `--glm-ch`, `--glm-cp`
- `--output-dir`

## `compare closures`

Compare multiple closures on one problem.

```bash
mhd compare closures --problem brio-wu --closures ideal,resistive,viscous
```

## `divfree demo`

Compare divergence cleaning methods from a shared perturbed B-field baseline.

```bash
mhd divfree demo --problem orszag-tang --method projection,glm
```

Useful GLM tuning flags:
- `--glm-steps`
- `--glm-dt`
- `--glm-ch`
- `--glm-cp`

## `opt residual-demo`

Run residual minimization comparison.

```bash
mhd opt residual-demo --nx 40 --ny 40 --steps 300
```

## Output Conventions

Most commands save:
- JSON summary in `results/`
- optional PNG plot when matplotlib is available
