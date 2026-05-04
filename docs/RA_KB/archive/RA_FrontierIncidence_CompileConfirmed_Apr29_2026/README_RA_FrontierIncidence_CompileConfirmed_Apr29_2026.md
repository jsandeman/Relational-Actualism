# RA Frontier/Incidence Compile-Confirmed Update — Apr 29, 2026

This packet updates the RAKB status for `RA_FrontierIncidence_v1.lean` after local compile success.

## Apply from `docs/RA_KB`

```bash
cp /path/to/RA_FrontierIncidence_CompileConfirmed_Apr29_2026/scripts/apply_frontier_v2_compile_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_frontier_v2_compile_upserts.py   --registry ./registry   --reports ./reports   --packet-root /path/to/RA_FrontierIncidence_CompileConfirmed_Apr29_2026   --dry-run
```

Apply:

```bash
python scripts/apply_frontier_v2_compile_upserts.py   --registry ./registry   --reports ./reports   --packet-root /path/to/RA_FrontierIncidence_CompileConfirmed_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Lakefile root recommendation

If `RA_FrontierIncidence_v1` is now meant to be reproducibly checked by `lake build`, add both selector files to the Lake roots:

```lean
`RA_ActualizationSelector_v1,
`RA_FrontierIncidence_v1,
```

A patch template is included under `patches/`.
