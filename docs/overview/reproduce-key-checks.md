# Reproduce Key Checks

## Symbolic report

```bash
python scripts/validate/run_research_checks.py
```

or

```bash
python -m mhd_toolkit research symbolic-checks
```

## Closure comparison baseline

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive --steps 20 --nx 128
```

## Divergence-cleaning demo

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --nx 64 --ny 64
```

## Residual optimization demo

```bash
python -m mhd_toolkit opt residual-demo --steps 80
```
