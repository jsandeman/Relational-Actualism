# Track A formal-chain → RAKB bridge

This packet adds **one** new RAKB framing entry:

- `RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001` (framing) — registers the four synthesis documents as the canonical entry-point for the Track A formal chain.

It does not modify any existing claim. Track A's three Lean modules (`RA-MOTIF-CERT-RESILIENCE-CONSOL-001`, `RA-MOTIF-CERT-CORRELATION-BRIDGE-001`, `RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001`) keep their existing entries; this synthesis is a "read-this-first" reference for paper-writing and RAKB session bootstraps.

## Mapping

| Output | RAKB anchor / cite-target |
|---|---|
| `RA_TrackA_CertificationResilience_FormalChain.md` | `RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001` (formal_anchor); narrative across all three Track A claim IDs. |
| `RA_TrackA_FormalChain_Map.csv` | Per-anchor table; rows tagged with controlling claim IDs. |
| `RA_TrackA_SimulatorToLean_Correspondence.md` | Cite-table for paper drafting; pairs simulator claim IDs with Lean qualitative-support modules or "simulator-only" markers. |
| `RA_TrackA_OpenFormalGaps.md` | What is NOT in Lean; cite when discussing the boundaries of the Track A formalization. |

## Use

When citing the Track A formal chain in any paper section, RAKB-facing note, or new packet: cite this framing entry and the appropriate output document. When citing a single Lean theorem, also cite its specific Track A claim ID (`RA-MOTIF-CERT-RESILIENCE-CONSOL-001` / `RA-MOTIF-CERT-CORRELATION-BRIDGE-001` / `RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001`).

## Discipline

This packet is synthesis-only. It does not promote any new positive or negative claim. The orientation-specific rescue exclusion (`RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001`) and the v1.5..v1.8.1 retraction (`RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`) remain in force.
