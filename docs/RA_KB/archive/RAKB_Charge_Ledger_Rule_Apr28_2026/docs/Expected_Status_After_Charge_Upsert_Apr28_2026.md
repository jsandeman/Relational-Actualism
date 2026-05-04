# Expected status after charge/ledger upsert v1

Assuming the current validated RAKB state is:

```text
claims=39 issues=12 targets=7 framing=3 archived=2
claim_edges=58 all_dependency_edges=97 artifacts=187 claim_artifact_edges=180
```

Expected validator headline after applying this upsert:

```text
claims=39 issues=13 targets=7 framing=3 archived=2
claim_edges=60 all_dependency_edges=103 artifacts=188 claim_artifact_edges=187
```

The claim count remains unchanged because `RA-MOTIF-006` already exists and is refined in place. The issue count increases by one due to:

```text
RA-OPEN-CHARGE-SIGN-001
```

The artifact count increases by one if you copy/archive:

```text
reports/RAKB_Ledger_Rule_Analysis_Apr28_2026.md
```

and apply the accompanying artifact upsert.
