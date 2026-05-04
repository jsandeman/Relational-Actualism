import RA_O01_KernelLocality
import RA_HasseFrontier_FiniteMaxExist

/-!
# RA_MotifCommitProtocol

Consensus-inspired motif commit semantics, expressed in RA-native vocabulary.

This module deliberately avoids importing engineered distributed-system terms
into the formal layer.  The operative object is a finite causal support cut:
a finite set of already-actualized supports whose presence in a realized past
makes a motif candidate ready for actualization.

Layer 1 works directly over `ActualizationDAG` from `RA_O01_KernelLocality`.
Layer 2 works over the concrete `ActualizationGraph` / Hasse-frontier ladder.
-/

namespace RA

/-! ## Layer 1: finite ActualizationDAG surface -/

section O01Layer

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- A finite motif candidate, represented only by its carrier vertices.

Later refinements can add BDG profile, incidence, orientation, ledger, or
closure certificates without changing the readiness/commit skeleton. -/
structure MotifCandidate (V : Type*) [Fintype V] [DecidableEq V] where
  carrier : Finset V

/-- A finite causal support cut for a motif.

`minimal` and `sufficient` are intentionally propositions at this layer.  The
hard RA work is to replace these fields by concrete BDG/local-ledger/frontier
conditions. -/
structure CausalSupportCut (V : Type*) [Fintype V] [DecidableEq V] where
  support : Finset V
  minimal : Prop
  sufficient : Prop

/-- Readiness: every vertex in the support cut lies in the realized causal past
of the candidate actualization site. -/
def DAGReadyAt
    (G : _root_.ActualizationDAG V)
    (Q : CausalSupportCut V) (x : V) : Prop :=
  ∀ y ∈ Q.support, G.precedes y x

/-- Readiness is equivalent to support-cut containment in `realized_past`. -/
theorem DAGReadyAt_iff_support_subset_realized_past
    (G : _root_.ActualizationDAG V)
    (Q : CausalSupportCut V) (x : V) :
    DAGReadyAt G Q x ↔ Q.support ⊆ _root_.realized_past G x := by
  constructor
  · intro h y hy
    simpa [_root_.realized_past] using h y hy
  · intro h y hy
    have hyPast : y ∈ _root_.realized_past G x := h hy
    simpa [_root_.realized_past] using hyPast

/-- Readiness is monotone toward the causal future. -/
theorem DAGReadyAt.future_mono
    (G : _root_.ActualizationDAG V)
    (Q : CausalSupportCut V) {x z : V}
    (hready : DAGReadyAt G Q x)
    (hxz : G.precedes x z) :
    DAGReadyAt G Q z := by
  intro y hy
  exact G.trans y x z (hready y hy) hxz

/-- A commit context supplies the native incompatibility relation.

This keeps the commit skeleton independent of any one concrete orientation,
ledger, or selector-closure package. -/
structure DAGCommitContext
    (G : _root_.ActualizationDAG V) where
  /-- `supports M Q` says that `Q` is an admissible/sufficient support cut
  for motif `M` in this context. Later modules should instantiate this using
  BDG locality, finite frontier data, orientation closure, and ledger checks. -/
  supports : MotifCandidate V → CausalSupportCut V → Prop
  incompatible : MotifCandidate V → MotifCandidate V → Prop

/-- A motif commits at `x` when its support cut is ready at `x`, and no ready
motif incompatible with it is also available in that same causal past. -/
def DAGCommitsAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (Q : CausalSupportCut V) (x : V) : Prop :=
  Γ.supports M Q ∧
  DAGReadyAt G Q x ∧
    ∀ M' Q', Γ.supports M' Q' → DAGReadyAt G Q' x →
      ¬ Γ.incompatible M M'

/-- A committed motif is ready. -/
theorem DAGCommitsAt.ready
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (Q : CausalSupportCut V) (x : V)
    (h : DAGCommitsAt G Γ M Q x) :
    DAGReadyAt G Q x :=
  h.2.1

/-- A committed motif is certified by its supplied support cut. -/
theorem DAGCommitsAt.supports
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (Q : CausalSupportCut V) (x : V)
    (h : DAGCommitsAt G Γ M Q x) :
    Γ.supports M Q :=
  h.1

/-- Direct local exclusion form: a committed motif rules out every ready motif
whose support cut is certified and which is incompatible with it at the same
causal site. -/
theorem DAGCommitsAt.no_ready_incompatible_same_site
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M M' : MotifCandidate V)
    (Q Q' : CausalSupportCut V) (x : V)
    (h : DAGCommitsAt G Γ M Q x)
    (hsupp' : Γ.supports M' Q')
    (hready' : DAGReadyAt G Q' x)
    (hinc : Γ.incompatible M M') :
    False :=
  h.2.2 M' Q' hsupp' hready' hinc

/-- Local safety: once `M₁` commits at `x`, no motif incompatible with `M₁` can
also commit at `x`. -/
theorem DAGCommitsAt.excludes_incompatible_same_site
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M₁ M₂ : MotifCandidate V)
    (Q₁ Q₂ : CausalSupportCut V) (x : V)
    (h₁ : DAGCommitsAt G Γ M₁ Q₁ x)
    (hinc : Γ.incompatible M₁ M₂) :
    ¬ DAGCommitsAt G Γ M₂ Q₂ x := by
  intro h₂
  exact DAGCommitsAt.no_ready_incompatible_same_site
    G Γ M₁ M₂ Q₁ Q₂ x h₁ h₂.1 h₂.2.1 hinc

/-- Depth-finality: all sites at depth at least `d` have the support cut in
their realized past.  This is the RA analogue of finality as causal inevitability. -/
def DAGFinalizedAtDepth
    (G : _root_.ActualizationDAG V) (Q : CausalSupportCut V)
    (depth : V → Nat) (d : Nat) : Prop :=
  ∀ x : V, d ≤ depth x → DAGReadyAt G Q x

/-- Finality persists when one restricts attention to later/deeper sites. -/
theorem DAGFinalizedAtDepth.future_depth_mono
    (G : _root_.ActualizationDAG V) (Q : CausalSupportCut V)
    (depth : V → Nat) {d d' : Nat}
    (hfin : DAGFinalizedAtDepth G Q depth d)
    (hdd' : d ≤ d') :
    DAGFinalizedAtDepth G Q depth d' := by
  intro x hx
  exact hfin x (Nat.le_trans hdd' hx)

end O01Layer

/-! ## Layer 2: concrete graph / Hasse-frontier surface -/

section GraphLayer

/-- A concrete graph motif candidate over the finite vertex subtype of an
`ActualizationGraph`. -/
structure GraphMotifCandidate (G : _root_.ActualizationGraph) where
  carrier : Finset (GraphVertex G)

/-- A finite causal support cut over the concrete graph vertex subtype. -/
structure GraphSupportCut (G : _root_.ActualizationGraph) where
  support : Finset (GraphVertex G)
  minimal : Prop
  sufficient : Prop

/-- Graph readiness: the support cut is contained in the reachable past of the
actualization site.  Because `Reachable` is reflexive, a site may witness its
own support only when the chosen support cut includes it. -/
def GraphReadyAt
    (G : _root_.ActualizationGraph)
    (Q : GraphSupportCut G) (x : GraphVertex G) : Prop :=
  ∀ y ∈ Q.support, Reachable G y x

/-- Graph readiness is monotone along concrete reachability. -/
theorem GraphReadyAt.future_mono
    (G : _root_.ActualizationGraph)
    (Q : GraphSupportCut G) {x z : GraphVertex G}
    (hready : GraphReadyAt G Q x)
    (hxz : Reachable G x z) :
    GraphReadyAt G Q z := by
  intro y hy
  exact reachable_trans (hready y hy) hxz

/-- Concrete graph commit context. -/
structure GraphCommitContext
    (G : _root_.ActualizationGraph) where
  /-- `supports M Q` says that `Q` is an admissible/sufficient support cut for
  graph motif `M` in this context. -/
  supports : GraphMotifCandidate G → GraphSupportCut G → Prop
  incompatible : GraphMotifCandidate G → GraphMotifCandidate G → Prop

/-- Concrete graph commit rule. -/
def GraphCommitsAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G)
    (x : GraphVertex G) : Prop :=
  Γ.supports M Q ∧
  GraphReadyAt G Q x ∧
    ∀ M' Q', Γ.supports M' Q' → GraphReadyAt G Q' x →
      ¬ Γ.incompatible M M'

/-- A concrete committed graph motif is ready. -/
theorem GraphCommitsAt.ready
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G)
    (x : GraphVertex G)
    (h : GraphCommitsAt G Γ M Q x) :
    GraphReadyAt G Q x :=
  h.2.1

/-- A committed graph motif is certified by its supplied support cut. -/
theorem GraphCommitsAt.supports
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G)
    (x : GraphVertex G)
    (h : GraphCommitsAt G Γ M Q x) :
    Γ.supports M Q :=
  h.1

/-- Direct local exclusion form: a committed graph motif rules out every ready
motif whose support cut is certified and which is incompatible with it at the
same concrete graph site. -/
theorem GraphCommitsAt.no_ready_incompatible_same_site
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M M' : GraphMotifCandidate G)
    (Q Q' : GraphSupportCut G) (x : GraphVertex G)
    (h : GraphCommitsAt G Γ M Q x)
    (hsupp' : Γ.supports M' Q')
    (hready' : GraphReadyAt G Q' x)
    (hinc : Γ.incompatible M M') :
    False :=
  h.2.2 M' Q' hsupp' hready' hinc

/-- Concrete graph safety: incompatible motifs cannot both commit at the same
actualization site. -/
theorem GraphCommitsAt.excludes_incompatible_same_site
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M₁ M₂ : GraphMotifCandidate G)
    (Q₁ Q₂ : GraphSupportCut G) (x : GraphVertex G)
    (h₁ : GraphCommitsAt G Γ M₁ Q₁ x)
    (hinc : Γ.incompatible M₁ M₂) :
    ¬ GraphCommitsAt G Γ M₂ Q₂ x := by
  intro h₂
  exact GraphCommitsAt.no_ready_incompatible_same_site
    G Γ M₁ M₂ Q₁ Q₂ x h₁ h₂.1 h₂.2.1 hinc

/-- The finite Hasse frontier of a graph-native candidate past, repackaged as a
support cut.

`minimal` and `sufficient` are placeholders at this scaffold level.  They are
the intended attachment points for later BDG/local-ledger/incidence theorems. -/
noncomputable def supportCutOfFiniteHasseFrontier
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    GraphSupportCut G := by
  classical
  letI : Fintype (GraphVertex G) := graphVertexFintype G
  exact
    { support := Finset.univ.filter (fun v => IsHasseFrontier P v)
      minimal := True
      sufficient := True }

/-- Membership in the support cut extracted from the finite Hasse frontier. -/
theorem mem_supportCutOfFiniteHasseFrontier_iff
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (v : GraphVertex G) :
    v ∈ (supportCutOfFiniteHasseFrontier P).support ↔ IsHasseFrontier P v := by
  classical
  simp [supportCutOfFiniteHasseFrontier]

/-- Readiness of the Hasse-frontier support cut is exactly reachability from
every Hasse-frontier vertex to the proposed site. -/
theorem GraphReadyAt_supportCutOfFiniteHasseFrontier_iff
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x : GraphVertex G) :
    GraphReadyAt G (supportCutOfFiniteHasseFrontier P) x ↔
      ∀ y : GraphVertex G, IsHasseFrontier P y → Reachable G y x := by
  constructor
  · intro h y hy
    exact h y ((mem_supportCutOfFiniteHasseFrontier_iff P y).2 hy)
  · intro h y hy
    exact h y ((mem_supportCutOfFiniteHasseFrontier_iff P y).1 hy)

/-- Depth-finality over the concrete graph surface. -/
def GraphFinalizedAtDepth
    (G : _root_.ActualizationGraph) (Q : GraphSupportCut G)
    (depth : GraphVertex G → Nat) (d : Nat) : Prop :=
  ∀ x : GraphVertex G, d ≤ depth x → GraphReadyAt G Q x

/-- Concrete graph finality persists to later/deeper sites. -/
theorem GraphFinalizedAtDepth.future_depth_mono
    (G : _root_.ActualizationGraph) (Q : GraphSupportCut G)
    (depth : GraphVertex G → Nat) {d d' : Nat}
    (hfin : GraphFinalizedAtDepth G Q depth d)
    (hdd' : d ≤ d') :
    GraphFinalizedAtDepth G Q depth d' := by
  intro x hx
  exact hfin x (Nat.le_trans hdd' hx)

end GraphLayer

end RA
