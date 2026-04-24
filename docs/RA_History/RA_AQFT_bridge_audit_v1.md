# RA AQFT Bridge Audit v1

## Scope

This pass audits the AQFT / Unruh / Casimir layer across the current core bundle:

- `RA_Paper_I_Kernel_and_Engine.tex`
- `RA_AQFT_Proofs_v10.lean`
- `RA_AQFT_Proofs.lean` (shadow file)
- `RA_CFC_Port.lean`
- `RA_AQFT_CFC_Patch.lean`
- `RA_CFC_Port_Retrospective.md`
- `rindler_relative_entropy.py`
- `casimir_benchmark.py`

## Main findings

### 1. The AQFT bottleneck is narrow, not diffuse

The current canonical Lean AQFT file is `RA_AQFT_Proofs_v10.lean`. Static inspection shows a compact declaration surface:

- `relEnt_unitary_invariant`
- `frame_independence`
- `rindler_stationarity`

The blocking items are also compact:

- one live `sorry`: `Matrix.cfc_conj_unitary`
- two axioms: `vacuum_lorentz_invariant`, `petz_monotonicity`

Crucially, only `vacuum_lorentz_invariant` is load-bearing for `frame_independence` and `rindler_stationarity`; `petz_monotonicity` sits in the CPTP/data-processing branch and is not invoked by the Unruh theorem chain.

### 2. The current repo metadata overstates the CFC closure state

The default `lakefile.lean` comments say the CFC proof chain was ported from Lean-QuantumInfo and that the toolchain mismatch was sidestepped. But the current default root still points to `RA_AQFT_Proofs_v10`, which contains the live `sorry`.

The dedicated retrospective note says the attempted Mathlib-only port failed and was reverted, with `RA_CFC_Port.lean` explicitly marked nonroot and noncompiling on the present Mathlib surface.

So there is a real governance mismatch:

- code comments imply CFC closure is effectively in hand
- the retrospective says the port failed
- the canonical root still contains the single CFC `sorry`

### 3. Paper I should stop calling the CFC gap "trivially closable"

The paper currently says `Matrix.cfc_conj_unitary` is trivially closable by copying the corresponding proof from Lean-QuantumInfo. The retrospective note directly undercuts that wording: the attempted port failed because the Mathlib CFC API drifted, and the next recommended move is a current-API proof, not a mechanical copy.

This is not a conceptual problem for RA. It is still a **narrow library-closure problem**. But "trivially closable" is too strong for the current snapshot.

### 4. The finite-dimensional Unruh theorem is narrower than "full AQFT closure"

What is actually established in the default-root Lean file is:

1. relative entropy is invariant under unitary conjugation (modulo the CFC lemma),
2. the vacuum is invariant under the chosen Lorentz/unitary action (axiom),
3. therefore the Rindler thermal state is stationary under the corresponding finite-dimensional action.

That is a meaningful result. But it is not yet the full local-algebra AQFT theorem.

The support script `rindler_relative_entropy.py` is honest about what remains open:

- `P_act` on local algebras `A(O)`
- commutation of `P_act` with modular flow
- interacting-theory extension
- entangled multi-particle local-algebra treatment

The best paper phrasing is therefore:

- **finite-dimensional conditional theorem is present**
- **full AQFT modular/local-algebra closure remains open**

### 5. The finite truncation hides an important full-QFT subtlety

The support script explicitly notes that in full QFT the Rindler thermal state and Minkowski vacuum are representation-sensitive / unitarily inequivalent, and that relative entropy can diverge modewise. The finite-dimensional truncation therefore should not be read as proving finiteness of the full continuum relative entropy.

The safe invariant claim is the one the paper actually needs:

- **stationarity / no irreversible increase under the relevant flow**

not

- **finiteness of the full continuum relative entropy**

A brief scope sentence in Paper I would prevent confusion here.

### 6. Casimir is a strong bridge benchmark, but still a bridge benchmark

`casimir_benchmark.py` runs cleanly and reproduces the standard pressure at `d = 1 μm`:

- `p_z = -1.3002e-03 Pa`

The RA-specific step in the script is the subtraction prescription

- `<T^μν_RA> = <T^μν_ren>[g,Φ] - <T^μν_ren>[g,|0⟩]`

which preserves the configuration-dependent Casimir term while suppressing the absolute vacuum reference.

That is a strong **compatibility / preservation** benchmark. It is not yet a discrete first-principles derivation of Casimir from BDG graph dynamics, and it does not close the full backreaction or local-algebra AQFT programme.

## Recommended source-of-truth wording

### For Paper I

Use three explicit layers:

1. **Finite-dimensional conditional Lean theorem**
   - `rindler_stationarity`, conditional on one CFC lemma and vacuum invariance axiom

2. **Current narrow closure target**
   - replace `Matrix.cfc_conj_unitary` with a current-Mathlib proof or an integrated dependency-backed proof

3. **Open AQFT layer**
   - define `P_act` on local algebras and prove modular-flow commutativity / full AQFT closure

### For the benchmark programme

Label:

- Casimir = **strong bridge benchmark**
- Unruh/Rindler stationarity = **conditional finite-dimensional bridge theorem**
- full modular/local-algebra AQFT = **open formal target**

## Best next move

The highest-value immediate move is **not** to widen the AQFT scope further.

It is to do these in order:

1. patch Paper I wording,
2. clean the repo metadata so the lakefile comments match the actual root state,
3. either close the single CFC lemma with current Mathlib or keep it explicitly open,
4. only then promote the local-algebra AQFT programme as the next frontier.

That will make the suite's AQFT layer both stronger and more credible.
