# RA Native Split Packet v1

This packet provides draft file splits that implement the native-first module boundary identified in the bedrock audit.

Included drafts:

- `RA_D1_Core_draft.lean`
- `RA_D1_Translations_draft.lean`
- `RA_D1_Bridge_draft.lean`
- `RA_D1_Aliases_draft.lean`
- `RA_O14_Uniqueness_Core_draft.lean`
- `RA_O14_Translations_draft.lean`
- `lakefile_native_draft.lean`

These are **draft extraction files only**:
- not compile-tested
- not path-adjusted for the existing repository namespace
- intended to accelerate native-first refactoring

Use them as starting points for a real refactor inside `src/RA_AQFT`.
