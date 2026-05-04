import Mathlib.Data.Fintype.Basic

/-!
# RA Actualization Selector v1

Exploratory Lean scaffold for the Selector Closure programme.

This file is intentionally abstract. It does **not** prove the substantive
Selector Closure Theorem. Instead it gives precise names for the theorem ladder:

* structured potentia as a finite candidate type;
* admissible candidates as a subtype;
* actualization selector as a selector of one admissible candidate;
* completion outcome as either actualization or severance;
* constraint-closure data as the package that would make a selector derivable;
* no-history-quotient discipline as a classifier/injectivity distinction.

Suggested RAKB status:

```text
exploratory_formalization_scaffold_not_active_root
proof_status: scaffold / weak lemmas only
```

The intended next step is to replace the abstract placeholders with the existing
RA graph / BDG / LLC structures.
-/

namespace RA

/-- Abstract finite universe-state placeholder.
Later versions should replace this with the actual RA causal graph type. -/
structure UniverseState where
  Vertex : Type
  vertexFinite : Fintype Vertex

attribute [instance] UniverseState.vertexFinite

/-- Structured potentia for a state: a finite candidate type plus an
admissibility predicate and an abstract saturation flag. -/
structure Potentia (U : UniverseState) where
  Candidate : Type
  candidateFinite : Fintype Candidate
  admissible : Candidate → Prop
  saturated : Prop

attribute [instance] Potentia.candidateFinite

/-- The subtype of admissible candidates. -/
abbrev Admissible {U : UniverseState} (Pot : Potentia U) : Type :=
  {c : Pot.Candidate // Pot.admissible c}

/-- A selector is not a probability measure. It chooses one admissible candidate. -/
structure ActualizationSelector (U : UniverseState) (Pot : Potentia U) where
  choose : Admissible Pot

/-- Weak closure lemma: once an actualization selector is given, the selected
candidate is unique. This is intentionally easy; the hard theorem is to derive
the selector from RA constraints. -/
theorem selected_candidate_unique
    {U : UniverseState} {Pot : Potentia U}
    (Sel : ActualizationSelector U Pot) :
    ∃! c : Admissible Pot, c = Sel.choose := by
  refine ⟨Sel.choose, rfl, ?_⟩
  intro y hy
  exact hy

/-- A completion outcome is either a connected actualization or severance.
The severance branch is the formal placeholder for saturation / loss of a
unique connected continuation. -/
inductive CompletionOutcome {U : UniverseState} (Pot : Potentia U) where
  | actualize : Admissible Pot → CompletionOutcome Pot
  | severance : CompletionOutcome Pot

/-- Convert a selector into the corresponding connected completion outcome. -/
def outcomeOfSelector {U : UniverseState} {Pot : Potentia U}
    (Sel : ActualizationSelector U Pot) : CompletionOutcome Pot :=
  CompletionOutcome.actualize Sel.choose

/-- Abstract RA-native constraints on candidates.

In the full RA theory, `valid` should be refined into the conjunction of:

* BDG admissibility / strict kernel positivity;
* LLC / frontier-incidence compatibility;
* finitary actuality;
* graph-locality / covariance;
* no-actual-history-quotient discipline;
* saturation/severance awareness.

The field `valid_implies_admissible` says that a candidate satisfying the full
constraint package is also admitted by the kernel. -/
structure CandidateConstraints {U : UniverseState} (Pot : Potentia U) where
  valid : Pot.Candidate → Prop
  valid_implies_admissible : ∀ c : Pot.Candidate, valid c → Pot.admissible c

/-- Valid candidates as a subtype. -/
abbrev ValidCandidate {U : UniverseState} {Pot : Potentia U}
    (Ω : CandidateConstraints Pot) : Type :=
  {c : Pot.Candidate // Ω.valid c}

/-- A valid candidate canonically gives an admissible candidate. -/
def validToAdmissible {U : UniverseState} {Pot : Potentia U}
    (Ω : CandidateConstraints Pot) (c : ValidCandidate Ω) : Admissible Pot :=
  ⟨c.val, Ω.valid_implies_admissible c.val c.property⟩

/-- Constraint-closure data for the weak Selector Closure theorem.

This packages the hard part as a hypothesis: the RA-native constraints pick out
a unique valid candidate below saturation. The future hard theorem is to derive
this package from the concrete graph/BDG/LLC/incidence structures. -/
structure SelectorClosureData {U : UniverseState} (Pot : Potentia U) where
  constraints : CandidateConstraints Pot
  below_saturation : ¬ Pot.saturated
  unique_valid : ∃! c : Pot.Candidate, constraints.valid c

noncomputable section

/-- If the full RA constraints determine a unique valid candidate, they induce
an actualization selector. This is the first safe formal bridge from
constraint closure to selector closure. -/
def selectorFromClosureData {U : UniverseState} {Pot : Potentia U}
    (H : SelectorClosureData Pot) : ActualizationSelector U Pot := by
  classical
  refine { choose := ?_ }
  let c : Pot.Candidate := Classical.choose H.unique_valid
  have hc : H.constraints.valid c := (Classical.choose_spec H.unique_valid).1
  exact ⟨c, H.constraints.valid_implies_admissible c hc⟩

/-- Weak Selector Closure theorem: if the RA constraints determine a unique
valid candidate below saturation, then the induced selector has a unique
selected admissible candidate. -/
theorem weak_selector_closure
    {U : UniverseState} {Pot : Potentia U}
    (H : SelectorClosureData Pot) :
    ∃! c : Admissible Pot, c = (selectorFromClosureData H).choose := by
  exact selected_candidate_unique (selectorFromClosureData H)

end

/-- Abstract classifier for actual histories.

This captures the distinction between classifying histories and quotienting
histories. A classifier may map distinct histories to the same structural type;
that does **not** prove the histories are ontologically identical. -/
structure HistoryClassifier (History Class : Type) where
  classify : History → Class

/-- If a classifier is injective, then equality of class labels implies equality
of histories. Without injectivity, classification is not quotienting. -/
theorem same_class_implies_same_history_of_injective
    {History Class : Type} (κ : HistoryClassifier History Class)
    (hinj : Function.Injective κ.classify)
    {h₁ h₂ : History}
    (hclass : κ.classify h₁ = κ.classify h₂) :
    h₁ = h₂ :=
  hinj hclass

/-- A classifier is explicitly non-quotienting when it identifies at least one
pair of distinct histories by class label. -/
def ClassifiesButDoesNotQuotient {History Class : Type}
    (κ : HistoryClassifier History Class) : Prop :=
  ∃ h₁ h₂ : History, h₁ ≠ h₂ ∧ κ.classify h₁ = κ.classify h₂

/-- If a classifier classifies two distinct histories the same way, it is not
injective. Therefore it cannot be used to quotient actual histories without an
additional proof. -/
theorem not_injective_of_classifies_but_does_not_quotient
    {History Class : Type} (κ : HistoryClassifier History Class)
    (h : ClassifiesButDoesNotQuotient κ) :
    ¬ Function.Injective κ.classify := by
  intro hinj
  rcases h with ⟨h₁, h₂, hneq, hclass⟩
  exact hneq (hinj hclass)

/-- Abstract normal-form map for candidate descriptions.

This does not assert that normal forms are ontological quotients. It only names
what would be needed to distinguish representational redundancy from genuine
history distinction. -/
structure CandidateNormalForm {U : UniverseState} (Pot : Potentia U) where
  Normal : Type
  normalize : Pot.Candidate → Normal
  physically_equiv : Pot.Candidate → Pot.Candidate → Prop
  equiv_iff_same_normal : ∀ c d : Pot.Candidate,
    physically_equiv c d ↔ normalize c = normalize d

/-- If two candidate descriptions are physically equivalent under a normal-form
package, then they have the same normal form. -/
theorem same_normal_of_physically_equiv
    {U : UniverseState} {Pot : Potentia U}
    (NF : CandidateNormalForm Pot)
    {c d : Pot.Candidate}
    (h : NF.physically_equiv c d) :
    NF.normalize c = NF.normalize d :=
  (NF.equiv_iff_same_normal c d).1 h

/-- If two candidate descriptions have the same normal form, then they are
physically equivalent under the given normal-form package. -/
theorem physically_equiv_of_same_normal
    {U : UniverseState} {Pot : Potentia U}
    (NF : CandidateNormalForm Pot)
    {c d : Pot.Candidate}
    (h : NF.normalize c = NF.normalize d) :
    NF.physically_equiv c d :=
  (NF.equiv_iff_same_normal c d).2 h

/-!
## Hard theorem target, deliberately not asserted here

Selector Closure Theorem.
For any finite non-saturated RA universe-state `U = (G, Pot(G))`, the concrete
RA constraints — causal graph ontology, structured potentia, BDG admissibility,
LLC/frontier incidence, finitary actuality, covariance/no-label dependence,
no primitive randomness, and no actual-history quotient — determine a unique
connected completion. If those constraints no longer distinguish a connected
completion, the completion outcome is severance.

The theorem above is not yet proved. This file proves only the safe weak bridge:

```text
unique valid candidate from RA constraints ⇒ selector ⇒ unique selected candidate
```
-/

end RA
