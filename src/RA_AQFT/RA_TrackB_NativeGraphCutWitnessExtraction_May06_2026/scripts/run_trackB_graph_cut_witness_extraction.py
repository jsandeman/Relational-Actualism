#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from ra_native_graph_cut_witness_extraction import main

if __name__ == "__main__":
    main()
