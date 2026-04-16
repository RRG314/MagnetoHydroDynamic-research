#!/usr/bin/env python3
"""Validate publication figures referenced by mhd_paper_upgraded.md."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "figures" / "mhd"
OUT_PATH = ROOT / "data/generated/figures/mhd_publication_figure_validation.json"

REQUIRED = [
    "mhd_remainder_constant_vs_variable_eta",
    "mhd_singularity_near_axis",
    "mhd_sheet_thinning_scaling",
    "mhd_axis_vs_annular_behavior",
]


def main() -> None:
    checks: dict[str, dict[str, object]] = {}
    all_passed = True

    for base in REQUIRED:
        png = FIG_DIR / f"{base}.png"
        pdf = FIG_DIR / f"{base}.pdf"
        png_ok = png.exists() and png.stat().st_size > 0
        pdf_ok = pdf.exists() and pdf.stat().st_size > 0
        checks[base] = {
            "png_exists": png_ok,
            "pdf_exists": pdf_ok,
            "png_bytes": png.stat().st_size if png.exists() else 0,
            "pdf_bytes": pdf.stat().st_size if pdf.exists() else 0,
        }
        all_passed = all_passed and png_ok and pdf_ok

    out = {"all_passed": all_passed, "checks": checks}
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
