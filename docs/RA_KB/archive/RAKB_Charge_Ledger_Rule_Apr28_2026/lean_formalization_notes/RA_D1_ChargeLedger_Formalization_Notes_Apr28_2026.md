# RA_D1_ChargeLedger Formalization Notes

This is not an active Lean source file. It is a formalization plan for a future file:

```text
src/RA_AQFT/RA_D1_ChargeLedger_v1.lean
```

## Minimal conditional theorem

The first theorem should not attempt to solve the full sign-source problem. It should prove the seven-value range conditional on a signed local N1 frame.

```lean
/- PSEUDO-LEAN / DESIGN SKETCH -/

import Mathlib.Data.Int.Basic
import Mathlib.Data.Finset.Basic

namespace RA_ChargeLedger

structure SignedN1Frame (α : Type*) [DecidableEq α] where
  parents : Finset α
  sign : α -> Int
  h_card : parents.card ≤ 3
  h_sign : ∀ p ∈ parents, sign p = -1 ∨ sign p = 0 ∨ sign p = 1

def qN1 {α : Type*} [DecidableEq α] (F : SignedN1Frame α) : Int :=
  F.parents.sum F.sign

/-- Conditional seven-value theorem: at most three signed N1 directions give Q_N1 in [-3,3]. -/
theorem qN1_range {α : Type*} [DecidableEq α] (F : SignedN1Frame α) :
    -3 ≤ qN1 F ∧ qN1 F ≤ 3 := by
  -- finite induction over parent cardinality ≤ 3
  -- each term in {-1,0,+1}
  sorry

/-- Later strengthening: membership in the explicit seven-value set. -/
theorem qN1_seven_values {α : Type*} [DecidableEq α] (F : SignedN1Frame α) :
    qN1 F = -3 ∨ qN1 F = -2 ∨ qN1 F = -1 ∨ qN1 F = 0 ∨
    qN1 F = 1 ∨ qN1 F = 2 ∨ qN1 F = 3 := by
  -- follows from qN1_range and integrality
  sorry

end RA_ChargeLedger
```

This gives an immediate formal target while keeping the hard problem honest.

## Hard theorem target

The hard theorem is to construct `SignedN1Frame` from finite DAG topology.

Possible route:

```lean
structure OrientedLocalCut ... where
  vertices : Finset V
  orientation : ...
  rank_le_three : ...

structure IncidenceSigns ... where
  signN1 : Edge V -> Int
  sign_range : ...
  induced_by_boundary : ...

theorem oriented_cut_induces_signed_n1_frame ... :
  SignedN1Frame Parent
```

This should probably use a finite incidence/chain-complex representation rather than particle labels.

## Conceptual target

The topological rule should implement:

```text
N2 winding / branching cells
  --boundary/incidence-->
N1 signed edge ledger
  --vertex divergence-->
LLC
```

This would turn the N1/N2 ambiguity into a theorem: the electric N1 signature is the boundary/readout of N2 spatial winding.
