# RAKB New Session Upload Checklist

Use this checklist when starting a fresh AI session.

## Minimal context bundle

Upload or zip the following:

```bash
zip -r RA_new_session_context_YYYYMMDD.zip \
  docs/RA_KB/README_RAKB_v0_5.md \
  docs/RA_KB/registry \
  docs/RA_KB/reports/RAKB_v0_5_1_release_notes_Apr28_2026.md \
  docs/RA_KB/reports/RAKB_stageD_node_coverage_matrix_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_stageD_gap_register_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_stageD_promotion_and_restoration_queue_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_stageD_evidence_health_summary_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_stageD_attention_index_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_stageC_paper_claim_crosswalk_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_python_source_classification_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_python_reproduction_smoke_tests_Apr28_2026.csv \
  docs/RA_KB/reports/RAKB_python_hardening_queue_Apr28_2026.csv \
  docs/RA_KB/reports/lake_build_Apr27_D2root_2026.log \
  docs/RA_KB/reports/lake_env_Apr27_2026.txt \
  docs/RA_Canonical_Papers/*.tex \
  docs/RA_Canonical_Papers/common
```

If those report filenames have changed, include the latest equivalents.

## Add Lean source bundle when doing formal work

```bash
zip -r RA_lean_source_context_YYYYMMDD.zip \
  src/RA_AQFT/*.lean \
  src/RA_AQFT/lakefile.lean \
  src/RA_AQFT/lakefile_v1.lean \
  src/RA_AQFT/lake-manifest.json \
  src/RA_AQFT/lean-toolchain \
  docs/RA_KB/reports/lake_build*.log \
  docs/RA_KB/reports/lake_env*.txt
```

## Add Python source bundle when doing computational work

```bash
zip -r RA_python_source_context_YYYYMMDD.zip \
  src/RA_AQFT/*.py \
  src/RA_AQFT/*.csv \
  src/RA_Complexity/*.py \
  src/ra_audit.py \
  data/DFT_Survey/*.py \
  docs/RA_KB/reports/python_audit*
```

## Add historical reference only for restoration/pruning work

```bash
zip -r RA_historical_restoration_context_YYYYMMDD.zip \
  docs/RA_History/RA_Programme_State_Apr16.md \
  docs/RA_History/RAKB_Update_Apr16.md \
  docs/RA_History/RA_Session_Log_Apr16.md \
  docs/RA_History/RA_Session_Log_Apr17.md \
  docs/RA_History/RA_Suite_Editorial_Catalog.md \
  docs/RA_History/RA_Papers_II_IV_Audit_Corrected_Framing_Apr23_2026.md
```

Do not upload entire docs/RA_History by default. Use specific historical sources only when the task is restoration, provenance, or over-pruning analysis.
