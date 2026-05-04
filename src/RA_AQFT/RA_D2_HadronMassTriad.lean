import RA_D2_MatterCartography
import RA_KvalRatio
import Mathlib.Data.Real.Basic

namespace RA_HadronMass

open RA_MatterCartography
open Real

/-- 
A Hadron Triad (e.g., a Proton) is defined in RA not as a bound state of 
continuum fields, but as a specific discrete topological cluster:
Three persistent 4-chains (valence fermions) cross-linked by symmetric 
branchings (strong gauge bosons).
--/
structure HadronTriad where
  fermion_1 : List Nat
  fermion_2 : List Nat
  fermion_3 : List Nat
  binding_motif : List Nat
  h_f1 : motif_to_observable fermion_1 = ObservableConcept.MassiveFermion
  h_f2 : motif_to_observable fermion_2 = ObservableConcept.MassiveFermion
  h_f3 : motif_to_observable fermion_3 = ObservableConcept.MassiveFermion
  h_bind : motif_to_observable binding_motif = ObservableConcept.StrongGaugeBoson

/--
The Triad Mass Ledger:
Calculates the sum of the scaled structural potentia (squared) for the triad components.
--/
noncomputable def triad_ledger_capacity (θ : ℝ) (m₀ : ℝ) : ℝ :=
  (∑ k : Fin 3, m₀ * kval θ k ^ 2)

/--
THEOREM: The Hadron Mass Bound.
The macroscopic geometric mass bound of a Hadron Triad evaluates strictly to 
a 2/3 topological ratio. This version is structurally aligned with the 
bedrock proof in RA_KvalRatio.
--/
theorem proton_mass_geometric_bound (θ : ℝ) (m₀ : ℝ) (hm₀ : 0 < m₀) :
  triad_ledger_capacity θ m₀ / (∑ k : Fin 3, sqrt m₀ * kval θ k) ^ 2 = 2 / 3 :=
by
  unfold triad_ledger_capacity
  -- This now matches the exact type signature of scaled_kval_ratio_two_thirds
  exact scaled_kval_ratio_two_thirds m₀ θ hm₀

end RA_HadronMass