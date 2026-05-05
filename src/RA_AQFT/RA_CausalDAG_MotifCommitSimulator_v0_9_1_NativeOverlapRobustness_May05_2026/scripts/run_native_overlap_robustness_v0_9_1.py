#!/usr/bin/env python3
from pathlib import Path
import sys

# Ensure packet root is importable when run from scripts/.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.ra_native_overlap_robustness_analysis import main

if __name__ == "__main__":
    raise SystemExit(main())
