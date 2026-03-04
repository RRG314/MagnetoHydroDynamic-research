# Getting Started

## 1) Install

```bash
pip install -e .
```

Optional plotting support:

```bash
pip install -e .[viz]
```

## 2) First Runs

1D Brio-Wu:

```bash
python -m mhd_toolkit run brio-wu --nx 400 --steps 80 --closure ideal
```

2D Orszag-Tang with projection cleaning:

```bash
python -m mhd_toolkit run orszag-tang --nx 128 --ny 128 --steps 40 --divfree projection
```

## 3) Compare Tools

Closures:

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive,viscous --steps 40
```

Divergence cleaning:

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --method projection,glm
```

## 4) Run Tests

```bash
pytest
```

## 5) Output Layout

- `results/*.json`: run summaries and metrics
- `results/*_diagnostics.json`: time-series budget logs
- optional `results/*.png`: quick plots when matplotlib is installed
