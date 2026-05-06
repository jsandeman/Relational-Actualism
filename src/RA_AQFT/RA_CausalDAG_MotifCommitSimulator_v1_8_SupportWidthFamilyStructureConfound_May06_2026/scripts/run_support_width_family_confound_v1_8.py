#!/usr/bin/env python3
from pathlib import Path
import sys, argparse
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.ra_support_width_family_confound import run_analysis

ap = argparse.ArgumentParser(description='Run RA v1.8 support-width/family-structure confound audit over v1.7 outputs.')
ap.add_argument('--input-dir', required=True, help='Directory containing v1.7 outputs, especially ra_v1_7_keyed_trial_rows.csv')
ap.add_argument('--output-dir', required=True)
args = ap.parse_args()
summary = run_analysis(args.input_dir, args.output_dir)
print(summary)
