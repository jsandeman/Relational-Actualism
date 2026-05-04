# RAKB Actualization Selector Update — Apr29 2026

This packet supersedes the earlier hold-only framework/growth-measure packets if they have not yet been applied.
It records the new kernel insight:

```text
selector before measure
```

That is: RA should seek a graph-native actualization selector / relational completion rule, and treat
probability measures as derived coarse-grained shadows rather than primitive hat-draw randomness.

## Contents

```text
registry_upserts_selector_v1/
  RAKB_selector_issues_upsert_v1_Apr29_2026.yaml
  RAKB_selector_artifacts_upsert_v1_Apr29_2026.csv
  RAKB_selector_claim_artifact_edges_upsert_v1_Apr29_2026.csv
reports/
  RAKB_Actualization_Selector_Framework_Report_Apr29_2026.md
formalization_notes/
  RA_Selector_Closure_Theorem_Programme_Apr29_2026.md
lean_scaffold/
  RA_ActualizationSelector_Scaffold.lean
scripts/
  apply_rakb_selector_upserts.py
data_summaries/
  RAGrowSim_selector_reframing_summary_Apr29_2026.csv
```

## Apply from docs/RA_KB

```bash
cp /path/to/RAKB_Actualization_Selector_Update_Apr29_2026/scripts/apply_rakb_selector_upserts.py scripts/

python scripts/apply_rakb_selector_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RAKB_Actualization_Selector_Update_Apr29_2026 \
  --dry-run

python scripts/apply_rakb_selector_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RAKB_Actualization_Selector_Update_Apr29_2026

python scripts/validate_rakb_v0_5.py
```

## Expected count movement

If no prior framework/growth/ledger hold packets were applied, expect approximately:

```text
issues: +11 net new, plus 1 existing issue update (RA-KERNEL-004)
artifacts: +4
claim_artifact_edges: +15
all_dependency_edges: +52 added / +2 updated dependency edges on the base v0.5 migration
```

If prior growth-measure/ledger hold packets were already applied, expect fewer new issues and more updates.
The script is idempotent: repeated runs update existing rows rather than duplicating them.

## Important status discipline

This packet does **not** prove determinism and does **not** demote existing Poisson-layer claims. It records
the selector programme as the next critical kernel target.
