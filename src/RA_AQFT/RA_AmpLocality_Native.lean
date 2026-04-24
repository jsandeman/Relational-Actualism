import RA_AmpLocality

/-!
# RA_AmpLocality_Native

Native wrapper for the active extension-order theorems.

This hotfix keeps the existing mathematical content of `RA_AmpLocality`
but makes all wrapper aliases fully explicit, so Lean does not get stuck on
implicit typeclass inference for the renamed symbols.
-/

open BigOperators Complex

variable {V : Type*} [Fintype V] [DecidableEq V]

abbrev GrowthDAG (V : Type*) [Fintype V] [DecidableEq V] := CausalDAG V

abbrev realized_past {V : Type*} [Fintype V] [DecidableEq V]
    (G : GrowthDAG V) (v : V) : Finset V :=
  causal_past G v

abbrev local_interval {V : Type*} [Fintype V] [DecidableEq V]
    (G : GrowthDAG V) (u v : V) (C : Finset V) : Finset V :=
  causal_interval G u v C

theorem interval_lies_in_realized_past
    (G : GrowthDAG V) (u v : V) (C : Finset V)
    (hu : u ∈ realized_past G v) :
    local_interval G u v C ⊆ realized_past G v :=
  interval_subset_past G u v C hu

theorem interval_context_reduces_to_past
    (G : GrowthDAG V) (u v : V) (C : Finset V)
    (hu : u ∈ realized_past G v) :
    local_interval G u v C = local_interval G u v (C ∩ realized_past G v) :=
  interval_eq_interval_past G u v C hu

theorem bdg_increment_past_determined
    (G : GrowthDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) :
    bdg_increment G cs v C = bdg_increment G cs v (C ∩ realized_past G v) :=
  bdg_increment_depends_on_past_only G cs v C

/-- Active native name for locality of the local weight. -/
def local_weight_past_determined (G : GrowthDAG V) (a : V → Finset V → ℂ) : Prop :=
  amplitude_local G a

/-- Active native name for the BDG local weight. -/
noncomputable def bdg_local_weight (G : GrowthDAG V) (cs : Fin 5 → ℤ)
    (v : V) (C : Finset V) : ℂ :=
  bdg_amplitude G cs v C

theorem bdg_local_weight_past_determined
    (G : GrowthDAG V) (cs : Fin 5 → ℤ) :
    local_weight_past_determined G (bdg_local_weight G cs) := by
  simpa [local_weight_past_determined, bdg_local_weight] using
    (bdg_amplitude_locality G cs)

/-- Active native name for the permutation-independent observable weight. -/
noncomputable def extension_order_weight
    (G : GrowthDAG V) (a : V → Finset V → ℂ)
    (σ : List V) (S : Finset V) : ℝ :=
  quantum_measure G a σ S

theorem extension_order_invariance
    (G : GrowthDAG V) (cs : Fin 5 → ℤ)
    (σ σ' : List V) (S : Finset V)
    (hσ : σ.Perm σ')
    (hcausal : ∀ i j, G.precedes (σ.get i) (σ.get j) → i < j) :
    extension_order_weight G (bdg_local_weight G cs) σ S =
    extension_order_weight G (bdg_local_weight G cs) σ' S := by
  simpa [extension_order_weight, bdg_local_weight] using
    (bdg_causal_invariance G cs σ σ' S hσ hcausal)
