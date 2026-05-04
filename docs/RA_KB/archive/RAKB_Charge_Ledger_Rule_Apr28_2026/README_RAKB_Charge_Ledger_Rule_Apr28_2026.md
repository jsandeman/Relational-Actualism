# RAKB Charge / Ledger Rule Upsert — Apr 28, 2026

This packet updates the RAKB treatment of electric charge and the open sign-source problem.

## Why this is an update, not a new duplicate claim

The current RAKB already contains:

```text
RA-MOTIF-006 — Signed three-direction charge spectrum
```

Therefore this packet refines `RA-MOTIF-006` in place and adds:

```text
RA-OPEN-CHARGE-SIGN-001 — Edge-level sign-source for signed N1 charge
```

`RA-MATTER-CHARGE-001` is added only as an alias inside the `RA-MOTIF-006` YAML node.

## Files

```text
registry_upserts_charge_v1/
  RAKB_charge_claim_issue_upsert_v1_Apr28_2026.yaml
  RAKB_charge_claim_edges_upsert_v1_Apr28_2026.csv
  RAKB_charge_issue_edges_upsert_v1_Apr28_2026.csv
  RAKB_charge_all_dependency_edges_upsert_v1_Apr28_2026.csv
  RAKB_charge_artifacts_upsert_v1_Apr28_2026.csv
  RAKB_charge_claim_artifact_edges_upsert_v1_Apr28_2026.csv
  RAKB_charge_source_text_references_upsert_v1_Apr28_2026.csv

reports/
  RAKB_Ledger_Rule_Analysis_Apr28_2026.md

scripts/
  apply_rakb_charge_upserts.py

lean_formalization_notes/
  RA_D1_ChargeLedger_Formalization_Notes_Apr28_2026.md
```

## Apply from `docs/RA_KB`

Copy the files:

```bash
mkdir -p reports/patches/Apr28_charge_v1
cp <packet>/registry_upserts_charge_v1/* reports/patches/Apr28_charge_v1/
cp <packet>/reports/RAKB_Ledger_Rule_Analysis_Apr28_2026.md reports/patches/Apr28_charge_v1/
cp <packet>/scripts/apply_rakb_charge_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_rakb_charge_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_charge_v1 \
  --reports ./reports \
  --dry-run
```

Apply:

```bash
python scripts/apply_rakb_charge_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_charge_v1 \
  --reports ./reports
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Expected headline counts

Starting from the current validated state:

```text
claims=39 issues=12 targets=7 framing=3 archived=2
claim_edges=58 all_dependency_edges=97 artifacts=187 claim_artifact_edges=180
```

expected result:

```text
claims=39 issues=13 targets=7 framing=3 archived=2
claim_edges=60 all_dependency_edges=103 artifacts=188 claim_artifact_edges=187
```

The claim count stays fixed because `RA-MOTIF-006` already exists and is refined rather than duplicated.

## Conceptual status

```text
RA-MOTIF-006:
  seven-value signed N1/electric translation claim
  status: derived_native, source_backed_pending_edge_sign_formalization

RA-OPEN-CHARGE-SIGN-001:
  formalization target for s(edge, local_context) -> {-1,0,+1}
  status: open
```

The report argues that the best candidate rule is topological in the finite graph sense: an incidence/cochain rule on an oriented local DAG complex.
