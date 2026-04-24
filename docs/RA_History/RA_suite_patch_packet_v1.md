# RA Suite Patch Packet v1

These patch copies implement the next audit-pass repairs in concrete TeX edits.

Decision defaults used in this pass:
- Insert the suite framing-discipline paragraph in Paper I and short echoes in Papers II–IV.
- Treat agreement with QFT/GR/SM inside their domains as a downstream benchmark, not the primitive mechanism.
- For Paper IV DFT/F1, adopt the safest immediate repair: downgrade to an open computational target rather than cite RACI as primary support.
- Retain legacy bibliography entries only as archival provenance via a historical note.
- Because Papers I and IV currently disagree on the KCB normalization, downgrade the closed-form KCB formula to a structural-ceiling claim until the normalization is re-derived.

## Files

### Paper I
- Patched TeX: `RA_Paper_I_Kernel_and_Engine_audit_patch_v1.tex`
- Unified diff: `RA_Paper_I_Kernel_and_Engine_audit_patch_v1.diff`
  - Inserted suite framing-discipline paragraph in Introduction.
  - Downgraded KCB formula claim to a structural-ceiling claim pending normalization audit.

### Paper II
- Patched TeX: `RA_Paper_II_Matter_Forces_and_Motifs_audit_patch_v1.tex`
- Unified diff: `RA_Paper_II_Matter_Forces_and_Motifs_audit_patch_v1.diff`
  - Inserted short framing echo in Introduction.
  - Restructured topology table so BDG content is primary and SM language is translation.
  - Reframed mass cascade as BDG-derived quantity plus empirical identification.
  - Retitled force-range section to make BDG primacy explicit.
  - Inserted force-range framing sentence clarifying translation status of SM labels.
  - Lightly softened gauge-group opening so BDG algebra is primary.
  - Reframed charge-quantization follow-through as translation rather than primary target.

### Paper III
- Patched TeX: `RA_Paper_III_Gravity_Cosmology_Complexity_audit_patch_v1.tex`
- Unified diff: `RA_Paper_III_Gravity_Cosmology_Complexity_audit_patch_v1.diff`
  - Renamed legacy “RACL chain” to “GR derivation chain” in abstract.
  - Softened Paper III introduction so GR is a downstream benchmark, not the primitive target.
  - Inserted short framing echo in Paper III Introduction.
  - Renamed legacy “RACL chain” in derivation section.
  - Softened MOND-language claim.
  - Softened conclusion language to emphasize phenomena over legacy-theory recovery.

### Paper IV
- Patched TeX: `RA_Paper_IV_Complexity_Life_Causal_Firewall_audit_patch_v1.tex`
- Unified diff: `RA_Paper_IV_Complexity_Life_Causal_Firewall_audit_patch_v1.diff`
  - Softened Paper IV introduction so legacy vocabularies are downstream organizers, not primary targets.
  - Inserted short framing echo in Paper IV Introduction.
  - Downgraded DFT/F1 material from legacy-dependent CV to open computational target.
  - Reframed sandwich-bound DFT sentence as open target and removed RACI dependence.
  - Inverted primacy in §7 scope note and exposed KCB normalization issue explicitly.
  - Rewrote KCB subsection to retain structural claim while removing unstable closed-form formula.
  - Updated status-table row for DFT/F1 to open computational target.
  - Updated status-table row for KCB to reflect normalization audit.
  - Inserted historical-note paragraph before bibliography.

## Remaining unresolved items

- KCB exact normalization remains unresolved; the patch makes the suite internally honest, not yet final on that formula.
- Paper II still contains many Standard-Model labels in later sections. The highest-risk primacy inversions are patched here; a full second editorial pass could further soften the remainder.
- Paper III still depends on the AQFT bridge assumptions already identified in the theorem inventory. The patch does not change that formal status.
