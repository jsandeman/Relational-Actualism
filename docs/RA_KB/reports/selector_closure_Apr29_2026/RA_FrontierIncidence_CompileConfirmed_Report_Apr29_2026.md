# RA Frontier/Incidence Compile Confirmation — Apr 29, 2026

## Summary

`RA_FrontierIncidence_v1.lean` now compiles locally after adding `RA_ActualizationSelector_v1.lean` to the Lake roots/import surface and invoking Lean through Lake.

Confirmed user-local command shape:

```bash
cd src/RA_AQFT
lake lean RA_FrontierIncidence_v1.lean
```

Important workflow correction: because `RA_FrontierIncidence_v1.lean` imports `RA_ActualizationSelector_v1`, the selector scaffold should be available through Lake's module-resolution path. In practice, that means either adding `RA_ActualizationSelector_v1` to the `roots` array or otherwise ensuring it is in the package module search surface.

## Recommended stable Lake root policy

For reproducible future checks, add both files to the active roots, preferably under a clearly labeled exploratory theorem-programme block:

```lean
-- Selector-closure theorem programme — exploratory but compile-checked
`RA_ActualizationSelector_v1,
`RA_FrontierIncidence_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake build
```

This promotes the status from one-file `lake lean` confirmation to full active-root build confirmation.

## Status update

Recommended artifact statuses:

```text
RA_ActualizationSelector_v1.lean:
  lean_env_compile_confirmed_no_sorry_no_admit_no_axiom_import_root

RA_FrontierIncidence_v1.lean:
  lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

No conceptual RAKB change is made here. This packet only hardens the formal evidence status of the selector/frontier scaffolds.

## Lean file hashes in this packet

```text
RA_ActualizationSelector_v1.lean  d7cd655f7a305f3adcecbe5164ede6f4598987d982118a9633091bb32b68ff2d
RA_FrontierIncidence_v1.lean      ba162c2d141a95729140dea3cdcfb586e142d2366cbdc4df6213715fdc48b9a7
```

## Next formal target

The next mathematical step remains connecting the abstract `CandidatePast` / `Frontier` / `BoundaryLedger` definitions to the concrete RA graph and LLC files, then proving closure/frontier invariance of the BDG and ledger data.
