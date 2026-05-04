# RAKB v0.4.5 Validation Cleanup Audit

## Main changes
- Added `superseded_wrapper` to schema enum and used it for MotifDynamics wrapper artifacts.
- Removed unused enum values `uploaded_wrapper_user_verified` and `not_applicable_textual_reference`.
- Filtered macOS resource-fork files (`._*`, `__MACOSX/`) and duplicate-download Lean files (`(1).lean`, etc.) from artifact inventory.
- Collapsed `RA-LLC-001` source ambiguity to `RA_GraphCore_Native.lean` only.
- Added `RA_prose_only_DR_audit_v0_4_5.csv` to expose DR claims with no file-backed artifact source.

## Counts
- Results: 63
- Artifact inventory rows: 97
- Proof edges: 97
- Prose-only DR nodes: 12

## Schema / inventory enum validation
- Inventory statuses not in schema: None
- Schema statuses unused in inventory: ['not_uploaded_in_current_audit', 'uploaded_uncompiled_imports_pending']

## Garbage inventory rows after filtering
- 0

## Missing proof dependencies
- None

## Prose-only DR nodes
- RA-KERNEL-003 — Finite potentia (kernel, support=none)
- RA-GRAV-004 — Severed-link entropy observable (gravity, support=none)
- RA-GRAV-005 — Discrete boundary law (gravity, support=none)
- RA-COMP-001 — Tier hierarchy (complexity, support=none)
- RA-COMP-002 — Recursive closure (complexity, support=none)
- RA-COMP-004 — RA assembly depth (complexity, support=none)
- RA-COMP-005 — Glycolysis assembly depth estimate (complexity, support=PI)
- RA-COMP-006 — E. coli assembly depth estimate (complexity, support=PI)
- RA-COMP-007 — Origin-of-life sandwich bound (complexity, support=PI)
- RA-COMP-008 — Substrate-independent biosignature criteria (complexity, support=PI)
- RA-NONTARGET-001 — Born rule as non-target (framing, support=CC)
- RA-NONTARGET-003 — Metric field as non-primitive (framing, support=CC)