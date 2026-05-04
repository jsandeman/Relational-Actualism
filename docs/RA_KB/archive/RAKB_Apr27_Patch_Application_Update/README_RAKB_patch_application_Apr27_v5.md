# RAKB Apr 27 v5 patch application guide

## What "apply the patches" meant

The files named `RAKB_*_patch_*.csv` were **not Git diffs** and were not meant to be run with `git apply`.

They were **registry upsert tables**:

- `artifact_patch...csv` = rows to add/update in `docs/RA_KB/registry/artifacts.csv`
- `claim_artifact_edge_patch...csv` = rows to add/update in `docs/RA_KB/registry/claim_artifact_edges.csv`
- `support_status_upgrades...csv` = an audit/report table recording why support statuses changed
- `restoration_candidates...csv` = rows for a restoration queue, not necessarily active claims yet

"Apply" therefore means: merge these rows into the corresponding KB tables using stable keys.

## Which patch version to use

Do **not** apply v3 and v4 separately.

Use this v5 packet instead:

```text
registry_patch_v5/RAKB_artifacts_upsert_v5_D2_build_confirmed_Apr27_2026.csv
registry_patch_v5/RAKB_claim_artifact_edges_upsert_v5_D2_build_confirmed_Apr27_2026.csv
registry_patch_v5/RAKB_restoration_candidates_upsert_v5_D2_build_confirmed_Apr27_2026.csv
registry_patch_v5/RAKB_support_status_upgrades_v5_D2_build_confirmed_Apr27_2026.csv
```

v5 supersedes v3/v4 and updates `RA_D2_HadronMassTriad.lean` based on the new lakefile root.

## Recommended repo placement

From the RA repo root:

```bash
mkdir -p docs/RA_KB/reports/patches/Apr27_v5
cp registry_patch_v5/*.csv docs/RA_KB/reports/patches/Apr27_v5/
cp scripts/apply_rakb_upserts.py docs/RA_KB/scripts/
```

## Apply safely

First do a dry run:

```bash
python docs/RA_KB/scripts/apply_rakb_upserts.py   --registry docs/RA_KB/registry   --patch-dir docs/RA_KB/reports/patches/Apr27_v5   --reports docs/RA_KB/reports   --dry-run
```

Then apply:

```bash
python docs/RA_KB/scripts/apply_rakb_upserts.py   --registry docs/RA_KB/registry   --patch-dir docs/RA_KB/reports/patches/Apr27_v5   --reports docs/RA_KB/reports
```

Then validate:

```bash
python docs/RA_KB/scripts/validate_rakb_v0_5.py
```

## D2/HadronMassTriad status

Your updated lakefile includes:

```lean
`RA_D2_HadronMassTriad
```

as an active root. Therefore this packet upgrades the artifact from:

```text
uploaded_static_audited_not_lake_build_confirmed
```

to:

```text
user_reported_lake_build_confirmed_no_sorry_updated_lakefile_pending_fresh_log
```

The remaining caveat is reproducibility: archive a fresh `lake_build_*.log` generated after the D2 root was added. Once that log is archived, the status can be hardened to:

```text
lean_build_confirmed_no_sorry
```

## Why the D2 theorem is still a restoration candidate

`RA_D2_HadronMassTriad.lean` can be build-confirmed as a formal source without immediately becoming a canonical RAKB claim.

The current recommendation is:

1. Track it in `registry/restoration_candidates.csv`.
2. Add candidate support edge from `RA-PRED-002` to `ART-LEAN-RA_D2_HadronMassTriad`.
3. Promote `RA-MATTER-HADRON-TRIAD-001` to `claims.yaml` only after the Paper II mapping decides the exact claim statement and epistemic tier.

This avoids creating a dangling active claim before the TeX/pruning audit.
