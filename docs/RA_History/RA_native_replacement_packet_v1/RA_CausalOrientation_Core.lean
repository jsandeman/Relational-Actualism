import RA_AmpLocality
import RA_D1_Core_draft

/-!
# RA_CausalOrientation_Core

Native replacement draft for `RA_BaryonChirality.lean`.

This file keeps the real native content:
- one-way causal orientation from DAG acyclicity
- stability asymmetry between forward and reverse winding profiles
- preservation of the depth-2 ledger count across the classified motif extensions

Particle-physics labels are intentionally removed from the theorem names.
-/

open BigOperators

variable {V : Type*} [Fintype V] [DecidableEq V]

lemma no_reverse_precedence (G : CausalDAG V) (u v : V)
    (h_forward : G.precedes u v) : ¬ G.precedes v u := by
  intro h_back
  exact G.irrefl u (G.trans u v u h_forward h_back)

theorem one_way_precedence (G : CausalDAG V) :
    ∀ u v : V, G.precedes u v → ¬ G.precedes v u :=
  fun u v huv hvu => G.irrefl u (G.trans u v u huv hvu)

theorem reverse_winding_filtered : bdgScore 1 1 1 0 < 0 := by
  norm_num [bdgScore]

theorem forward_winding_stable : bdgScore 1 1 0 1 > 0 := by
  norm_num [bdgScore]

theorem fixed_point_orientation_symmetric :
    bdgScore 1 1 1 1 > 0 ∧ (1 : ℤ) = (1 : ℤ) := by
  exact ⟨by norm_num [bdgScore], rfl⟩

theorem orientation_one_way :
    bdgScore 1 1 1 0 < 0 ∧
    bdgScore 1 1 0 1 > 0 ∧
    bdgScore 1 1 1 1 > 0 ∧
    bdgScore 1 1 1 2 > 0 ∧ (1 : ℤ) < 2 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore], by norm_num⟩

theorem motif_depth2_profiles :
    bdgScore 0 0 0 0 = 1 ∧
    bdgScore 1 1 0 0 = 9 ∧
    bdgScore 1 1 1 1 = 1 ∧
    bdgScore 1 2 0 0 = 18 ∧
    bdgScore 2 1 0 0 = 8 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore]⟩

theorem symmetric_branch_depth2_preserved_all (m : Fin 15) :
    extensionScore_gluon m ≤ 0 ∨ extensionScore_gluon m = bdgScore 1 2 0 0 := by
  have h := D1c_gluon_complete m
  rcases h with h_le | h_eq
  · exact Or.inl h_le
  · exact Or.inr (by rw [h_eq]; norm_num [bdgScore])

theorem chain_escape_depth2_profile :
    bdgScore 1 1 0 0 = 9 := by
  norm_num [bdgScore]

theorem asymmetric_branch_replica_depth2_profile :
    bdgScore 2 1 0 0 = 8 := by
  norm_num [bdgScore]

theorem asymmetric_branch_extensions_classified (m : Fin 15) :
    extensionScore_quark m ≤ 0 ∨
    extensionScore_quark m = 9 ∨
    extensionScore_quark m = 8 ∨
    extensionScore_quark m = 2 := D1c_quark_complete m

theorem chain_depth2_fixed :
    bdgScore 0 0 0 0 = 1 ∧
    bdgScore 1 1 0 0 = 9 ∧
    bdgScore 1 1 1 1 = 1 ∧
    chainScore 1 = 0 ∧
    chainScore 3 = -7 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by simp [chainScore], by simp [chainScore]⟩

theorem orientation_and_depth2_ledger_core :
    (bdgScore 1 1 1 0 < 0) ∧
    (bdgScore 1 1 0 1 > 0) ∧
    (bdgScore 0 0 0 0 = 1) ∧
    (bdgScore 1 1 0 0 = 9) ∧
    (bdgScore 1 1 1 1 = 1) ∧
    (bdgScore 1 2 0 0 = 18) ∧
    (bdgScore 2 1 0 0 = 8) := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore]⟩
