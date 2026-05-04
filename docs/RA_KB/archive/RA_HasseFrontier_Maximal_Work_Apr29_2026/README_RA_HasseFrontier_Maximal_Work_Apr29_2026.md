# RA Hasse Frontier Maximal Work Packet — Apr 29 2026

## Contents

```text
lean/RA_HasseFrontier_Maximal_v1.lean
formalization_notes/RA_HasseFrontier_Maximal_Programme_Apr29_2026.md
reports/RA_HasseFrontier_Maximal_First_Formalization_Report_Apr29_2026.md
registry_upserts_hasse_maximal_v1/*.csv
scripts/apply_hasse_maximal_v1_upserts.py
patches/patch_lakefile_add_hasse_frontier_maximal_root.diff
```

## Install

Copy the Lean file:

```bash
cp RA_HasseFrontier_Maximal_Work_Apr29_2026/lean/RA_HasseFrontier_Maximal_v1.lean \
   src/RA_AQFT/
```

Add the Lake root after `RA_HasseFrontier_v1`:

```lean
`RA_HasseFrontier_v1,
`RA_HasseFrontier_Maximal_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_HasseFrontier_Maximal_v1.lean
lake build
```

## Apply RAKB upserts

From `docs/RA_KB`:

```bash
cp /path/to/RA_HasseFrontier_Maximal_Work_Apr29_2026/scripts/apply_hasse_maximal_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_hasse_maximal_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_HasseFrontier_Maximal_Work_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_hasse_maximal_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_HasseFrontier_Maximal_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```
