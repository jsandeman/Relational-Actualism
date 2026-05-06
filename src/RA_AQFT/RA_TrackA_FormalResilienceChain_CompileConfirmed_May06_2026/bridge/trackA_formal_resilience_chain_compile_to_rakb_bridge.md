# Track A formal resilience chain (compile-confirmed) → RAKB bridge

This packet adds **one** new RAKB framing entry:

- `RA-MOTIF-TRACKA-FORMAL-RESILIENCE-CHAIN-METHOD-001` (framing) — registers the four-module Track A spine as a coherent compile-confirmed formal chain. Cross-references the earlier three-module synthesis `RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001`, which is preserved as provenance.

It does not modify any existing claim. The four Track A modules keep their existing claim IDs:

- `RA-MOTIF-CERT-RESILIENCE-CONSOL-001` (Layer 1)
- `RA-MOTIF-CERT-CORRELATION-BRIDGE-001` (Layer 2)
- `RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001` (Layer 3)
- `RA-MOTIF-SUPPORT-FAMILY-RESCUE-TAXONOMY-001` (Layer 4)

## Mapping

| Output | RAKB anchor / cite-target |
|---|---|
| `RA_TrackA_FormalResilienceChain.md` | `RA-MOTIF-TRACKA-FORMAL-RESILIENCE-CHAIN-METHOD-001` (formal_anchor); narrative across all four module claim IDs. |
| `RA_TrackA_LeanModuleMap.csv` | One row per module with claim_id, key structures, key theorems, build receipt. |
| `RA_TrackA_SimulatorLessonMap.csv` | One row per simulator lesson, paired with its Track A formal counterpart (or "simulator-only" / "excluded by discipline"). |
| `RA_TrackA_OpenFormalGaps.md` | What is NOT in Lean after Track A.2: numerical decay, calibration, metric-repair coefficients, monotonicity-violation counts, AUC/rescue rates, endpoint-equivalence partial result. |
| `RA_TrackA_CompileConfirmed_Report.md` | Build receipts + environment + reproduction instructions; cites audit events `EV-2026-05-06-010` through `-014`. |

## Use

When citing the Track A formal chain in any paper section, RAKB-facing note, or new packet: cite this framing entry and the appropriate output document. When citing a single Lean theorem, also cite its specific Track A claim ID (Layer 1 / Layer 2 / Layer 3 / Layer 4 above).

The earlier three-module synthesis (`RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001`) remains in the registry and is correct for what it covered; for Track A.2 onwards, prefer this four-module synthesis.

## Discipline

This packet is synthesis-only. No new positive or negative claims. The orientation-specific rescue exclusion (`RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001`) and the v1.5..v1.8.1 retraction (`RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`) remain in force.
