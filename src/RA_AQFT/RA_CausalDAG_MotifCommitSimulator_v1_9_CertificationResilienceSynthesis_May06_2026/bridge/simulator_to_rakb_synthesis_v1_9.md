# v1.9 simulator → RAKB bridge

This packet is synthesis-only. It does not introduce new claims about Nature; it consolidates the v0.x / v1.x simulator chain so future RAKB sessions can read the controlling result for orientation-overlap rescue in one place.

## RAKB nodes added

- **Framing**: `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` — registers the four synthesis documents as the canonical entry-point for the v1.x simulator chain.

## RAKB nodes touched

- `RA-SIM-CONFOUND-METHOD-001` — extended with rule (f) (fixed-bin discipline).

## RAKB nodes referenced (no edits)

The synthesis cites the v0.5.x .. v1.8.1 chain but does not re-edit those entries. New audits should add `audit_events.csv` rows rather than modifying the cited claims directly.

## Mapping table

| Synthesis output | RAKB anchor |
|---|---|
| `ra_confirmed_resilience_signatures_v1_9.md` | `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` (formal_anchor); cites all simulator-side robust-positive claims by ID |
| `ra_retracted_orientation_specificity_chain_v1_9.md` | `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` (formal_anchor); cites the v1.5..v1.8.1 chain claim IDs |
| `ra_open_native_witness_requirements_v1_9.md` | `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` (formal_anchor); cites `RA-SIM-CONFOUND-METHOD-001`, `RA-SIM-ORIENT-KEYING-METHOD-001` |
| `ra_v1_series_epistemic_status_matrix.csv` | Generated from `claims.yaml` + `audit_events.csv` by `scripts/build_status_matrix.py`; one row per packet |

## Use

When citing the orientation-overlap result in any future packet, paper, or RAKB entry: cite this synthesis (`RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`) and the appropriate output document, not the individual v1.5 / v1.6 / v1.7 / v1.8 / v1.8.1 entries. Those entries are still in the registry as provenance; the synthesis is the controlling reference.
