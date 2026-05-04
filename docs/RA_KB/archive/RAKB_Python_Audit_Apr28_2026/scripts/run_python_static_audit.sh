#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
OUT="${2:-docs/RA_KB/reports/python_audit_Apr28_2026}"
python "$ROOT/docs/RA_KB/scripts/ra_python_static_audit.py" \
  --repo "$ROOT" \
  --out "$OUT" \
  --roots src/RA_AQFT src/RA_Complexity data/DFT_Survey src/ra_audit.py
