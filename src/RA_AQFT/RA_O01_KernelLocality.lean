import Mathlib

open BigOperators

/-!
# RA_O01_KernelLocality_v2

Dependency-first native replacement for the active O01 support chain.

This file isolates the genuinely RA-native proof content presently living inside
`RA_AmpLocality.lean`, but restates it directly in terms of DAG precedence,
realized past, BDG kernel evaluation, and admissibility.

It deliberately does **not** speak about complex amplitudes, quantum measure,
or linear-extension invariance. Those belong to the deferred bridge archive.

Status: source-level draft for systematic rewrite from the restored baseline.
-/

/-- A finite actualization DAG with a strict causal precedence relation. -/
structure ActualizationDAG (V : Type*) [Fintype V] [DecidableEq V] where
  precedes : V → V → Prop
  [decidable_precedes : DecidableRel precedes]
  irrefl : ∀ v, ¬ precedes v v
  trans : ∀ u w v, precedes u w → precedes w v → precedes u v

attribute [instance] ActualizationDAG.decidable_precedes

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- The realized causal past of a candidate vertex. -/
def realized_past (G : ActualizationDAG V) (v : V) : Finset V :=
  Finset.univ.filter (fun u => G.precedes u v)

/-- The local interval from `u` to `v` inside context `C`. -/
def local_interval (G : ActualizationDAG V) (u v : V) (C : Finset V) : Finset V :=
  C.filter (fun w => G.precedes u w ∧ G.precedes w v)

/-- Any interval endpointing at `v` lies inside the realized past of `v`. -/
lemma local_interval_subset_realized_past
    (G : ActualizationDAG V) (u v : V) (C : Finset V)
    (_hu : u ∈ realized_past G v) :
    local_interval G u v C ⊆ realized_past G v := by
  intro w hw
  simp only [local_interval, realized_past, Finset.mem_filter, Finset.mem_univ,
    true_and] at hw ⊢
  exact hw.2.2

/-- Restricting the context to the realized past of `v` does not change the
local interval from `u` to `v`. -/
lemma local_interval_eq_restricted
    (G : ActualizationDAG V) (u v : V) (C : Finset V)
    (_hu : u ∈ realized_past G v) :
    local_interval G u v C = local_interval G u v (C ∩ realized_past G v) := by
  ext w
  simp only [local_interval, realized_past, Finset.mem_filter, Finset.mem_inter,
    Finset.mem_univ, true_and]
  tauto

/-- The purely discrete BDG kernel for candidate `v` in context `C`. -/
def bdg_kernel (G : ActualizationDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : ℤ :=
  ∑ n : Fin 5,
    cs n * ((realized_past G v ∩ C).filter
      (fun u => (local_interval G u v C).card = n.val)).card

/-- The kernel depends only on the realized past of `v`. -/
lemma bdg_kernel_depends_on_realized_past
    (G : ActualizationDAG V) (cs : Fin 5 → ℤ)
    (v : V) (C : Finset V) :
    bdg_kernel G cs v C = bdg_kernel G cs v (C ∩ realized_past G v) := by
  simp only [bdg_kernel]
  congr 1
  ext n
  congr 1
  have hset : realized_past G v ∩ C = realized_past G v ∩ (C ∩ realized_past G v) := by
    ext u
    simp only [Finset.mem_inter]
    tauto
  suffices hfilt :
      (realized_past G v ∩ C).filter
        (fun u => (local_interval G u v C).card = n.val) =
      (realized_past G v ∩ (C ∩ realized_past G v)).filter
        (fun u => (local_interval G u v (C ∩ realized_past G v)).card = n.val) by
    rw [hfilt]
  rw [hset]
  apply Finset.filter_congr
  intro u hu
  have hu_past : u ∈ realized_past G v := by
    simp only [Finset.mem_inter] at hu
    exact hu.1
  rw [local_interval_eq_restricted G u v C hu_past,
      local_interval_eq_restricted G u v (C ∩ realized_past G v) hu_past]

/-- Native O01 theorem surface: if two contexts agree on the realized past of
`v`, the BDG kernel for `v` is identical. -/
theorem bdg_kernel_locality
    (G : ActualizationDAG V) (cs : Fin 5 → ℤ) (v : V)
    (C C' : Finset V)
    (h : C ∩ realized_past G v = C' ∩ realized_past G v) :
    bdg_kernel G cs v C = bdg_kernel G cs v C' := by
  rw [bdg_kernel_depends_on_realized_past G cs v C,
      bdg_kernel_depends_on_realized_past G cs v C',
      h]

/-- A candidate extension is admissible exactly when its BDG kernel is positive. -/
def admissible_extension
    (G : ActualizationDAG V) (cs : Fin 5 → ℤ) (v : V) (C : Finset V) : Prop :=
  0 < bdg_kernel G cs v C

/-- Native operational corollary of O01: admissibility depends only on the
realized past of the candidate. -/
theorem admissibility_depends_on_realized_past
    (G : ActualizationDAG V) (cs : Fin 5 → ℤ) (v : V)
    (C C' : Finset V)
    (h : C ∩ realized_past G v = C' ∩ realized_past G v) :
    admissible_extension G cs v C ↔ admissible_extension G cs v C' := by
  unfold admissible_extension
  rw [bdg_kernel_locality G cs v C C' h]
