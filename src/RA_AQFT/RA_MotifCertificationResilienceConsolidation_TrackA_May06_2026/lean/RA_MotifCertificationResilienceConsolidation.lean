import RA_MotifCertifiedSupportFamilyBridge

/-!
# RA_MotifCertificationResilienceConsolidation

Track A consolidation for the robust positive support-family / certification-family
line of the RA motif-actualization resilience workbench.

This module deliberately avoids the unsupported v1.x orientation-specific rescue
branch.  It introduces structural predicates for:

* strict-parent rescue;
* family-internal certification resilience;
* refinement back to certified-family readiness and ordinary family readiness;
* future monotonicity of the consolidated predicates.

No numerical rescue law, probability law, or Nature-facing prediction is asserted
here.  Concrete BDG-LLC, native-ledger, graph-cut, and orientation evidence may
refine the certificate context downstream.
-/

namespace RA

/-! ## DAG consolidation layer -/

section O01CertificationResilience

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Strict-parent rescue: the selected parent support cut is not ready at `x`,
but some independently certified family member is ready at `x`.

This formalizes the workbench distinction between strict rescue and generic
family-internal resilience. -/
def DAGStrictParentRescueAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Qparent : CausalSupportCut V) (x : V) : Prop :=
  F.cuts Qparent ∧ ¬ DAGReadyAt G Qparent x ∧
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x

/-- Family-internal resilience: at least one independently certified family
member remains ready.  Unlike strict rescue, this does not require the parent
support cut to fail first. -/
def DAGFamilyInternalResilienceAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F) (x : V) : Prop :=
  DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x

/-- Strict-parent rescue implies family-internal resilience. -/
theorem DAGStrictParentRescueAt.to_family_internal_resilience
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGStrictParentRescueAt G Γ M F Ξ Qparent x) :
    DAGFamilyInternalResilienceAt G Γ M F Ξ x :=
  h.2.2

/-- Strict-parent rescue records that the parent cut itself is not ready. -/
theorem DAGStrictParentRescueAt.parent_not_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGStrictParentRescueAt G Γ M F Ξ Qparent x) :
    ¬ DAGReadyAt G Qparent x :=
  h.2.1

/-- Strict-parent rescue implies ordinary certified-family readiness. -/
theorem DAGStrictParentRescueAt.to_certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGStrictParentRescueAt G Γ M F Ξ Qparent x) :
    DAGCertifiedFamilyReadyAt G Γ M F x :=
  DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready h.2.2

/-- Strict-parent rescue implies ordinary family readiness. -/
theorem DAGStrictParentRescueAt.to_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGStrictParentRescueAt G Γ M F Ξ Qparent x) :
    DAGFamilyReadyAt G F x :=
  DAGIndependentCertifiedFamilyReadyAt.to_family_ready h.2.2

/-- Family-internal resilience implies certified-family readiness. -/
theorem DAGFamilyInternalResilienceAt.to_certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F} {x : V}
    (h : DAGFamilyInternalResilienceAt G Γ M F Ξ x) :
    DAGCertifiedFamilyReadyAt G Γ M F x :=
  DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready h

/-- Family-internal resilience is future-monotone along DAG precedence. -/
theorem DAGFamilyInternalResilienceAt.future_mono
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F) {x z : V}
    (h : DAGFamilyInternalResilienceAt G Γ M F Ξ x)
    (hxz : G.precedes x z) :
    DAGFamilyInternalResilienceAt G Γ M F Ξ z :=
  DAGIndependentCertifiedFamilyReadyAt.future_mono G Γ M F Ξ h hxz

end O01CertificationResilience

/-! ## Concrete graph consolidation layer -/

section GraphCertificationResilience

/-- Graph strict-parent rescue: the parent support cut is not ready, but an
independently certified family member is ready. -/
def GraphStrictParentRescueAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Qparent : GraphSupportCut G) (x : GraphVertex G) : Prop :=
  F.cuts Qparent ∧ ¬ GraphReadyAt G Qparent x ∧
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x

/-- Graph family-internal resilience: some independently certified family member
is ready. -/
def GraphFamilyInternalResilienceAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F) (x : GraphVertex G) : Prop :=
  GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x

/-- Graph strict-parent rescue implies family-internal resilience. -/
theorem GraphStrictParentRescueAt.to_family_internal_resilience
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphStrictParentRescueAt G Γ M F Ξ Qparent x) :
    GraphFamilyInternalResilienceAt G Γ M F Ξ x :=
  h.2.2

/-- Graph strict-parent rescue records that the parent cut is not ready. -/
theorem GraphStrictParentRescueAt.parent_not_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphStrictParentRescueAt G Γ M F Ξ Qparent x) :
    ¬ GraphReadyAt G Qparent x :=
  h.2.1

/-- Graph strict-parent rescue implies ordinary certified-family readiness. -/
theorem GraphStrictParentRescueAt.to_certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphStrictParentRescueAt G Γ M F Ξ Qparent x) :
    GraphCertifiedFamilyReadyAt G Γ M F x :=
  GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready h.2.2

/-- Graph strict-parent rescue implies ordinary family readiness. -/
theorem GraphStrictParentRescueAt.to_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphStrictParentRescueAt G Γ M F Ξ Qparent x) :
    GraphFamilyReadyAt G F x :=
  GraphIndependentCertifiedFamilyReadyAt.to_family_ready h.2.2

/-- Graph family-internal resilience implies certified-family readiness. -/
theorem GraphFamilyInternalResilienceAt.to_certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F} {x : GraphVertex G}
    (h : GraphFamilyInternalResilienceAt G Γ M F Ξ x) :
    GraphCertifiedFamilyReadyAt G Γ M F x :=
  GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready h

/-- Graph family-internal resilience is future-monotone along reachability. -/
theorem GraphFamilyInternalResilienceAt.future_mono
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F) {x z : GraphVertex G}
    (h : GraphFamilyInternalResilienceAt G Γ M F Ξ x)
    (hxz : Reachable G x z) :
    GraphFamilyInternalResilienceAt G Γ M F Ξ z :=
  GraphIndependentCertifiedFamilyReadyAt.future_mono G Γ M F Ξ h hxz

end GraphCertificationResilience

end RA
