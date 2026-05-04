#!/usr/bin/env bash
set -euo pipefail

# Usage: run from the root of the Lean project.
# Copies the uploaded/revised files into the project root and tries to build
# the motif-commit file.  If the full project target has unrelated broken roots,
# the direct `lake env lean` line gives a narrower diagnostic.

cp "${1:-/mnt/data}/RA_GraphCore(2).lean" ./RA_GraphCore.lean
cp "${1:-/mnt/data}/RA_O14_ArithmeticCore_v1(2).lean" ./RA_O14_ArithmeticCore_v1.lean
cp "${1:-/mnt/data}/RA_BDG_Coefficient_Arithmetic_v2.lean" ./RA_BDG_Coefficient_Arithmetic.lean
cp "${1:-/mnt/data}/RA_MotifCommitProtocol_v2.lean" ./RA_MotifCommitProtocol_v2.lean

if command -v lake >/dev/null 2>&1; then
  lake env lean RA_MotifCommitProtocol_v2.lean
else
  echo "lake not found on PATH; files copied but not compiled" >&2
fi
