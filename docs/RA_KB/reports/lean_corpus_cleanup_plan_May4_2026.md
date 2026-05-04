# Lean corpus cleanup plan — May 4, 2026

## Scope of the cleanup

User request: remove version numbers / version-metadata descriptors from
filenames; move metadata into file comments; fix stale imports; zip
deprecated/superseded files for archive; integrate the new
`RA_MotifCommitProtocol_v2` work and its `RA_O01_KernelLocality_v2`
dependency.

## Naming-convention judgment call

The user said "no version numbers or other descriptors". Two readings:

- **Narrow reading (what I'm doing):** strip `_v1`, `_v2`, `_draft`,
  `_v10` — these are version-metadata.
- **Broad reading (NOT doing without confirmation):** also strip `_Core`,
  `_Native`. These designate semantic role, not version. Removing them
  creates name collisions (`RA_GraphCore` vs `RA_GraphCore_Native`,
  `RA_AmpLocality` vs `RA_AmpLocality_Native`). If you want these
  cleaned too, we'd need to merge or rename the underlying files.

I'm proceeding with the narrow reading. Adjust if needed.

## File disposition

### Group 1 — RENAME (drop version suffix; preserves git history via `git mv`)

| current | new |
|---|---|
| `RA_O14_ArithmeticCore_v1.lean` | `RA_O14_ArithmeticCore.lean` |
| `RA_D1_Core_draft.lean` | `RA_D1_Core.lean` |
| `RA_D1_NativeKernel_v1.lean` | `RA_D1_NativeKernel.lean` |
| `RA_D1_NativeConfinement_v1.lean` | `RA_D1_NativeConfinement.lean` |
| `RA_D1_NativeClosure_v1.lean` | `RA_D1_NativeClosure.lean` |
| `RA_D1_NativeLedgerOrientation_v1.lean` | `RA_D1_NativeLedgerOrientation.lean` |
| `RA_D1_NativeDimensionality_v1.lean` | `RA_D1_NativeDimensionality.lean` |
| `RA_ActualizationSelector_v1.lean` | `RA_ActualizationSelector.lean` |
| `RA_FrontierIncidence_v1.lean` | `RA_FrontierIncidence.lean` |
| `RA_FrontierGraphBridge_v1.lean` | `RA_FrontierGraphBridge.lean` |
| `RA_HasseFrontier_v1.lean` | `RA_HasseFrontier.lean` |
| `RA_HasseFrontier_Maximal_v1.lean` | `RA_HasseFrontier_Maximal.lean` |
| `RA_HasseFrontier_FiniteMax_v1.lean` | `RA_HasseFrontier_FiniteMax.lean` |
| `RA_HasseFrontier_FiniteMaxExist_v1.lean` | `RA_HasseFrontier_FiniteMaxExist.lean` |
| `RA_IncidenceCharge_v1.lean` | `RA_IncidenceCharge.lean` |
| `RA_IncidenceSignSource_v1.lean` | `RA_IncidenceSignSource.lean` |
| `RA_GraphOrientationChart_v1.lean` | `RA_GraphOrientationChart.lean` |
| `RA_GraphOrientationClosure_v1.lean` | `RA_GraphOrientationClosure.lean` |
| `RA_O01_KernelLocality_v2.lean` | `RA_O01_KernelLocality.lean` |
| `RA_MotifCommitProtocol_v2.lean` | `RA_MotifCommitProtocol.lean` |

### Group 2 — REPLACE in place (corrected import)

| action | detail |
|---|---|
| Replace `RA_BDG_Coefficient_Arithmetic.lean` content with `RA_BDG_Coefficient_Arithmetic_v2.lean`'s content. | The v2 file has the corrected import (`RA_O14_ArithmeticCore_v1` instead of stale `RA_O14_Uniqueness_Core_draft`). Then archive the v2 standalone file (no longer needed). |

### Group 3 — ADD to active roots in `lakefile.lean`

- `RA_MotifCommitProtocol` (Tier B — native content; consensus/motif-commit semantics)
- `RA_O01_KernelLocality` (Tier A — bedrock; kernel locality lemma; new dependency)

### Group 4 — ARCHIVE (zip + remove from src/RA_AQFT/)

Per `lakefile.lean` retirement docstring + analysis:

| file | rationale |
|---|---|
| `RA_AQFT_Proofs.lean` | v10.1; superseded approach; not in roots |
| `RA_AQFT_Proofs_v2.lean` | v3.4 SM-flavored; retired by lakefile docstring |
| `RA_AQFT_Proofs_v10.lean` | retired (IC46 framing violation) per lakefile docstring |
| `RA_AQFT_CFC_Patch.lean` | patch for retired `RA_AQFT_Proofs_v10` |
| `RA_CFC_Port.lean` | retired (broken against current Mathlib) per lakefile docstring |
| `RA_BaryonChirality.lean` | retired (renamed to `RA_CausalOrientation_Core`) per lakefile docstring |
| `RA_AmpLocality_v2.lean` | duplicate of active `RA_AmpLocality.lean` |
| `RA_GraphCore_v2.lean` | "v2 sorry closure attempt" per its header; superseded |
| `RA_O14_Uniqueness.lean` | original 238-line file; superseded by `RA_O14_ArithmeticCore` |
| `RA_O14_Uniqueness_Core_draft.lean` | intermediate 175-line draft; superseded by `RA_O14_ArithmeticCore` |
| `RA_BDG_Coefficient_Arithmetic_v2.lean` | content moved into renamed canonical file |
| `RA_D1_Proofs.lean` | older D1 proofs; D1_Core + D1_Native* family supersedes |
| `RA_Alpha_EM_Proof.lean` | exploratory; not in roots, not imported |
| `RA_PACT_conservation_lean.lean` | exploratory; not in roots, not imported |
| `RA_Proofs_Lean4.lean` | exploratory; not in roots, not imported |
| `lakefile_v1.lean` | prior lakefile config; superseded |

Zip will be at: `archive_lean_deprecated_May4_2026.zip` in the repo root.

## Import-fix pass

After rename, every `import RA_..._v1` / `_v2` / `_draft` reference
needs to be updated to the new clean name. Affected files (per grep):
about 24 files have at least one such import.

## Build verification

After all renames + import fixes + lakefile update, run:
```
cd src/RA_AQFT && lake build
```
Expect ≥ 8000 jobs to succeed with 0 errors.

## RAKB updates

- `artifacts.csv`: update `repo_relative_path` for ~24 renamed Lean files; add 2 new artifacts for `RA_MotifCommitProtocol` and `RA_O01_KernelLocality`.
- `targets.yaml` and `issues.yaml`: update sources lists where they reference renamed files.
- Add new claim nodes per the user's RAKB mapping:
  - `RA-MOTIF-COMMIT-001` (formal_anchor: `supportCutOfFiniteHasseFrontier`)
  - `RA-MOTIF-COMMIT-002` (formal_anchor: `DAGReadyAt_iff_support_subset_realized_past`)
  - `RA-MOTIF-COMMIT-003` (formal_anchor: `DAGReadyAt.future_mono` / `GraphReadyAt.future_mono`)
  - `RA-MOTIF-COMMIT-004` (formal_anchor: `DAGCommitsAt.excludes_incompatible_same_site` / `GraphCommitsAt.excludes_incompatible_same_site`)
  - Plus the bridge theorem `GraphReadyAt_supportCutOfFiniteHasseFrontier_iff` as part of `RA-MOTIF-COMMIT-001`.

## Execution order

1. Pre-flight backup snapshot of `src/RA_AQFT/`
2. Replace `RA_BDG_Coefficient_Arithmetic.lean` with v2 content
3. Mass rename via `git mv` (Group 1 + Group 3 entry files)
4. Update all in-corpus `import` statements
5. Update `lakefile.lean` (rename refs + add new roots + update docstring)
6. Test build with `lake build`
7. Zip + remove deprecated files (Group 4)
8. Test build again to confirm no orphan imports broke
9. Update RAKB (paths + new claims + new artifacts)
10. Commit
