# RA Graph Orientation Closure Work Packet — Apr 29 2026

## Install Lean file

```bash
cp RA_GraphOrientationClosure_Work_Apr29_2026/lean/RA_GraphOrientationClosure_v1.lean \
   src/RA_AQFT/
```

Add Lake root after `RA_GraphOrientationChart_v1`:

```lean
`RA_GraphOrientationChart_v1,
`RA_GraphOrientationClosure_v1,
```

Then:

```bash
cd src/RA_AQFT
lake env lean RA_GraphOrientationClosure_v1.lean
lake build
```

## Apply RAKB upserts

From `docs/RA_KB`:

```bash
cp /path/to/RA_GraphOrientationClosure_Work_Apr29_2026/scripts/apply_graph_orientation_closure_v1_upserts.py scripts/

python scripts/apply_graph_orientation_closure_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationClosure_Work_Apr29_2026 \
  --dry-run

python scripts/apply_graph_orientation_closure_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationClosure_Work_Apr29_2026

python scripts/validate_rakb_v0_5.py
```

## Status

The Lean file is a static scaffold until locally compiled. It contains no generated `sorry`, `admit`, or `axiom` by static scan.
