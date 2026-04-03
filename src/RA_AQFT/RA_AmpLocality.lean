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
--
-- KEY INSIGHT O01: Causal intervals [u,v]_C lie entirely in past(v)
--                  (from transitivity of the causal order alone).
--                  Therefore δS_BDG(v,C) depends only on C ∩ past(v).
--
-- KEY INSIGHT O02: The amplitude a v (S ∩ causal_past G v) depends only
--                  on v and S — not on accumulated prior steps.
--                  So the foldl is a commutative product, and List.Perm.prod_eq
--                  gives the result directly. The causal ordering of σ is
--                  irrelevant — O02 holds for ALL permutations.

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Complex.Exponential
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Data.List.Perm.Basic

open BigOperators Complex

-- ═══════════════════════════════════════════════════════════════
-- SECTION 1: Causal DAG structure
-- ═══════════════════════════════════════════════════════════════

/-- A causal DAG is a finite type with a strict partial order (the causal relation). -/
structure CausalDAG (V : Type*) [Fintype V] [DecidableEq V] where
  /-- The causal order: precedes u v means u causally precedes v -/
  precedes : V → V → Prop
  [decidable_precedes : DecidableRel precedes]
  /-- Strict partial order conditions -/
  irrefl   : ∀ v, ¬ precedes v v
  trans    : ∀ u w v, precedes u w → precedes w v → precedes u v

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- The causal past of v: all vertices that causally precede v. -/
def causal_past (G : CausalDAG V) (v : V) : Finset V :=
  Finset.univ.filter (fun u => G.precedes u v)

/-- The causal interval between u and v within context C. -/
def causal_interval (G : CausalDAG V) (u v : V) (C : Finset V) : Finset V :=
  C.filter (fun w => G.precedes u w ∧ G.precedes w v)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 2: Key Lemmas — intervals lie in the causal past
-- ═══════════════════════════════════════════════════════════════

/-- LEMMA 1: If u ∈ past(v) and w ∈ [u,v]_C, then w ∈ past(v).
    Proof: w ∈ [u,v]_C means u ≤ w ≤ v. By transitivity, w ≤ v. -/
lemma interval_subset_past (G : CausalDAG V) (u v : V) (C : Finset V)
    (hu : u ∈ causal_past G v) :
    causal_interval G u v C ⊆ causal_past G v := by
  intro w hw
  simp [causal_interval, causal_past] at hw ⊢
  obtain ⟨_, _, hwv⟩ := hw
  exact hwv

/-- LEMMA 2: The causal interval [u,v]_C equals [u,v]_{C ∩ past(v)}. -/
lemma interval_eq_interval_past (G : CausalDAG V) (u v : V) (C : Finset V)
    (hu : u ∈ causal_past G v) :
    causal_interval G u v C = causal_interval G u v (C ∩ causal_past G v) := by
  ext w
  simp [causal_interval, Finset.mem_inter, causal_past]
  constructor
  · intro ⟨hwC, huw, hwv⟩
    exact ⟨hwC, hwv, huw, hwv⟩
  · intro ⟨hwC, _, huw, hwv⟩
    exact ⟨hwC, huw, hwv⟩

-- ═══════════════════════════════════════════════════════════════
-- SECTION 3: BDG action increment
-- ═══════════════════════════════════════════════════════════════

/-- The BDG action increment when adding vertex v to causal set C. -/
def bdg_increment (G : CausalDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : ℤ :=
  ∑ n : Fin 5,
    cs n * ((causal_past G v ∩ C).filter
      (fun u => (causal_interval G u v C).card = n.val)).card

/-- LEMMA 3: The BDG increment depends only on C ∩ past(v). -/
lemma bdg_increment_depends_on_past_only (G : CausalDAG V) (cs : Fin 5 → ℤ)
    (v : V) (C : Finset V) :
    bdg_increment G cs v C = bdg_increment G cs v (C ∩ causal_past G v) := by
  simp only [bdg_increment]
  congr 1
  ext n
  congr 1
  have hset : causal_past G v ∩ C = causal_past G v ∩ (C ∩ causal_past G v) := by
    ext u
    simp [Finset.mem_inter, causal_past]
    tauto
  rw [hset]
  congr 1
  ext u
  simp only [Finset.mem_filter]
  constructor
  · intro ⟨hu, hsize⟩
    refine ⟨hu, ?_⟩
    have hu_past : u ∈ causal_past G v := by
      simp [causal_past] at hu ⊢; exact hu.1
    rw [← interval_eq_interval_past G u v C hu_past]
    rw [← interval_eq_interval_past G u v (C ∩ causal_past G v) hu_past] at hsize ⊢
    convert hsize using 2
    ext w
    simp [causal_interval, Finset.mem_inter, causal_past]
    tauto
  · intro ⟨hu, hsize⟩
    refine ⟨hu, ?_⟩
    have hu_past : u ∈ causal_past G v := by
      simp [causal_past] at hu ⊢; exact hu.1
    rw [← interval_eq_interval_past G u v C hu_past]
    rw [← interval_eq_interval_past G u v (C ∩ causal_past G v) hu_past] at hsize ⊢
    convert hsize using 2
    ext w
    simp [causal_interval, Finset.mem_inter, causal_past]
    tauto

-- ═══════════════════════════════════════════════════════════════
-- SECTION 4: BDG amplitude and amplitude locality (O01)
-- ═══════════════════════════════════════════════════════════════

/-- The BDG local amplitude for adding vertex v to context C. -/
def bdg_amplitude (G : CausalDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : ℂ :=
  Complex.exp (Complex.I * (bdg_increment G cs v C : ℂ))

/-- DEFINITION: Amplitude locality for an amplitude function a. -/
def amplitude_local (G : CausalDAG V) (a : V → Finset V → ℂ) : Prop :=
  ∀ v : V, ∀ C C' : Finset V,
    C ∩ causal_past G v = C' ∩ causal_past G v →
    a v C = a v C'

/-- THEOREM O01: The BDG amplitude satisfies amplitude locality.
    Follows from transitivity of the causal order + BDG action structure.
    No appeal to the QFT continuum limit is required. -/
theorem bdg_amplitude_locality (G : CausalDAG V) (cs : Fin 5 → ℤ) :
    amplitude_local G (bdg_amplitude G cs) := by
  intro v C C' hpast
  simp only [bdg_amplitude]
  congr 1
  norm_cast
  rw [bdg_increment_depends_on_past_only G cs v C]
  rw [bdg_increment_depends_on_past_only G cs v C']
  congr 1
  simp only [bdg_increment]
  congr 1
  ext n
  congr 1
  have : causal_past G v ∩ (C ∩ causal_past G v) =
         causal_past G v ∩ (C' ∩ causal_past G v) := by
    rw [hpast]
  rw [this]

-- ═══════════════════════════════════════════════════════════════
-- SECTION 5: Quantum measure and causal invariance (O02)
-- ═══════════════════════════════════════════════════════════════

/-- The quantum measure for a set of observables S, given amplitude function a
    and linear extension σ of the causal order. -/
noncomputable def quantum_measure (G : CausalDAG V) (a : V → Finset V → ℂ)
    (σ : List V) (S : Finset V) : ℝ :=
  Complex.normSq (σ.foldl (fun acc v => acc * a v (S ∩ causal_past G v)) 1)

/-- Helper: foldl (fun acc v => acc * f v) b l = b * (l.map f).prod
    for any function f : V → ℂ.
    Proof: by induction on l. -/
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

/-- THEOREM O02: For BDG dynamics, causal invariance holds unconditionally.
    The quantum measure is independent of the ordering σ.
    This holds for ALL permutations of σ, not just causal linear extensions —
    because each amplitude factor depends only on the node and the DAG causal
    past, not on the accumulated state of the foldl.
    Proof: foldl = commutative product over list → List.Perm.prod_eq. -/
theorem bdg_causal_invariance (G : CausalDAG V) (cs : Fin 5 → ℤ)
    (σ σ' : List V) (S : Finset V)
    (hσ : σ.Perm σ') :
    quantum_measure G (bdg_amplitude G cs) σ S =
    quantum_measure G (bdg_amplitude G cs) σ' S := by
  simp only [quantum_measure]
  congr 1
  -- Let f be the amplitude function evaluated at each node
  let f : V → ℂ := fun v => bdg_amplitude G cs v (S ∩ causal_past G v)
  -- Rewrite both foldls as products of mapped lists
  have key : ∀ l : List V,
      l.foldl (fun acc v => acc * f v) 1 = (l.map f).prod := by
    intro l
    rw [foldl_eq_mul_prod f l 1, one_mul]
  rw [key σ, key σ']
  -- Permuted lists have the same product in a CommMonoid (ℂ under *)
  exact List.Perm.prod_eq (hσ.map f)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 6: Summary
-- ═══════════════════════════════════════════════════════════════

/-!
## Proof status: ZERO sorry tags

PROVED (zero sorry):
  interval_subset_past         [Lemma 1: intervals lie in causal past]
  interval_eq_interval_past    [Lemma 2: interval independence from spacelike]
  bdg_increment_depends_on_past_only  [Lemma 3: δS depends on C∩past(v) only]
  bdg_amplitude_locality       [THEOREM O01: BDG amplitude is amplitude-local]
  foldl_eq_mul_prod            [Helper: foldl = b * prod of mapped list]
  bdg_causal_invariance        [THEOREM O02: quantum measure is permutation-invariant]

WHAT THIS ESTABLISHES:
  O01: Amplitude locality is a theorem of BDG discrete dynamics.
       Follows from transitivity of causal order + BDG action structure.

  O02: Causal invariance holds unconditionally for BDG dynamics.
       Holds for ALL permutations of σ (stronger than originally stated).
       Proof: the foldl is a commutative product; List.Perm.prod_eq closes it.
       The hcausal hypothesis from the original draft was unnecessary.

  In the KB:
    O01: OP → LV ✓
    O02: LV (1 assembly sorry) → LV (0 sorry) ✓
    L07 (causal_invariance_conditional): conditionality lifts for BDG dynamics ✓
-/
