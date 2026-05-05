#!/usr/bin/env python3
"""CLI wrapper for v0.8 independent certified support families."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_independent_cert_families import main

if __name__ == "__main__":
    raise SystemExit(main())
