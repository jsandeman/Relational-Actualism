import RA_MotifSelectorClosure
import RA_GraphOrientationClosure

/-!
# RA_MotifOrientationSupportBridge

RA-native bridge from graph-orientation closure certificates into the
motif-commit / selector-closure stack.

This module does not prove the hard theorem that RA graph/frontier/orientation
structure uniquely determines actualization.  Instead, it establishes the next
compiled-safe interface:

```text
finite Hasse frontier
  + graph-orientation closure certificate
  + local ledger/frontier sufficiency conditions
  -> certified graph-oriented motif support
  -> GraphCommitContext.supports
  -> selected commitment carries frontier reachability and orientation evidence
```

The module keeps inherited-theory comparison language out of the formal layer.
It uses only RA-native notions: Hasse frontier, graph orientation closure,
incidence sign source, support certification, incompatibility witness, selector
closure, selected commitment, and unresolved incompatibility.
-/

namespace RA

section GraphOrientationSupportBridge

/-- A graph-oriented support witness for a graph motif over a candidate past.

The witness packages the orientation-closure certificate already available in
`RA_GraphOrientationClosure` with two local support obligations:

* the motif carrier is represented inside the candidate past;
* the finite frontier and local ledger data are sufficient for this motif.

The proof obligations remain proposition-valued at this bridge layer because the
hard RA-native derivation is intentionally deferred to downstream modules. -/
structure GraphOrientedMotifSupport
    {G : _root_.ActualizationGraph}
    (M : GraphMotifCandidate G) (P : HasseCandidatePast G) where
  closure : GraphOrientationClosureCertificate P
  carrier_in_candidate_past :
    ∀ v ∈ M.carrier, P.contains v
  frontier_sufficient_for_motif : Prop
  local_ledger_compatible : Prop

/-- Certification predicate for a graph-oriented support witness.

The support cut must be the finite Hasse-frontier support cut for the witness's
candidate past, and the supplied orientation/ledger/frontier obligations must be
satisfied. -/
def GraphOrientedMotifSupport.certified
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P)
    (Q : GraphSupportCut G) : Prop :=
  W.frontier_sufficient_for_motif ∧
  W.local_ledger_compatible ∧
  W.closure.selector_compatible ∧
  W.closure.no_extra_random_labels ∧
  W.closure.nativeEvidence.no_particle_label_primitives ∧
  Q = supportCutOfFiniteHasseFrontier P

/-- A certified graph-oriented support witness has the finite Hasse-frontier
support cut as its support cut. -/
theorem GraphOrientedMotifSupport.support_eq_hasse_frontier
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P)
    {Q : GraphSupportCut G}
    (hcert : W.certified Q) :
    Q = supportCutOfFiniteHasseFrontier P := by
  rcases hcert with ⟨_, _, _, _, _, hQ⟩
  exact hQ

/-- Readiness of a certified graph-oriented support witness is exactly
reachability from every Hasse-frontier support vertex to the site. -/
theorem GraphOrientedMotifSupport.ready_iff_frontier_reaches_site
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P)
    {Q : GraphSupportCut G}
    (hcert : W.certified Q)
    (x : GraphVertex G) :
    GraphReadyAt G Q x ↔
      ∀ y : GraphVertex G, IsHasseFrontier P y → Reachable G y x := by
  rw [GraphOrientedMotifSupport.support_eq_hasse_frontier W hcert]
  exact GraphReadyAt_supportCutOfFiniteHasseFrontier_iff P x

/-- A graph-oriented support witness induces a deterministic incidence sign
source through its orientation-closure certificate. -/
def GraphOrientedMotifSupport.signSource
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P) : IncidenceSignSource P :=
  signSourceOfGraphOrientationClosureCertificate W.closure

/-- Evaluation rule for the sign source induced by a graph-oriented support
witness. -/
theorem GraphOrientedMotifSupport.signSource_eval
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P)
    (l : OrientedFrontierLink P) :
    (GraphOrientedMotifSupport.signSource W).signOf l =
      (W.closure.orientationData.polarityBetween l.src l.dst).toSign :=
  signSourceOfGraphOrientationClosureCertificate_eval W.closure l

/-- Boundary ledger induced by a graph-oriented support witness has the
seven-value N1 signature already proved in the orientation-closure layer. -/
theorem GraphOrientedMotifSupport.ledger_qN1_seven
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {P : HasseCandidatePast G}
    (W : GraphOrientedMotifSupport M P)
    (F : OrientedN1ThreeFrame P) (local_conserved : Prop) :
    SevenCharge
      (ledgerOfGraphOrientedBoundary
        (graphOrientedBoundaryOfClosureCertificate
          W.closure F local_conserved)).qN1 :=
  ledgerOfGraphOrientationClosureCertificate_qN1_seven
    W.closure F local_conserved

/-- Orientation-certified support for a motif/support-cut pair: the support cut
is certified by some graph-oriented support witness over some Hasse candidate
past. -/
def GraphOrientationSupports
    (G : _root_.ActualizationGraph)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G) : Prop :=
  ∃ P : HasseCandidatePast G,
    ∃ W : GraphOrientedMotifSupport M P,
      W.certified Q

/-- Any orientation-certified support has a Hasse-frontier witness. -/
theorem GraphOrientationSupports.has_witness
    {G : _root_.ActualizationGraph}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (hsupp : GraphOrientationSupports G M Q) :
    ∃ P : HasseCandidatePast G,
      ∃ W : GraphOrientedMotifSupport M P,
        W.certified Q :=
  hsupp

/-- A witnessed orientation conflict between two graph motifs.

The bridge does not prescribe a particular conflict rule.  It requires that
conflict used as motif incompatibility be witnessed by a native orientation
reason rather than by an ungrounded external label. -/
structure GraphOrientationConflictWitness
    {G : _root_.ActualizationGraph}
    (M₁ M₂ : GraphMotifCandidate G) where
  conflict_reason : Prop
  conflict_holds : conflict_reason

/-- Graph-orientation actualization context.

Support is fixed definitionally as `GraphOrientationSupports`.  The only
remaining context-specific component is the orientation-native incompatibility
relation, together with a witness discipline and symmetry. -/
structure GraphOrientationActualizationContext
    (G : _root_.ActualizationGraph) where
  incompatible : GraphMotifCandidate G → GraphMotifCandidate G → Prop
  incompatibility_is_witnessed :
    ∀ M₁ M₂, incompatible M₁ M₂ →
      GraphOrientationConflictWitness M₁ M₂
  incompatible_symmetric :
    ∀ M₁ M₂, incompatible M₁ M₂ → incompatible M₂ M₁

/-- Convert a graph-orientation actualization context into the commit context
expected by `RA_MotifCommitProtocol`. -/
def GraphOrientationActualizationContext.toCommitContext
    {G : _root_.ActualizationGraph}
    (Ω : GraphOrientationActualizationContext G) : GraphCommitContext G :=
  { supports := GraphOrientationSupports G
    incompatible := Ω.incompatible }

/-- Orientation selector closure at a concrete graph site. -/
abbrev GraphOrientationSelectorClosureAt
    {G : _root_.ActualizationGraph}
    (Ω : GraphOrientationActualizationContext G)
    (x : GraphVertex G) : Type :=
  GraphSelectorClosureAt G (Ω.toCommitContext) x

/-- Selected commitment in a graph-orientation actualization context. -/
def GraphOrientationSelectedCommitsAt
    {G : _root_.ActualizationGraph}
    {Ω : GraphOrientationActualizationContext G}
    {x : GraphVertex G}
    (S : GraphOrientationSelectorClosureAt Ω x)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G) : Prop :=
  GraphSelectedCommitsAt S M Q

/-- Selected commitment in a graph-orientation context carries an orientation
support witness and Hasse-frontier reachability to the selected site. -/
theorem GraphOrientationSelectedCommitsAt.has_oriented_frontier_witness
    {G : _root_.ActualizationGraph}
    {Ω : GraphOrientationActualizationContext G}
    {x : GraphVertex G}
    {S : GraphOrientationSelectorClosureAt Ω x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (h : GraphOrientationSelectedCommitsAt S M Q) :
    ∃ P : HasseCandidatePast G,
      ∃ W : GraphOrientedMotifSupport M P,
        W.certified Q ∧
        (∀ y : GraphVertex G, IsHasseFrontier P y → Reachable G y x) := by
  have hsupp : GraphOrientationSupports G M Q :=
    GraphSelectedCommitsAt.supports h
  rcases hsupp with ⟨P, W, hcert⟩
  have hready : GraphReadyAt G Q x := GraphSelectedCommitsAt.ready h
  have hfrontier :
      ∀ y : GraphVertex G, IsHasseFrontier P y → Reachable G y x :=
    (GraphOrientedMotifSupport.ready_iff_frontier_reaches_site
      W hcert x).1 hready
  exact ⟨P, W, hcert, hfrontier⟩

/-- Under complete selector closure, graph-orientation selected commitment
recovers the strict graph commit predicate. -/
theorem GraphOrientationSelectedCommitsAt.to_strict_commits_of_complete
    {G : _root_.ActualizationGraph}
    {Ω : GraphOrientationActualizationContext G}
    {x : GraphVertex G}
    {S : GraphOrientationSelectorClosureAt Ω x}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    (hcomplete : GraphSelectorCompleteAt S)
    (h : GraphOrientationSelectedCommitsAt S M Q) :
    GraphCommitsAt G (Ω.toCommitContext) M Q x := by
  exact GraphSelectedCommitsAt.to_strict_commits_of_complete hcomplete h

/-- Orientation-context unresolved incompatibility is the graph selector-layer
unresolved incompatibility for the orientation-induced commit context. -/
def GraphOrientationUnresolvedIncompatibilityAt
    {G : _root_.ActualizationGraph}
    {Ω : GraphOrientationActualizationContext G}
    {x : GraphVertex G}
    (S : GraphOrientationSelectorClosureAt Ω x) : Prop :=
  GraphUnresolvedIncompatibilityAt S

/-- Any unresolved incompatibility in an orientation context carries a witnessed
orientation conflict. -/
theorem GraphOrientationUnresolvedIncompatibilityAt.has_conflict_witness
    {G : _root_.ActualizationGraph}
    {Ω : GraphOrientationActualizationContext G}
    {x : GraphVertex G}
    {S : GraphOrientationSelectorClosureAt Ω x}
    (h : GraphOrientationUnresolvedIncompatibilityAt S) :
    ∃ M₁ Q₁ M₂ Q₂,
      GraphCertifiedReadyAt G (Ω.toCommitContext) x M₁ Q₁ ∧
      GraphCertifiedReadyAt G (Ω.toCommitContext) x M₂ Q₂ ∧
      Nonempty (GraphOrientationConflictWitness M₁ M₂) ∧
      ¬ S.selected M₁ Q₁ ∧
      ¬ S.selected M₂ Q₂ := by
  rcases h with ⟨M₁, Q₁, M₂, Q₂, hcert₁, hcert₂, hinc, hnsel₁, hnsel₂⟩
  exact ⟨M₁, Q₁, M₂, Q₂,
    hcert₁, hcert₂,
    ⟨Ω.incompatibility_is_witnessed M₁ M₂ hinc⟩,
    hnsel₁, hnsel₂⟩

/-- Orientation incompatibility is symmetric by context discipline. -/
theorem GraphOrientationActualizationContext.incompatible_symm
    {G : _root_.ActualizationGraph}
    (Ω : GraphOrientationActualizationContext G)
    {M₁ M₂ : GraphMotifCandidate G}
    (hinc : Ω.incompatible M₁ M₂) :
    Ω.incompatible M₂ M₁ :=
  Ω.incompatible_symmetric M₁ M₂ hinc

end GraphOrientationSupportBridge

end RA
