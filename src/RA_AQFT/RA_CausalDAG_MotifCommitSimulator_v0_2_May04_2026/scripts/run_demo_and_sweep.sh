#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python simulator/ra_causal_dag_simulator.py \
  --steps 24 \
  --seed 17 \
  --conflict-rate 0.30 \
  --defect-rate 0.12 \
  --run-sweep
