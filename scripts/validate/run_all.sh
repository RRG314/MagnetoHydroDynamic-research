#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="/Users/stevenreid/Documents/New project/.venv_research/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" -m pytest -q
"$PYTHON_BIN" scripts/validate/run_research_checks.py
"$PYTHON_BIN" -m mhd_toolkit research symbolic-checks --output data/generated/validation/cli_symbolic_report.json
