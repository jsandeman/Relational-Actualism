# Stage 5 paper patch note (Papers I, III, IV)

This patch note updates the support surface after two facts:

1. `RA_O01_KernelLocality_v2.lean` compiles standalone.
2. `RA_O14_ArithmeticCore_v1.lean` compiles standalone.
3. The D1 replacement family now exists as source-level native rewrite modules, but has not yet been compile-validated.

## Paper I

### Replace the active Lean block with this exact support block

```tex
Local ledger / graph-cut chain & \texttt{RA\_GraphCore.lean} & Proved \\
Kernel locality / admissibility depends on realized past & \texttt{RA\_O01\_KernelLocality\_v2.lean} & Proved standalone \\
d=4 arithmetic coefficient inversion & \texttt{RA\_O14\_ArithmeticCore\_v1.lean} & Proved standalone \\
```

### Move out of the active native support block

- causal invariance
- Markov blanket shielding
- `alpha_inv_137`
- Koide
- confinement depths
- universe closure / five-type closure
- AQFT / Unruh / Rindler material

### Replace the status-summary sentence

Use:

> The presently active native Lean support surface consists of the graph-cut / local-ledger chain in `RA_GraphCore.lean`, the kernel-locality replacement family in `RA_O01_KernelLocality_v2.lean`, and the arithmetic coefficient-inversion layer in `RA_O14_ArithmeticCore_v1.lean`. Other historical Lean files remain part of the restored baseline, but are not currently counted as active native support until their theorem families are rewritten and revalidated in RA-native terms.

## Paper III

### Replace the active support sentence in the introduction / RACL summary

Use:

> The active native support presently established in Lean consists of the local-ledger / graph-cut layer (`RA_GraphCore.lean`), the kernel-locality replacement family (`RA_O01_KernelLocality_v2.lean`), and the d=4 arithmetic coefficient-inversion layer (`RA_O14_ArithmeticCore_v1.lean`). Continuum field-equation, Lorentz-frame, and cosmological translation claims are not currently part of the active native Lean support surface.

### Lorentz / causal-invariance section

Replace any positive support claim with:

> Earlier versions of the suite linked Lorentz-frame independence to a causal-invariance theorem at the amplitude / quantum-measure layer. Under the current native-first programme, that chain is treated as deferred bridge material rather than active native support. The active O01 support now concerns kernel locality and admissibility dependence on realized past.

### Remove these as active support

- `causal_invariance`
- Lorentz–causal equivalence
- `alpha_s(\mu)`-dependent formulas in the active derivation chain

## Paper IV

### Markov blanket / shielding language

Replace the current strong theorem language with:

> The restored Lean baseline provides verified graph-cut and boundary-interface structure in `RA_GraphCore.lean`. A shielding theorem strong enough to justify the present decoherence rhetoric is not yet part of the active native support surface. Boundary shielding is therefore treated here as a structural research target, not as a closed Lean theorem.

### F1 / F2 language

Replace bridge-heavy labels with native placeholders:

- F1: redundant boundary inscription
- F2: bounded boundary turnover / controllable overwrite rate

### Status table edits

Replace rows implying closed theorem support for:

- hierarchical decoherence,
- KCB,
- Landauer,
- Maxwell-demon dissolution,

with deferred or native-candidate language.

## Bottom line

After Stage 5, Papers I, III, and IV can rely positively only on:

- `RA_GraphCore.lean`
- `RA_O01_KernelLocality_v2.lean`
- `RA_O14_ArithmeticCore_v1.lean`

The new D1 modules are promising source-level replacements, but they should not be cited as active native support until they compile.
