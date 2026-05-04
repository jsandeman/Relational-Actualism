import Mathlib.Data.Fintype.Basic

/-!
# RA Actualization Selector Scaffold

This file is a non-canonical exploratory scaffold for the Selector Closure programme.
It is intentionally abstract. It does **not** prove the substantive Selector Closure Theorem.

Purpose:
  1. make the distinction between a selector and a measure explicit;
  2. prove the weak fact that a given selector yields a unique selected candidate;
  3. provide names for later connection to the existing RA graph/BDG/LLC files.

Suggested status in RAKB:
  exploratory_formalization_scaffold_not_active_root
-/

namespace RA

/-- Abstract finite universe-state placeholder.
Later versions should replace this with the actual RA causal graph type. -/
structure UniverseState where
  Vertex : Type
  vertexFinite : Fintype Vertex

/-- Structured potentia for a state: a finite candidate type plus an admissibility predicate. -/
structure Potentia (U : UniverseState) where
  Candidate : Type
  candidateFinite : Fintype Candidate
  admissible : Candidate → Prop

/-- A selector is not a probability measure. It chooses one admissible candidate. -/
structure ActualizationSelector (U : UniverseState) (Π : Potentia U) where
  choose : {c : Π.Candidate // Π.admissible c}

/-- Weak closure lemma: once an actualization selector is given, the selected candidate is unique. -/
theorem selected_candidate_unique
    {U : UniverseState} {Π : Potentia U}
    (Σ : ActualizationSelector U Π) :
    ∃! c : {c : Π.Candidate // Π.admissible c}, c = Σ.choose := by
  refine ⟨Σ.choose, rfl, ?_⟩
  intro y hy
  exact hy

/-- Placeholder for a saturation/severance flag. Later this should be defined from the BDG kernel. -/
inductive ContinuationStatus where
  | connected
  | severed
  deriving DecidableEq, Repr

/-- A total completion rule may either select a candidate or signal severance. -/
inductive CompletionOutcome {U : UniverseState} (Π : Potentia U) where
  | actualize : {c : Π.Candidate // Π.admissible c} → CompletionOutcome Π
  | severance : CompletionOutcome Π

/-- Abstract completion rule. The substantive theorem target is to derive such a rule from RA constraints. -/
abbrev CompletionRule (U : UniverseState) (Π : Potentia U) := CompletionOutcome Π

/-
Substantive open theorem target, not stated as a theorem here:

Selector Closure Theorem.
For any finite, non-saturated RA universe-state U=(G,Π(G)), the RA-native constraints
(DAG, BDG admissibility, LLC/frontier incidence, finitary actuality, no-history-quotient,
and covariance/no-label dependence) determine a unique CompletionOutcome.actualize c.
At saturation, the rule yields CompletionOutcome.severance.
-/

end RA
