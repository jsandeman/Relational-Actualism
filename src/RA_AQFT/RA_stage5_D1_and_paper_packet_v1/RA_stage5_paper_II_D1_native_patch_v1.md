# Stage 5 Paper II D1-native patch note

Paper II is the paper most directly affected by the D1 rewrite.

## What changes immediately

The restored historical file `RA_D1_Proofs.lean` can no longer be cited wholesale as active native support. Its theorem families now split into:

- native rewrite candidates (Sections 0–14), and
- retired archive / bridge material (Sections 15–16).

The new native replacements are:

- `RA_D1_NativeKernel_v1.lean`
- `RA_D1_NativeConfinement_v1.lean`
- `RA_D1_NativeClosure_v1.lean`
- `RA_D1_NativeLedgerOrientation_v1.lean`

but they are still source-level drafts until compile-validated.

## Exact paper consequences

### 1. Confinement proposition

Current support claim:

> Verified in `RA_D1_Proofs.lean` (`confinement_lengths`).

Replacement:

> The historical Lean baseline contains a finite-closure theorem family for the two minimal branching motif classes. A native rewrite of this family is underway in `RA_D1_NativeConfinement_v1.lean`; until that rewrite is compile-validated, the confinement-length statements should be treated as restored-baseline support rather than active native Lean support.

### 2. Closure theorem / topology exhaustion

Current support claim:

> `RA_D1_Proofs.lean` (`universe_closure`), zero errors and zero `sorry` tags.

Replacement:

> The historical baseline contains a complete finite extension census and closure theorem for the D1 motif universe. Under the current native-first programme, this result is being rewritten in native motif language (`RA_D1_NativeClosure_v1.lean`) before it re-enters the active support surface.

### 3. Baryon number / chirality language

These labels should leave the active theorem surface.

Replace with:

- depth-2 ledger preservation
- orientation asymmetry from DAG irreversibility
- unique symmetric stable endpoint

### 4. Section 15 / 16 derived claims

Anything depending on:

- coherent states,
- isospin,
- GMN,
- hypercharge,
- `P_act` field-equation bridge,

should be removed from the active Lean-supported chain and labeled either historical overlay or deferred bridge material.

## Recommended status language for Paper II

Use three buckets:

- **Active native Lean support** — currently only `RA_GraphCore`, `RA_O01_KernelLocality_v2`, `RA_O14_ArithmeticCore_v1`
- **Restored historical baseline / native rewrite in progress** — D1 theorem family
- **Deferred archive / bridge** — coherent-state, isospin, GMN, `P_act` bridge material
