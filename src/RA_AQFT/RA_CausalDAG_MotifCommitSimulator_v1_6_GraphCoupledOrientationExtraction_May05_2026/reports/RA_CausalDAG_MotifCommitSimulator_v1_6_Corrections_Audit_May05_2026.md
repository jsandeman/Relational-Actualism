# v1.6 Corrections Audit

This corrected v1.6 packet applies the audit recommendations before any RAKB promotion.

## Corrections applied

1. `graph_coupled_orientation_link_overlap` now computes all-pairs mean Jaccard across family-member orientation-link witnesses.
2. `v1_6_parent_anchored_orientation_link_overlap` is retained separately for the old parent-to-member diagnostic.
3. CLI now exposes `--severance-seeds`, `--modes`, `--severities`, `--threshold-fractions`, and `--family-semantics`.
4. README/report/proposals now describe the included outputs as a subset matched-graph diagnostic run, not a canonical run.
5. Partial-correlation narrative now matches the CSV: nonzero rescue residuals for ledger/orientation cells, zero residuals only for selector-stress controls.
6. Validation log regenerated: 6 tests pass when v0.9 simulator is available; isolated packet audits may skip the integration test if v0.9 is absent.

## Scientific posture

v1.6 establishes a methodological correction: rescue event and orientation-link overlap can be computed on the same v0.9 CausalDAG per trial. It retracts the use of v1.5 as independent cross-validation of v0.9.2. It does not establish robust reverse orientation specificity.
