#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.ra_joint_width_family_confound import run_analysis

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Run RA v1.8.1 joint width × family-size confound audit.")
    ap.add_argument("--input-dir", required=True, help="Directory containing v1.7 outputs, especially ra_v1_7_keyed_trial_rows.csv")
    ap.add_argument("--output-dir", required=True, help="Output directory")
    args = ap.parse_args()
    summary = run_analysis(args.input_dir, args.output_dir)
    print(summary)
