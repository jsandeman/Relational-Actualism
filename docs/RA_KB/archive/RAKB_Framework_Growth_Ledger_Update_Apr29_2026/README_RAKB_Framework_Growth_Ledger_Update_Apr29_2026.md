# RAKB Framework/Growth/Ledger Update Packet — Apr 29, 2026

This packet records the current RAGrowSim findings and the theoretical diagnosis of why the growth/ledger rule is underdetermined.

It is intentionally conservative:

- adds or updates open issues;
- adds simulation/report artifacts;
- adds issue-artifact evidence edges;
- does **not** modify settled claims;
- does **not** demote Poisson-based paper results;
- does **not** promote RAGrowSim as proof support.

## Apply from `docs/RA_KB`

First copy the script into your RAKB scripts directory:

```bash
cp /path/to/RAKB_Framework_Growth_Ledger_Update_Apr29_2026/scripts/apply_rakb_framework_upserts.py scripts/
```

Then dry-run:

```bash
python scripts/apply_rakb_framework_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RAKB_Framework_Growth_Ledger_Update_Apr29_2026 \
  --dry-run
```

Then apply:

```bash
python scripts/apply_rakb_framework_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RAKB_Framework_Growth_Ledger_Update_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Expected effects

Against your current post-Python/post-Stage-C state, if none of these hold issues were previously applied, the expected headline movement is approximately:

```text
issues: +7
all_dependency_edges: +31
artifacts: +7
claim_artifact_edges: +22
```

If an earlier hold packet was already applied, the script updates those rows instead of duplicating them.


Depending on whether earlier hold packets were already applied, the upsert will add/update up to seven issues:

```text
RA-OPEN-GROWTH-MEASURE-001
RA-OPEN-FRONTIER-NORMAL-FORM-001
RA-OPEN-POISSON-DYNAMICS-001
RA-OPEN-MU-ESTIMATOR-001
RA-OPEN-GROWTH-KERNEL-WEIGHT-001
RA-OPEN-CHARGE-SIGN-001
RA-OPEN-TOPOLOGICAL-LEDGER-001
```

It will also add seven artifacts and issue-artifact evidence edges.

## Main report

Read first:

```text
reports/RAKB_Framework_Underdetermination_and_Topological_Ledger_Report_Apr29_2026.md
```

## Recommended commit

```bash
git add registry reports scripts
git commit -m "RAKB: add growth-measure and topological-ledger methodology issues"
```
