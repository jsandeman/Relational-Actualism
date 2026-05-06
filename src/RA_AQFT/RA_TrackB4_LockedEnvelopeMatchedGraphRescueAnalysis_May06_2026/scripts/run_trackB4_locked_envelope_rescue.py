#!/usr/bin/env python3
from pathlib import Path
import argparse, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.ra_trackB4_locked_envelope_rescue import run_analysis


def parse_args():
    ap=argparse.ArgumentParser(description='Track B.4 locked-envelope matched-graph rescue analysis')
    ap.add_argument('--input-dirs', default='', help='Comma-separated output dirs containing v1.7/B.3b trial rows')
    ap.add_argument('--input-files', default='', help='Comma-separated explicit CSV files to analyze')
    ap.add_argument('--output-dir', default='outputs')
    ap.add_argument('--min-rows-per-bin', type=int, default=25)
    return ap.parse_args()

if __name__=='__main__':
    ns=parse_args()
    dirs=[Path(x) for x in ns.input_dirs.split(',') if x]
    files=[Path(x) for x in ns.input_files.split(',') if x]
    summary=run_analysis(dirs, Path(ns.output_dir), files, ns.min_rows_per_bin)
    print(summary)
