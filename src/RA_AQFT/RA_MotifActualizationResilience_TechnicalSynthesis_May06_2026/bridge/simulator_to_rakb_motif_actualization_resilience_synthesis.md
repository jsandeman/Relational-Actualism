# Technical synthesis → RAKB bridge

This packet adds **one** new RAKB node:

- `RA-MOTIF-ACTUALIZATION-RESILIENCE-SYNTHESIS-METHOD-001` (framing) — registers the technical note as the canonical RA-internal synthesis anchor for the motif → support-family → certification-family → native-overlap → orientation-overlap arc.

It does not modify any existing claim. It is a "read-this-first" reference for collaborators / paper drafts / future sessions. Future audits or new packets that touch the synthesized arc should add `audit_events.csv` rows referencing this anchor when appropriate.

## Mapping

| Output | RAKB anchor / cite-target |
|---|---|
| `RA_MotifActualizationResilience_TechnicalNote_May06_2026.md` § 1 (Nature-target) | `RA-METHOD-001`, `RA-METHOD-002` |
| § 2 (BDG–LLC) | `RA-ISSUE-LEAN-CHAINSCORE-001` (resolved); `RA_AmpLocality.lean` (axiom; open problem) |
| § 3 (motif ladder) | `RA-SIM-SEVERANCE-SIGNATURE-*`, `RA-SIM-SEVERANCE-CHANNEL-*` |
| § 4 (support-family semantics) | `RA-SIM-SUPPORT-FAMILY-*`, `RA-SIM-SUPPORT-FAMILY-MONO-*`, `RA-SIM-SUPPORT-FAMILY-METRIC-*` |
| § 5 (certification-family) | `RA-SIM-CERT-FAMILY-*`, `RA-SIM-CERT-CORRELATION-*` |
| § 6 (native-overlap signature) | `RA-SIM-NATIVE-CERT-OVERLAP-*`, `-ROBUST-*`, `-CALIB-*`, `-ANCHOR-*`; `RA-SIM-NATIVE-COMPONENT-DECOUPLE-*` |
| § 7 (retraction + confound discipline) | `RA-SIM-V1-5-CORRIGENDUM-METHOD-001`, `RA-SIM-ORIENT-KEYING-METHOD-001`, `RA-SIM-CONFOUND-METHOD-001`, `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` |
| § 8 (open problems) | CLAUDE.md "Key open problems" section |
| § 9 (next formal targets) | proposes Track A (formalization) and Track B (native witness extraction) |

## Discipline

This synthesis does NOT promote any new positive or negative claim. The retracted findings stay retracted; the confirmed findings keep their controlling claim IDs. Cite this synthesis in collaborator handoffs, paper drafts, and the RAKB "new session" prompt; do not pull individual cited claims out of context.
