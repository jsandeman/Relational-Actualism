# RA native strict scaffold build note v1

Use this packet if you want to preserve the strict policy that the active native
root must not depend on hybrid legacy modules.

## What went wrong

The build errors are not asking for a new Lean toolchain.
They are not primarily asking for a new Lake manifest.

They show two concrete source problems:

1. The strict-native wrapper files import split native modules that were never
   copied into the active project directory:
   - `RA_D1_Core_draft.lean`
   - `RA_O14_Uniqueness_Core_draft.lean`

2. `RA_AmpLocality_Native.lean` needs explicit type parameters in its alias
   layer so Lean can resolve the wrapper names.

## Strict fix

Keep the existing project package name and dependencies.
Do not rename the package yet.
Do not change the toolchain.

Instead, copy these files into `src/RA_AQFT/`:

- `RA_D1_Core_draft.lean`
- `RA_O14_Uniqueness_Core_draft.lean`
- `RA_AmpLocality_Native.lean` (patched explicit-alias version)
- `RA_BDG_Coefficient_Arithmetic.lean`
- `RA_MotifDynamics_Core.lean`
- `RA_CausalOrientation_Core.lean`
- `lakefile.lean` (scaffold version with original package name)

## Why keep the original package name?

Because package renaming adds no value at the scaffold stage and can force a
manifest refresh. The active problem here is internal imports, not dependency
resolution.

## Suggested build sequence

```bash
cd src/RA_AQFT
rm -rf .lake/build

lake build RA_GraphCore_Native
lake build RA_AmpLocality_Native
lake build RA_BDG_Coefficient_Arithmetic
lake build RA_MotifDynamics_Core
lake build RA_CausalOrientation_Core
```

Only if you insist on keeping a renamed package declaration should you run
`lake update` afterward to refresh `lake-manifest.json`.
