import RA_MotifOrientationSupportBridge

/-!
# RA_MotifCausalSeveranceBridge

RA-native bridge for causal-support severance and actualization fragility.

This module is intentionally abstract. It does not mutate an `ActualizationGraph`;
instead, it records a post-severance reachability predicate on the same graph
vertices. This is the formal surface corresponding to the v0.5 causal-DAG
simulator's support disruption views.
-/

namespace RA

section GraphCausalSeveranceBridge

/-- A graph-local severance profile supplies a post-severance reachability
relation over the same graph vertices. -/
structure GraphCausalSeveranceProfile
    (G : _root_.ActualizationGraph) where
  postReach : GraphVertex G → GraphVertex G → Prop

/-- A support cut is ready after severance when every support vertex reaches the
site in the post-severance reachability relation. -/
def GraphReadyAtAfterSeverance
    (G : _root_.ActualizationGraph)
    (S : GraphCausalSeveranceProfile G)
    (Q : GraphSupportCut G) (x : GraphVertex G) : Prop :=
  ∀ y ∈ Q.support, S.postReach y x

/-- If post-severance reachability is provided for every support vertex, then
readiness after severance holds. -/
theorem GraphReadyAtAfterSeverance.of_support_postReach
    {G : _root_.ActualizationGraph}
    {S : GraphCausalSeveranceProfile G}
    {Q : GraphSupportCut G} {x : GraphVertex G}
    (h : ∀ y ∈ Q.support, S.postReach y x) :
    GraphReadyAtAfterSeverance G S Q x :=
  h

/-- Ordinary readiness survives a severance profile when every original reachable
support edge used by the cut is preserved by the profile. -/
theorem GraphReadyAtAfterSeverance.of_reach_preserved
    {G : _root_.ActualizationGraph}
    {S : GraphCausalSeveranceProfile G}
    {Q : GraphSupportCut G} {x : GraphVertex G}
    (hready : GraphReadyAt G Q x)
    (hpres : ∀ y, y ∈ Q.support → Reachable G y x → S.postReach y x) :
    GraphReadyAtAfterSeverance G S Q x := by
  intro y hy
  exact hpres y hy (hready y hy)

/-- A support cut is destroyed at a site when at least one required support
vertex fails to reach the site after severance. -/
def GraphSupportCutDestroyedAt
    (G : _root_.ActualizationGraph)
    (S : GraphCausalSeveranceProfile G)
    (Q : GraphSupportCut G) (x : GraphVertex G) : Prop :=
  ∃ y : GraphVertex G, y ∈ Q.support ∧ ¬ S.postReach y x

/-- Destroyed support cuts are not ready after severance. -/
theorem GraphSupportCutDestroyedAt.not_ready_after
    {G : _root_.ActualizationGraph}
    {S : GraphCausalSeveranceProfile G}
    {Q : GraphSupportCut G} {x : GraphVertex G}
    (hdestroyed : GraphSupportCutDestroyedAt G S Q x) :
    ¬ GraphReadyAtAfterSeverance G S Q x := by
  intro hready
  rcases hdestroyed with ⟨y, hy, hnot⟩
  exact hnot (hready y hy)

/-- Post-severance commit predicate: certified support plus readiness in the
post-severance reachability profile, with incompatible certified-ready
competitors excluded in the same post-severance view. -/
def GraphCommitsAfterSeverance
    (G : _root_.ActualizationGraph)
    (Γ : GraphCommitContext G)
    (S : GraphCausalSeveranceProfile G)
    (M : GraphMotifCandidate G) (Q : GraphSupportCut G)
    (x : GraphVertex G) : Prop :=
  Γ.supports M Q ∧
  GraphReadyAtAfterSeverance G S Q x ∧
    ∀ M' Q', Γ.supports M' Q' →
      GraphReadyAtAfterSeverance G S Q' x →
      ¬ Γ.incompatible M M'

/-- A post-severance committed graph motif is post-severance ready. -/
theorem GraphCommitsAfterSeverance.ready
    {G : _root_.ActualizationGraph}
    {Γ : GraphCommitContext G}
    {S : GraphCausalSeveranceProfile G}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    {x : GraphVertex G}
    (h : GraphCommitsAfterSeverance G Γ S M Q x) :
    GraphReadyAtAfterSeverance G S Q x :=
  h.2.1

/-- Destroyed support blocks post-severance commitment for that support cut. -/
theorem GraphCommitBlockedBySupportDestruction
    {G : _root_.ActualizationGraph}
    {Γ : GraphCommitContext G}
    {S : GraphCausalSeveranceProfile G}
    {M : GraphMotifCandidate G} {Q : GraphSupportCut G}
    {x : GraphVertex G}
    (hdestroyed : GraphSupportCutDestroyedAt G S Q x) :
    ¬ GraphCommitsAfterSeverance G Γ S M Q x := by
  intro hcommit
  exact GraphSupportCutDestroyedAt.not_ready_after
    hdestroyed (GraphCommitsAfterSeverance.ready hcommit)

/-- Depth-indexed post-severance finality: the support cut is ready after
severance at every site whose depth is at least `d`. -/
def GraphFinalizedAtDepthAfterSeverance
    (G : _root_.ActualizationGraph)
    (S : GraphCausalSeveranceProfile G)
    (Q : GraphSupportCut G)
    (depth : GraphVertex G → Nat) (d : Nat) : Prop :=
  ∀ x : GraphVertex G, d ≤ depth x →
    GraphReadyAtAfterSeverance G S Q x

/-- Post-severance finality persists to later/deeper sites. -/
theorem GraphFinalizedAtDepthAfterSeverance.future_depth_mono
    {G : _root_.ActualizationGraph}
    {S : GraphCausalSeveranceProfile G}
    {Q : GraphSupportCut G}
    (depth : GraphVertex G → Nat) {d d' : Nat}
    (hfin : GraphFinalizedAtDepthAfterSeverance G S Q depth d)
    (hdd' : d ≤ d') :
    GraphFinalizedAtDepthAfterSeverance G S Q depth d' := by
  intro x hx
  exact hfin x (Nat.le_trans hdd' hx)

end GraphCausalSeveranceBridge

end RA
