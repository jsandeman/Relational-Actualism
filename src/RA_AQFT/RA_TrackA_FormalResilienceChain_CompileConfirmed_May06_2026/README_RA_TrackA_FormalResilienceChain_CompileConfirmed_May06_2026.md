# RA Track A — Formal Resilience Chain (Compile-Confirmed, May 06 2026)

**Synthesis-only.** No new Lean code. No new simulator runs. Records the **five-module** compile-confirmed Track A spine as a coherent formal chain so future paper drafts and RAKB sessions can cite it as a unit.

**Refreshed 2026-05-06 (audit_events EV-2026-05-06-017)** to add Layer 5 (Track A.3 comparison-domain validity, `RA-MOTIF-COMPARISON-DOMAIN-VALIDITY-001`). The original four-module synthesis is preserved by this same packet; only the five output documents and this README were updated to reflect the new layer. The earlier `RA_TrackA_CertificationResilience_FormalChain_May06_2026/` (three-module synthesis) remains in the registry as provenance.

## Outputs

```
outputs/RA_TrackA_FormalResilienceChain.md
  Narrative across all five Lean modules:
  Layer 1 — RA_MotifCertificationResilienceConsolidation
  Layer 2 — RA_MotifCertificateCorrelationBridge
  Layer 3 — RA_MotifNativeOverlapCorrelationBridge
  Layer 4 — RA_MotifSupportFamilyRescueTaxonomy
  Layer 5 — RA_MotifComparisonDomainValidity

outputs/RA_TrackA_LeanModuleMap.csv
  One row per module: layer, claim_id, key structures, key
  theorems, build receipt, lex-clean status.

outputs/RA_TrackA_SimulatorLessonMap.csv
  One row per simulator lesson it formalizes: lesson, source
  claim, Track A module, formal counterpart, what's not formalized.

outputs/RA_TrackA_OpenFormalGaps.md
  What remains simulator-only. Numerical decay, calibration,
  metric-repair coefficients, monotonicity-violation counts,
  AUC and rescue rates.

outputs/RA_TrackA_CompileConfirmed_Report.md
  Build receipts: lake build per module with job count and wall
  time; lex-clean confirmation; toolchain pin; environment notes.
```

## Anchor

`RA-MOTIF-TRACKA-FORMAL-RESILIENCE-CHAIN-METHOD-001` (framing) registers this packet as the canonical paper-citation reference for the **five-module** Track A spine. Cross-references the earlier `RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001` (three-module synthesis, preserved as provenance).

## Discipline

This packet does not promote any new positive or negative claim. The orientation-specific rescue exclusion (`RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001`) and the v1.5..v1.8.1 retraction (`RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`) remain in force.
