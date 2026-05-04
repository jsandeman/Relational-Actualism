# RAKB Stage D Synthesis Packet — Apr 28 2026

This packet is a synthesis/release-readiness layer, not a broad new registry migration.

## Main files

- `RAKB_StageD_Synthesis_Report_Apr28_2026.md`
- `RAKB_v0_5_1_release_notes_Apr28_2026.md`
- `reports/RAKB_stageD_node_coverage_matrix_Apr28_2026.csv`
- `reports/RAKB_stageD_gap_register_Apr28_2026.csv`
- `reports/RAKB_stageD_promotion_and_restoration_queue_Apr28_2026.csv`
- `reports/RAKB_stageD_evidence_health_summary_Apr28_2026.csv`
- `reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv`
- `reports/RAKB_stageD_attention_index_Apr28_2026.csv`

## Optional v0.5.1 registry hardening upsert

This only hardens D2/HadronMassTriad build evidence and adds the fresh D2-root Lake build log artifact.

From `docs/RA_KB`:

```bash
mkdir -p reports/patches/Apr28_stageD_v0_5_1
cp <packet>/registry_upserts_v0_5_1/*.csv reports/patches/Apr28_stageD_v0_5_1/
cp <packet>/scripts/apply_rakb_stageD_v0_5_1_upserts.py scripts/

python scripts/apply_rakb_stageD_v0_5_1_upserts.py   --registry ./registry   --patch-dir ./reports/patches/Apr28_stageD_v0_5_1   --dry-run

python scripts/apply_rakb_stageD_v0_5_1_upserts.py   --registry ./registry   --patch-dir ./reports/patches/Apr28_stageD_v0_5_1

python scripts/validate_rakb_v0_5.py
```

## Optional Lean warning patch

```bash
git apply <packet>/patches/patch_RA_D3_CosmologicalExpansion_unused_hN2.diff
lake build
```

The patch is cosmetic: it silences the unused-variable warning and should not change theorem content.
