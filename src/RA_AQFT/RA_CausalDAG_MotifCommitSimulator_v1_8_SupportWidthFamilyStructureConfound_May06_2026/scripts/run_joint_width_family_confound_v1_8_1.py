#!/usr/bin/env python3
"""v1.8.1 joint (support_width × family_size) stratified confound audit.

Refines v1.8 by stratifying simultaneously on support_width AND family_size
(plus mode, family_semantics, threshold_fraction, severity) before the
orientation tertile-bin gap is computed.
"""
from __future__ import annotations
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.ra_support_width_family_confound import run_joint_analysis  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Run RA v1.8.1 joint width x family-size stratified confound audit")
    ap.add_argument("--input-dir", required=True, help="Directory containing v1.7 ra_v1_7_keyed_trial_rows.csv")
    ap.add_argument("--output-dir", required=True, help="Output directory for v1.8.1 CSVs and summaries")
    args = ap.parse_args()
    summary = run_joint_analysis(args.input_dir, args.output_dir)
    print(json.dumps(asdict(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
