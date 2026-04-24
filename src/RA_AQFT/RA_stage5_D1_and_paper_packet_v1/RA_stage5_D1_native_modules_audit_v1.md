# Stage 5 D1 native modules audit

This packet promotes the D1 rewrite from blueprint-only status to concrete source-level modules.

## What is included

- `RA_D1_NativeKernel_v1.lean`
- `RA_D1_NativeConfinement_v1.lean`
- `RA_D1_NativeClosure_v1.lean`
- `RA_D1_NativeLedgerOrientation_v1.lean`

## Design rule

Each module is written from scratch against the restored baseline, but only keeps theorem families that can be stated in terms of:

- BDG depth counts
- filter positivity / negativity
- extension census
- finite closure length
- depth-2 ledger preservation
- DAG orientation asymmetry

Everything from the historical Section 15 (coherent states / isospin / GMN / hypercharge) and Section 16 (`P_act` / field-equation bridge) remains retired from the active native path.

## Dependency order

1. `RA_D1_NativeKernel_v1`
2. `RA_D1_NativeConfinement_v1`
3. `RA_D1_NativeClosure_v1`
4. `RA_D1_NativeLedgerOrientation_v1`

This matches the dependency-first roadmap already established for the restored baseline.

## Status honesty

These files are **source-level drafts** produced from the audited historical theorem chain. They have not been compile-tested in this environment.

The correct next local workflow is:

```bash
lake lean RA_D1_NativeKernel_v1.lean
lake lean RA_D1_NativeConfinement_v1.lean
lake lean RA_D1_NativeClosure_v1.lean
lake lean RA_D1_NativeLedgerOrientation_v1.lean
```

Only after they compile should their theorem families move onto the active native support surface.

## Immediate paper consequence

Until these four files compile, Papers II–IV should treat all D1-derived matter claims as:

- historical baseline support,
- native rewrite in progress, or
- deferred archive material,

rather than active native Lean support.
