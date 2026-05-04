import RA_MotifCommitProtocol

/-!
# RA_MotifSelectorClosure

RA-native selector-closure bridge for the motif-commit protocol.

This module is deliberately abstract. It does not formalize a simulator policy
such as greedy tie-breaking, and it does not import quantum-mechanical or
engineered-consensus vocabulary. It states the site-local structure needed for
selector closure over certified-ready motif candidates:

* certified readiness = certified support plus causal readiness;
* selector closure = a selected, pairwise-compatible subset of certified-ready
  candidates at a site;
* selected commit = selected motif whose selected competitors are compatible;
* complete selector closure recovers the strict `CommitsAt` predicate from
  `RA_MotifCommitProtocol`.

This is the formal bridge suggested by the v0.3 causal-DAG motif-commit
simulator. Concrete selector policies remain downstream.
-/

namespace RA

/-! ## Layer 1: finite ActualizationDAG selector closure -/

section O01SelectorLayer

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Certified readiness at a DAG site: the support cut is certified for the
motif by the commit context and is causally ready at the site. -/
def DAGCertifiedReadyAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G) (x : V)
    (M : MotifCandidate V) (Q : CausalSupportCut V) : Prop :=
  Γ.supports M Q ∧ DAGReadyAt G Q x

/-- A site-local selector closure over certified-ready DAG motifs.

`selected` is intentionally only a predicate. Later modules may instantiate it
by BDG/local-ledger/orientation closure, by a derived unique-valid-candidate
package, or by a concrete simulator policy. -/
structure DAGSelectorClosureAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G) (x : V) where
  selected : MotifCandidate V → CausalSupportCut V → Prop
  selected_certified_ready :
    ∀ M Q, selected M Q → DAGCertifiedReadyAt G Γ x M Q
  selected_pairwise_compatible :
    ∀ M₁ Q₁ M₂ Q₂,
      selected M₁ Q₁ → selected M₂ Q₂ → ¬ Γ.incompatible M₁ M₂

/-- A selector closure is complete at a site when every certified-ready candidate
is selected. Complete closure is strong and often inappropriate in the presence
of unresolved incompatible alternatives; partial selector closure is the native
notion used to model narrowing. -/
def DAGSelectorCompleteAt
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    (S : DAGSelectorClosureAt G Γ x) : Prop :=
  ∀ M Q, DAGCertifiedReadyAt G Γ x M Q → S.selected M Q

/-- Selected commit at a DAG site: a selected motif whose selected competitors
are all compatible with it. For a `DAGSelectorClosureAt`, the second conjunct
is derivable from pairwise compatibility, but keeping it explicit mirrors the
commit-protocol shape. -/
def DAGSelectedCommitsAt
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    (S : DAGSelectorClosureAt G Γ x)
    (M : MotifCandidate V) (Q : CausalSupportCut V) : Prop :=
  S.selected M Q ∧
    ∀ M' Q', S.selected M' Q' → ¬ Γ.incompatible M M'

/-- Every selected motif/support-cut pair in a selector closure has a
selected-commit witness. -/
theorem DAGSelectedCommitsAt.of_selected
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    (S : DAGSelectorClosureAt G Γ x)
    {M : MotifCandidate V} {Q : CausalSupportCut V}
    (hsel : S.selected M Q) :
    DAGSelectedCommitsAt S M Q := by
  refine ⟨hsel, ?_⟩
  intro M' Q' hsel'
  exact S.selected_pairwise_compatible M Q M' Q' hsel hsel'

/-- A selected commit is certified-ready. -/
theorem DAGSelectedCommitsAt.certified_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    {S : DAGSelectorClosureAt G Γ x}
    {M : MotifCandidate V} {Q : CausalSupportCut V}
    (h : DAGSelectedCommitsAt S M Q) :
    DAGCertifiedReadyAt G Γ x M Q :=
  S.selected_certified_ready M Q h.1

/-- A selected commit has certified support. -/
theorem DAGSelectedCommitsAt.supports
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    {S : DAGSelectorClosureAt G Γ x}
    {M : MotifCandidate V} {Q : CausalSupportCut V}
    (h : DAGSelectedCommitsAt S M Q) :
    Γ.supports M Q :=
  (DAGSelectedCommitsAt.certified_ready h).1

/-- A selected commit is causally ready. -/
theorem DAGSelectedCommitsAt.ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    {S : DAGSelectorClosureAt G Γ x}
    {M : MotifCandidate V} {Q : CausalSupportCut V}
    (h : DAGSelectedCommitsAt S M Q) :
    DAGReadyAt G Q x :=
  (DAGSelectedCommitsAt.certified_ready h).2

/-- If selector closure is complete, selected commit recovers the strict DAG
commit predicate from `RA_MotifCommitProtocol`.

This theorem is the main formal bridge: strict commit is what one obtains when
selector closure covers all certified-ready alternatives at the site. -/
theorem DAGSelectedCommitsAt.to_strict_commits_of_complete
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    {S : DAGSelectorClosureAt G Γ x}
    {M : MotifCandidate V} {Q : CausalSupportCut V}
    (hcomplete : DAGSelectorCompleteAt S)
    (h : DAGSelectedCommitsAt S M Q) :
    DAGCommitsAt G Γ M Q x := by
  refine ⟨DAGSelectedCommitsAt.supports h,
    DAGSelectedCommitsAt.ready h, ?_⟩
  intro M' Q' hsupp' hready' hinc
  have hcert' : DAGCertifiedReadyAt G Γ x M' Q' := ⟨hsupp', hready'⟩
  have hsel' : S.selected M' Q' := hcomplete M' Q' hcert'
  exact h.2 M' Q' hsel' hinc

/-- A complete compatible selector closure cannot coexist with two certified-ready
incompatible alternatives. Thus unresolved incompatible alternatives force a
non-complete/partial selector closure, a severance branch, or some stronger
RA-native narrowing principle. -/
theorem DAGSelectorClosureAt.no_certified_ready_incompatible_of_complete
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    (S : DAGSelectorClosureAt G Γ x)
    (hcomplete : DAGSelectorCompleteAt S)
    {M₁ M₂ : MotifCandidate V} {Q₁ Q₂ : CausalSupportCut V}
    (hcert₁ : DAGCertifiedReadyAt G Γ x M₁ Q₁)
    (hcert₂ : DAGCertifiedReadyAt G Γ x M₂ Q₂)
    (hinc : Γ.incompatible M₁ M₂) :
    False := by
  have hsel₁ : S.selected M₁ Q₁ := hcomplete M₁ Q₁ hcert₁
  have hsel₂ : S.selected M₂ Q₂ := hcomplete M₂ Q₂ hcert₂
  exact S.selected_pairwise_compatible M₁ Q₁ M₂ Q₂ hsel₁ hsel₂ hinc

/-- Site-local unresolved incompatibility: two certified-ready alternatives are
incompatible, while neither is selected by the current selector closure. This is
an RA-native way to mark actualization ambiguity without importing external
superposition or voting vocabulary into the formal layer. -/
def DAGUnresolvedIncompatibilityAt
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G} {x : V}
    (S : DAGSelectorClosureAt G Γ x) : Prop :=
  ∃ M₁ Q₁ M₂ Q₂,
    DAGCertifiedReadyAt G Γ x M₁ Q₁ ∧
    DAGCertifiedReadyAt G Γ x M₂ Q₂ ∧
    Γ.incompatible M₁ M₂ ∧
    ¬ S.selected M₁ Q₁ ∧
    ¬ S.selected M₂ Q₂

end O01SelectorLayer

/-! ## Layer 2: concrete graph selector closure -/

section GraphSelectorLayer

/-- Certified readiness at a concrete graph site. -/
def GraphCertifiedReadyAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (x : GraphVertex G)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G) : Prop :=
  Γ.supports M Q ∧ GraphReadyAt G Q x

/-- A site-local selector closure over certified-ready concrete graph motifs. -/
structure GraphSelectorClosureAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (x : GraphVertex G) where
  selected : GraphMotifCandidate G → GraphSupportCut G → Prop
  selected_certified_ready :
    ∀ M Q, selected M Q → GraphCertifiedReadyAt G Γ x M Q
  selected_pairwise_compatible :
    ∀ M₁ Q₁ M₂ Q₂,
      selected M₁ Q₁ → selected M₂ Q₂ → ¬ Γ.incompatible M₁ M₂

/-- Completeness for a concrete graph selector closure. -/
def GraphSelectorCompleteAt
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x) : Prop :=
  ∀ M Q, GraphCertifiedReadyAt G Γ x M Q → S.selected M Q

/-- Selected commit at a concrete graph site. -/
def GraphSelectedCommitsAt
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G) : Prop :=
  S.selected M Q ∧
    ∀ M' Q', S.selected M' Q' → ¬ Γ.incompatible M M'

/-- Every selected concrete graph motif/support-cut pair has a selected-commit
witness. -/
theorem GraphSelectedCommitsAt.of_selected
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x)
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (hsel : S.selected M Q) :
    GraphSelectedCommitsAt S M Q := by
  refine ⟨hsel, ?_⟩
  intro M' Q' hsel'
  exact S.selected_pairwise_compatible M Q M' Q' hsel hsel'

/-- A selected concrete graph commit is certified-ready. -/
theorem GraphSelectedCommitsAt.certified_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    {S : GraphSelectorClosureAt G Γ x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (h : GraphSelectedCommitsAt S M Q) :
    GraphCertifiedReadyAt G Γ x M Q :=
  S.selected_certified_ready M Q h.1

/-- A selected concrete graph commit has certified support. -/
theorem GraphSelectedCommitsAt.supports
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    {S : GraphSelectorClosureAt G Γ x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (h : GraphSelectedCommitsAt S M Q) :
    Γ.supports M Q :=
  (GraphSelectedCommitsAt.certified_ready h).1

/-- A selected concrete graph commit is causally ready. -/
theorem GraphSelectedCommitsAt.ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    {S : GraphSelectorClosureAt G Γ x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (h : GraphSelectedCommitsAt S M Q) :
    GraphReadyAt G Q x :=
  (GraphSelectedCommitsAt.certified_ready h).2

/-- Complete graph selector closure recovers the strict graph commit predicate. -/
theorem GraphSelectedCommitsAt.to_strict_commits_of_complete
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    {S : GraphSelectorClosureAt G Γ x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (hcomplete : GraphSelectorCompleteAt S)
    (h : GraphSelectedCommitsAt S M Q) :
    GraphCommitsAt G Γ M Q x := by
  refine ⟨GraphSelectedCommitsAt.supports h,
    GraphSelectedCommitsAt.ready h, ?_⟩
  intro M' Q' hsupp' hready' hinc
  have hcert' : GraphCertifiedReadyAt G Γ x M' Q' := ⟨hsupp', hready'⟩
  have hsel' : S.selected M' Q' := hcomplete M' Q' hcert'
  exact h.2 M' Q' hsel' hinc

/-- A complete compatible graph selector closure cannot coexist with two
certified-ready incompatible concrete alternatives. -/
theorem GraphSelectorClosureAt.no_certified_ready_incompatible_of_complete
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x)
    (hcomplete : GraphSelectorCompleteAt S)
    {M₁ M₂ : GraphMotifCandidate G} {Q₁ Q₂ : GraphSupportCut G}
    (hcert₁ : GraphCertifiedReadyAt G Γ x M₁ Q₁)
    (hcert₂ : GraphCertifiedReadyAt G Γ x M₂ Q₂)
    (hinc : Γ.incompatible M₁ M₂) :
    False := by
  have hsel₁ : S.selected M₁ Q₁ := hcomplete M₁ Q₁ hcert₁
  have hsel₂ : S.selected M₂ Q₂ := hcomplete M₂ Q₂ hcert₂
  exact S.selected_pairwise_compatible M₁ Q₁ M₂ Q₂ hsel₁ hsel₂ hinc

/-- Concrete graph unresolved incompatibility. -/
def GraphUnresolvedIncompatibilityAt
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x) : Prop :=
  ∃ M₁ Q₁ M₂ Q₂,
    GraphCertifiedReadyAt G Γ x M₁ Q₁ ∧
    GraphCertifiedReadyAt G Γ x M₂ Q₂ ∧
    Γ.incompatible M₁ M₂ ∧
    ¬ S.selected M₁ Q₁ ∧
    ¬ S.selected M₂ Q₂

/-- Hasse-frontier-selected graph commit: the support cut is the finite Hasse
frontier extracted from the candidate past `P`. -/
def GraphHasseFrontierSelectedCommitsAt
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    (S : GraphSelectorClosureAt G Γ x)
    (M : GraphMotifCandidate G) (P : HasseCandidatePast G) : Prop :=
  GraphSelectedCommitsAt S M (supportCutOfFiniteHasseFrontier P)

/-- A Hasse-frontier-selected graph commit carries the frontier-readiness
reachability property from `RA_MotifCommitProtocol`. -/
theorem GraphHasseFrontierSelectedCommitsAt.frontier_reaches_site
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {x : GraphVertex G}
    {S : GraphSelectorClosureAt G Γ x}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (h : GraphHasseFrontierSelectedCommitsAt S M P) :
    ∀ y : GraphVertex G, IsHasseFrontier P y → Reachable G y x :=
  (GraphReadyAt_supportCutOfFiniteHasseFrontier_iff P x).1
    (GraphSelectedCommitsAt.ready h)

end GraphSelectorLayer

end RA
