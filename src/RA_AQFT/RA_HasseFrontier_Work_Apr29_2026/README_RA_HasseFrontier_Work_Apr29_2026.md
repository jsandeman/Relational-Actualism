# RA Hasse Frontier Work Packet — April 29, 2026

## Contents

```text
lean/RA_HasseFrontier_v1.lean
formalization_notes/RA_HasseFrontier_Programme_Apr29_2026.md
reports/RA_HasseFrontier_First_Formalization_Report_Apr29_2026.md
registry_upserts_hasse_v1/RAKB_hasse_v1_artifacts_upsert_Apr29_2026.csv
registry_upserts_hasse_v1/RAKB_hasse_v1_claim_artifact_edges_upsert_Apr29_2026.csv
scripts/apply_hasse_v1_upserts.py
patches/patch_lakefile_add_hasse_frontier_root.diff
```

## Install Lean file

Copy into the RA Lean source directory:

```bash
cp RA_HasseFrontier_Work_Apr29_2026/lean/RA_HasseFrontier_v1.lean \
   src/RA_AQFT/
```

Add the root after the selector/frontier/graph bridge roots:

```lean
`RA_ActualizationSelector_v1,
`RA_FrontierIncidence_v1,
`RA_FrontierGraphBridge_v1,
`RA_HasseFrontier_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_HasseFrontier_v1.lean
lake build
```

## RAKB update

From `docs/RA_KB`:

```bash
cp /path/to/RA_HasseFrontier_Work_Apr29_2026/scripts/apply_hasse_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_hasse_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_HasseFrontier_Work_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_hasse_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_HasseFrontier_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Expected registry movement

```text
artifacts.csv: +3
claim_artifact_edges.csv: +8
```

If rows already exist, the script updates them instead of duplicating them.
