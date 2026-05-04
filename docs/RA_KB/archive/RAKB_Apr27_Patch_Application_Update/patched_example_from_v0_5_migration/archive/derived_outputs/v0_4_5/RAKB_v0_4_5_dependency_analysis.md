# RAKB v0.4.5 Dependency Analysis

This is a validation-cleanup patch. Proof topology is unchanged from v0.4.4; artifact inventory is cleaner and source-status enum now validates.

## Top proof-leverage nodes
- **RA-ONT-001 — Finite causal graph ontology** (STATED/none): reach 57, direct proof children 5.
- **RA-ONT-003 — Structured potentia / adjacent possible** (STATED/none): reach 49, direct proof children 3.
- **RA-KERNEL-001 — Four-dimensional BDG acceptance kernel** (ANC/none): reach 48, direct proof children 8.
- **RA-ONT-002 — Irreversible actualization** (STATED/none): reach 31, direct proof children 1.
- **RA-LLC-001 — Local Ledger Condition** (STATED/none): reach 30, direct proof children 5.
- **RA-ARITH-001 — BDG coefficient arithmetic spine** (ANC/none): reach 27, direct proof children 7.
- **RA-D4-001 — D4U02 selectivity ceiling** (DR/CV): reach 23, direct proof children 4.
- **RA-MOTIF-001 — Native motif sector definition** (STATED/none): reach 15, direct proof children 1.
- **RA-MOTIF-002 — Stable motif census** (ANC/none): reach 14, direct proof children 5.
- **RA-GRAV-001 — Kernel–Poisson divergence identity** (DR/CV): reach 13, direct proof children 3.
- **RA-ONT-004 — Finitary Actuality** (STATED/none): reach 10, direct proof children 3.
- **RA-COMP-001 — Tier hierarchy** (DR/none): reach 10, direct proof children 2.
- **RA-KERNEL-002 — Kernel locality** (ANC/none): reach 9, direct proof children 2.
- **RA-MOTIF-005 — Depth-2 ledger/orientation structure** (ANC/none): reach 6, direct proof children 4.
- **RA-COMP-002 — Recursive closure** (DR/none): reach 6, direct proof children 2.

## What the prose-only DR audit means
Prose-only DR nodes are not necessarily weak or wrong. They are informal derivations currently backed by paper prose rather than Lean/Python/MD source artifacts. They should be prioritized for formalization only when they sit on high-leverage paths or support quantitative claims.

## Remaining actions
1. Decide whether the complexity-sector prose-only DR claims should receive MD derivations or Lean/Python formal support.
2. Locate or archive `RA-MOTIF-009` Type IV exact-zero support.
3. Audit exploratory scripts before upgrading prediction nodes.