# RAKB Stage C Paper Audit — April 28, 2026

This packet audits the canonical four-paper TeX suite against the current RAKB v0.5 registry and the April 16 historical RAKB update/session material.

## Main outputs

- `reports/RAKB_stageC_paper_claim_crosswalk_Apr28_2026.csv` — section-level map from canonical TeX sections to RAKB claims/issues/targets/restoration candidates.
- `reports/RAKB_stageC_historical_restoration_assessment_Apr28_2026.csv` — assessment of historical D09–D51 items against current canonical TeX.
- `reports/RAKB_stageC_overpruned_results_backlog_Apr28_2026.csv` — likely restoration/target backlog.
- `reports/RAKB_stageC_paper_action_queue_Apr28_2026.csv` — recommended paper/registry actions.
- `registry_upserts_v1/RAKB_stageC_source_text_references_upsert_v1_Apr28_2026.csv` — proposed source-text references.
- `registry_upserts_v1/RAKB_stageC_restoration_candidates_upsert_v1_Apr28_2026.csv` — proposed restoration candidates.
- `scripts/apply_rakb_stageC_upserts.py` — optional upsert helper.

## Summary

Historical D09–D51 assessment:

- present or explicitly handled in canonical suite: 23
- candidates for restoration or target tracking: 12
- absent but correctly demoted/archived under current framing: 8

Canonical sections mapped:

- mapped sections: 83 / 113
- distinct mapped node IDs: 63

## How to apply proposed registry upserts

From `docs/RA_KB`:

```bash
mkdir -p reports/patches/Apr28_stageC_v1

cp <this_packet>/registry_upserts_v1/*.csv reports/patches/Apr28_stageC_v1/
cp <this_packet>/reports/RAKB_stageC_*_Apr28_2026.csv reports/patches/Apr28_stageC_v1/
cp <this_packet>/scripts/apply_rakb_stageC_upserts.py scripts/

python scripts/apply_rakb_stageC_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_stageC_v1 \
  --reports ./reports \
  --dry-run

python scripts/apply_rakb_stageC_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_stageC_v1 \
  --reports ./reports

python scripts/validate_rakb_v0_5.py
```

Review before applying. The Stage C upserts include candidates, not all of which should become active claims.
