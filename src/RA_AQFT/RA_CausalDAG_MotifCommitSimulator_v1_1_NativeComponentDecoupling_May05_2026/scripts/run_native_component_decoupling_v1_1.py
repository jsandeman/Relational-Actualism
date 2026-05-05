#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.ra_native_component_decoupling import main

if __name__ == "__main__":
    raise SystemExit(main())
