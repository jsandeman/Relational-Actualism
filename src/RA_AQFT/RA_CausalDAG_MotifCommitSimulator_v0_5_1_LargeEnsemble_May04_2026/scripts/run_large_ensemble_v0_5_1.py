#!/usr/bin/env python3
"""Convenience runner for RA causal-DAG simulator v0.5.1 large ensembles."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_ensemble import main

if __name__ == "__main__":
    main()
