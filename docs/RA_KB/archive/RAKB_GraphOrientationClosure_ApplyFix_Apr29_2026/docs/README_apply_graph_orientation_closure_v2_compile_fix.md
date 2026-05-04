# Fixed RAKB apply script: Graph Orientation Closure compile confirmation

The earlier apply script only printed an instruction. This replacement actually upserts the packet CSV rows into:

- `registry/artifacts.csv`
- `registry/claim_artifact_edges.csv`

It creates timestamped backups before writing.

## Install

```bash
cp RAKB_GraphOrientationClosure_ApplyFix_Apr29_2026/scripts/apply_graph_orientation_closure_v2_compile_upserts.py \
   docs/RA_KB/scripts/
chmod +x docs/RA_KB/scripts/apply_graph_orientation_closure_v2_compile_upserts.py
```

## Run from `docs/RA_KB`

```bash
python scripts/apply_graph_orientation_closure_v2_compile_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationClosure_CompileConfirmed_Apr29_2026 \
  --dry-run
```

Then apply:

```bash
python scripts/apply_graph_orientation_closure_v2_compile_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_GraphOrientationClosure_CompileConfirmed_Apr29_2026
```

Then validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Notes

- CSV files are registry upserts, not `git apply` patches.
- The script discovers the correct upsert CSVs under `--packet-root`.
- If an existing row has the same key, non-empty patch fields update that row.
- If no existing row has the key, the row is appended.
