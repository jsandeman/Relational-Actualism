# RA Graph Orientation Chart Work Packet — Apr 29 2026

This packet introduces `RA_GraphOrientationChart_v1.lean`, the next formal rung after `RA_IncidenceSignSource_v1.lean`.

## Install

```bash
cp RA_GraphOrientationChart_Work_Apr29_2026/lean/RA_GraphOrientationChart_v1.lean \
   src/RA_AQFT/
```

Add the Lake root after `RA_IncidenceSignSource_v1`:

```lean
`RA_IncidenceSignSource_v1,
`RA_GraphOrientationChart_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_GraphOrientationChart_v1.lean
lake build
```

## RAKB update

From `docs/RA_KB`:

```bash
cp /path/to/RA_GraphOrientationChart_Work_Apr29_2026/scripts/apply_graph_orientation_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_graph_orientation_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationChart_Work_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_graph_orientation_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationChart_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```
