# MHD Publication Figure Scripts

These scripts generate and validate figures used in `papers/mhd_paper_upgraded.md`.

## Generate figures

```bash
python scripts/figures/generate_publication_figures.py
```

## Validate figure presence

```bash
python scripts/figures/validate_publication_figures.py
```

Generated outputs:

- Figures: `figures/mhd/*.png` and `figures/mhd/*.pdf`
- Metrics: `data/generated/figures/mhd_publication_figure_metrics.json`
- Validation report: `data/generated/figures/mhd_publication_figure_validation.json`
