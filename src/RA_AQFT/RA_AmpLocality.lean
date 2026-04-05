-- RA_AmpLocality.lean
-- Proof of O01: Amplitude Locality as a theorem of BDG discrete DAG dynamics
-- Proof of O02: Causal Invariance unconditional for BDG dynamics
--
-- THEOREM O01: For the BDG amplitude function, a(v|C) = a(v|C') whenever
--              C ∩ past(v) = C' ∩ past(v)
--
-- THEOREM O02: quantum_measure G (bdg_amplitude G cs) σ S =
--              quantum_measure G (bdg_amplitude G cs) σ' S
--              for any permutation σ.Perm σ'
--              (NO hcausal hypothesis needed — holds for all permutations)

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Algebra.BigOperators.Group.List.Lemmas
import Mathlib.Data.List.Perm.Basic

open BigOperators Complex Classical

-- ═══════════════════════════════════════════════════════════════
-- SECTION 1: Causal DAG structure
-- ═══════════════════════════════════════════════════════════════

/-- A causal DAG is a finite type with a strict partial order (the causal relation). -/
structure CausalDAG (V : Type*) [Fintype V] [DecidableEq V] where
  /-- The causal order: precedes u v means u causally precedes v -/
  precedes : V → V → Prop
  /-- Strict partial order conditions -/
  irrefl   : ∀ v, ¬ precedes v v
  trans    : ∀ u w v, precedes u w → precedes w v → precedes u v

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- The causal past of v: all vertices that causally precede v. -/
noncomputable def causal_past (G : CausalDAG V) (v : V) : Finset V :=
  Finset.univ.filter (fun u => G.precedes u v)

/-- The causal interval between u and v within context C. -/
noncomputable def causal_interval (G : CausalDAG V) (u v : V) (C : Finset V) : Finset V :=
  C.filter (fun w => G.precedes u w ∧ G.precedes w v)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 2: Key Lemmas — intervals lie in the causal past
-- ═══════════════════════════════════════════════════════════════

/-- LEMMA 1: If u ∈ past(v) and w ∈ [u,v]_C, then w ∈ past(v). -/
lemma interval_subset_past (G : CausalDAG V) (u v : V) (C : Finset V)
    (_hu : u ∈ causal_past G v) :
    causal_interval G u v C ⊆ causal_past G v := by
  intro w hw
  simp only [causal_interval, causal_past, Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢
  tauto

/-- LEMMA 2: The causal interval [u,v]_C equals [u,v]_{C ∩ past(v)}. -/
lemma interval_eq_interval_past (G : CausalDAG V) (u v : V) (C : Finset V)
    (_hu : u ∈ causal_past G v) :
    causal_interval G u v C = causal_interval G u v (C ∩ causal_past G v) := by
  ext w
  simp only [causal_interval, causal_past, Finset.mem_inter, Finset.mem_filter, Finset.mem_univ, true_and]
  tauto

-- ═══════════════════════════════════════════════════════════════
-- SECTION 3: BDG action increment
-- ═══════════════════════════════════════════════════════════════

/-- The BDG action increment when adding vertex v to causal set C. -/
noncomputable def bdg_increment (G : CausalDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : ℤ :=
  ∑ n : Fin 5,
    cs n * ((causal_past G v ∩ C).filter
      (fun u => (causal_interval G u v C).card = n.val)).card

/-- LEMMA 3: The BDG increment depends only on C ∩ past(v). -/
lemma bdg_increment_depends_on_past_only (G : CausalDAG V) (cs : Fin 5 → ℤ)
    (v : V) (C : Finset V) :
    bdg_increment G cs v C = bdg_increment G cs v (C ∩ causal_past G v) := by
  simp only [bdg_increment]
  apply Finset.sum_congr rfl
  intro n _
  
  -- 1. Prove the base intersecting sets are equal
  have hset : causal_past G v ∩ C = causal_past G v ∩ (C ∩ causal_past G v) := by
    ext u
    simp only [causal_past, Finset.mem_inter, Finset.mem_filter, Finset.mem_univ, true_and]
    tauto
    
  -- 2. Prove the filtered sets are exactly equal to bypass coercion / .card issues
  have h_filter : (causal_past G v ∩ C).filter (fun u => (causal_interval G u v C).card = n.val) =
                  (causal_past G v ∩ (C ∩ causal_past G v)).filter (fun u => (causal_interval G u v (C ∩ causal_past G v)).card = n.val) := by
    rw [hset]
    apply Finset.filter_congr
    intro u hu
    have hu_past : u ∈ causal_past G v := by
      simp only [Finset.mem_inter] at hu
      exact hu.1
    rw [interval_eq_interval_past G u v C hu_past]
    
  -- 3. Rewrite the set inside the .card and multiplication
  rw [h_filter]

-- ═══════════════════════════════════════════════════════════════
-- SECTION 4: BDG amplitude and amplitude locality (O01)
-- ═══════════════════════════════════════════════════════════════

/-- The BDG local amplitude for adding vertex v to context C. -/
noncomputable def bdg_amplitude (G : CausalDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : ℂ :=
  Complex.exp (Complex.I * (bdg_increment G cs v C : ℂ))

/-- DEFINITION: Amplitude locality for an amplitude function a. -/
def amplitude_local (G : CausalDAG V) (a : V → Finset V → ℂ) : Prop :=
  ∀ v : V, ∀ C C' : Finset V,
    C ∩ causal_past G v = C' ∩ causal_past G v →
    a v C = a v C'

/-- THEOREM O01: The BDG amplitude satisfies amplitude locality. -/
theorem bdg_amplitude_locality (G : CausalDAG V) (cs : Fin 5 → ℤ) :
    amplitude_local G (bdg_amplitude G cs) := by
  intro v C C' hpast
  have h1 := bdg_increment_depends_on_past_only G cs v C
  have h2 := bdg_increment_depends_on_past_only G cs v C'
  simp only [bdg_amplitude]
  rw [h1, h2, hpast]

-- ═══════════════════════════════════════════════════════════════
-- SECTION 5: Quantum measure and causal invariance (O02)
-- ═══════════════════════════════════════════════════════════════

/-- The quantum measure for a set of observables S... -/
noncomputable def quantum_measure (G : CausalDAG V) (a : V → Finset V → ℂ)
    (σ : List V) (S : Finset V) : ℝ :=
  Complex.normSq (σ.foldl (fun acc v => acc * a v (S ∩ causal_past G v)) 1)

omit [Fintype V] [DecidableEq V] in
/-- Helper: foldl = commutative product over mapped list -/
private lemma foldl_eq_mul_prod (f : V → ℂ) :
    ∀ (l : List V) (b : ℂ),
    l.foldl (fun acc v => acc * f v) b = b * (l.map f).prod := by
  intro l
  induction l with
  | nil => intro b; simp
  | cons h t ih =>
    intro b
    simp only [List.foldl, List.map, List.prod_cons]
    rw [ih (b * f h), mul_assoc]

/-- THEOREM O02: For BDG dynamics, causal invariance holds unconditionally. -/
theorem bdg_causal_invariance (G : CausalDAG V) (cs : Fin 5 → ℤ)
    (σ σ' : List V) (S : Finset V)
    (hσ : σ.Perm σ') :
    quantum_measure G (bdg_amplitude G cs) σ S =
    quantum_measure G (bdg_amplitude G cs) σ' S := by
  simp only [quantum_measure]
  let f : V → ℂ := fun v => bdg_amplitude G cs v (S ∩ causal_past G v)
  have key : ∀ l : List V, l.foldl (fun acc v => acc * f v) 1 = (l.map f).prod := by
    intro l
    rw [foldl_eq_mul_prod f l 1, one_mul]
  rw [key σ, key σ']
  congr 1
  exact List.Perm.prod_eq (List.Perm.map f hσ)

-- ═══════════════════════════════════════════════════════════════
-- Summary: Zero `sorry` tags. O01 and O02 fully verified.
-- ═══════════════════════════════════════════════════════════════