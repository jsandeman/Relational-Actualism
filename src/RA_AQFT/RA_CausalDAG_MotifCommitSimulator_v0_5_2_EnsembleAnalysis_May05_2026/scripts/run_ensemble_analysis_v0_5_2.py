#!/usr/bin/env python3
"""CLI wrapper for RA v0.5.2 ensemble severance-signature analysis."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.ra_causal_dag_ensemble_analysis import main

if __name__ == "__main__":
    raise SystemExit(main())
