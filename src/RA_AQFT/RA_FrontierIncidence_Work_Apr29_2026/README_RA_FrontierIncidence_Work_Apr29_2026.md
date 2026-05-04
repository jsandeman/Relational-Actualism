# RA Frontier / Incidence Work Packet — April 29, 2026

This packet advances the Selector Closure theorem ladder from the compiled abstract selector scaffold to a first frontier/incidence scaffold.

## Files

```text
lean/RA_FrontierIncidence_v1.lean
formalization_notes/RA_Frontier_Incidence_Normal_Form_Programme_Apr29_2026.md
reports/RA_FrontierIncidence_First_Formalization_Report_Apr29_2026.md
registry_upserts_frontier_v1/*.csv
scripts/apply_frontier_v1_upserts.py
```

## Lean install/check

Copy the Lean file into the same source directory as `RA_ActualizationSelector_v1.lean`:

```bash
cp lean/RA_FrontierIncidence_v1.lean src/RA_AQFT/
cd src/RA_AQFT
lake env lean RA_FrontierIncidence_v1.lean
```

Keep the file out of active Lake roots initially unless you intentionally want it in the active build surface.

## Registry upsert

From `docs/RA_KB`:

```bash
cp /path/to/RA_FrontierIncidence_Work_Apr29_2026/scripts/apply_frontier_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_frontier_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierIncidence_Work_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_frontier_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierIncidence_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

Expected effect:

```text
artifacts.csv: +3
claim_artifact_edges.csv: +9
```

If existing rows are present, the script updates instead of duplicating.
