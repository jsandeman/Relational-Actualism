#!/usr/bin/env python3
"""Run v0.9 native certificate-overlap workbench from the packet root."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from simulator.ra_causal_dag_native_cert_overlap import main
if __name__ == "__main__":
    raise SystemExit(main())
