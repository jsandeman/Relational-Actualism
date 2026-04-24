# Stage 5 rewrite status

## Confirmed compiled native modules

- `RA_O01_KernelLocality_v2.lean`
- `RA_O14_ArithmeticCore_v1.lean`

These are now strong enough to support immediate paper-surface corrections.

## New native rewrite modules produced in this pass

- `RA_D1_NativeKernel_v1.lean`
- `RA_D1_NativeConfinement_v1.lean`
- `RA_D1_NativeClosure_v1.lean`
- `RA_D1_NativeLedgerOrientation_v1.lean`

## Local compile sequence for next pass

```bash
lake lean RA_D1_NativeKernel_v1.lean
lake lean RA_D1_NativeConfinement_v1.lean
lake lean RA_D1_NativeClosure_v1.lean
lake lean RA_D1_NativeLedgerOrientation_v1.lean
```

## What should happen after successful compilation

If all four compile cleanly, the active native support surface expands to include the D1 kernel, finite-closure, closure census, and ledger/orientation families.

At that point the next paper pass should:

1. patch Paper II support references from `RA_D1_Proofs.lean` to the new D1 modules,
2. rewrite Paper II's theorem-language in motif / closure / ledger / orientation vocabulary,
3. demote any remaining Section-15/16 material to archive or bridge status,
4. revisit Paper IV only for those claims that depend on D1-derived structure.
