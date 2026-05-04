# RA Frontier/Graph Bridge Compile-Confirmed Packet — Apr 29 2026

This packet updates RAKB after local warning-free compilation of:

```text
src/RA_AQFT/RA_FrontierGraphBridge_v1.lean
```

## Apply from `docs/RA_KB`

```bash
cp /path/to/RA_FrontierGraphBridge_CompileConfirmed_Apr29_2026/scripts/apply_frontier_graph_v2_compile_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_frontier_graph_v2_compile_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierGraphBridge_CompileConfirmed_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_frontier_graph_v2_compile_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierGraphBridge_CompileConfirmed_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Expected effect

If the v1 Frontier/Graph Bridge upsert was already applied, this packet updates the existing Lean artifact/edges to:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom_warning_free
```

and adds one compile-confirmation report artifact.

If v1 was not applied, this packet also inserts the relevant rows.
