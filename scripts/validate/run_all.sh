#!/usr/bin/env bash
set -euo pipefail

python -m pytest -q
python scripts/validate/run_research_checks.py
python -m mhd_toolkit research symbolic-checks --output data/generated/validation/cli_symbolic_report.json
