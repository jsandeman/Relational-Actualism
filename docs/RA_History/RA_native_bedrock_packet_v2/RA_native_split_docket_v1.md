# RA Native Split Docket v1

## `RA_D1_Proofs.lean`

Suggested split boundary:
- `RA_D1_Core.lean`: lines 1–930 (Sections 0–14)
- `RA_D1_Translations.lean`: lines 931–1051 (Section 15)
- `RA_D1_Bridge.lean`: lines 1052–1164 (Section 16)
- `RA_D1_Aliases.lean`: lines 1165–end (Section 17)

## `RA_O14_Uniqueness.lean`

Suggested split boundary:
- `RA_O14_Uniqueness_Core.lean`: lines 1–165 and 194–end summary rewrite
- `RA_O14_Translations.lean`: lines 166–179

## `RA_GraphCore.lean`

No mandatory split, but:
- remove or quarantine `horizon_partition`
- consider renaming `MarkovBlanket` within the file before Paper IV relies on it more heavily

## `RA_AmpLocality.lean`

No split needed.
Only terminology cleanup is recommended.
