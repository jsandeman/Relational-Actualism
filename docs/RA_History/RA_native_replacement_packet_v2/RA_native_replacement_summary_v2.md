# RA Native Replacement Packet v2 Summary

This packet carries the native-first reset forward in three ways.

1. It makes the active Lean root explicit with native wrapper modules:
   - `RA_GraphCore_Native`
   - `RA_AmpLocality_Native`
   - `RA_BDG_Coefficient_Arithmetic`

2. It extends the paper rewrite programme to the remaining hybrid-heavy papers:
   - `RA_Paper_III_native_rewrite_patch_v1.md`
   - `RA_Paper_IV_native_rewrite_patch_v1.md`

3. It turns remaining hybrid or non-native targets into direct Nature-facing research tasks:
   - `RA_native_research_replacement_docket_v1.md`
   - `RA_native_section_replacement_registry_v1.csv`

Status:
- all Lean files in this packet are source-level draft wrappers
- none of these new modules were compile-tested here
- the paper patches are editorial / structural patch notes, not in-place TeX edits
