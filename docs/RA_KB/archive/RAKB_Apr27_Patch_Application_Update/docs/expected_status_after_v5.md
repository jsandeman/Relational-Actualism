# Expected RAKB status after Apr 27 v5 upserts

## Lean formal surface

- Active formal source surface: externally/user build-confirmed, no sorry/admit reported.
- Build environment: Lean 4.29.0 / Lake 5.0.0, commit `2698aa72490ef585692f1d708ec3c92d6d555bba`.
- One interface axiom remains: `axiom CausalGraph : Type` in `RA_D1_NativeDimensionality_v1.lean`.
- One previously observed linter warning remains unless separately patched: unused variable `hN2` in `RA_D3_CosmologicalExpansion.lean`.

## D2/HadronMassTriad

- `RA_D2_HadronMassTriad.lean` is now an active Lake root in the updated lakefile.
- Status: `user_reported_lake_build_confirmed_no_sorry_updated_lakefile_pending_fresh_log`.
- It should remain a restoration candidate until Paper II claim mapping chooses the exact typed claim.

## Obsolete patch CSVs

The following are superseded by v5:

```text
RAKB_artifact_patch_v3_build_confirmed_Apr27_2026.csv
RAKB_claim_artifact_edge_patch_v3_build_confirmed_Apr27_2026.csv
RAKB_support_status_upgrades_build_confirmed_Apr27_2026.csv

RAKB_artifact_patch_v4_final_build_Apr27_2026.csv
RAKB_claim_artifact_edge_patch_v4_final_build_Apr27_2026.csv
RAKB_support_status_upgrades_v4_final_build_Apr27_2026.csv
RAKB_restoration_candidates_patch_v4_final_build_Apr27_2026.csv
```
