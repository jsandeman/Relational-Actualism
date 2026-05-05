import RA_MotifNativeCertificateOverlapBridge

/-!
# RA_MotifNativeCertificateComponents

Native certificate-component anchoring layer for certified support-cut families.

The v0.9 simulator introduced native certificate-witness overlap as an
operational proxy for shared certification fate.  This v1.0 bridge keeps the
formal layer qualitative: it names the component surfaces that later BDG-LLC,
graph-cut, native-ledger, orientation, and causal-firewall modules may refine.

No probability law, numerical overlap score, or empirical rescue claim is
asserted here.  The bridge only shows that component witnesses can package into
the native-overlap witness layer from `RA_MotifNativeCertificateOverlapBridge`.
-/

namespace RA

/-! ## DAG component anchoring -/

section DAGComponentAnchoring

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Component-level native certificate context for a DAG support-cut family.

Each component is Type-valued so downstream modules can preserve witness data.
The seven components mirror the v0.9/v1.0 simulator surfaces:

* support-cut evidence
* Hasse/frontier evidence
* orientation-link evidence
* native-ledger evidence
* causal-past evidence
* BDG-LLC kernel-local evidence
* causal-firewall / severance-exposure evidence

`witness_of_components` packages these component witnesses into the native
certificate witness expected by the v0.9 overlap context. -/
structure DAGNativeCertificateComponentContext
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ) where
  supportComponent : CausalSupportCut V → Type*
  frontierComponent : CausalSupportCut V → Type*
  orientationComponent : CausalSupportCut V → Type*
  ledgerComponent : CausalSupportCut V → Type*
  causalPastComponent : CausalSupportCut V → Type*
  kernelLocalComponent : CausalSupportCut V → Type*
  firewallExposureComponent : CausalSupportCut V → Type*
  witness_of_components :
    ∀ Q,
      supportComponent Q → frontierComponent Q → orientationComponent Q →
      ledgerComponent Q → causalPastComponent Q → kernelLocalComponent Q →
      firewallExposureComponent Q → Ω.witness Q

/-- A DAG support cut is component-witnessed when all native component witness
surfaces are inhabited. -/
def DAGNativelyComponentWitnessed
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    (C : DAGNativeCertificateComponentContext Ω)
    (Q : CausalSupportCut V) : Prop :=
  Nonempty (C.supportComponent Q) ∧
  Nonempty (C.frontierComponent Q) ∧
  Nonempty (C.orientationComponent Q) ∧
  Nonempty (C.ledgerComponent Q) ∧
  Nonempty (C.causalPastComponent Q) ∧
  Nonempty (C.kernelLocalComponent Q) ∧
  Nonempty (C.firewallExposureComponent Q)

/-- Component witnesses package into the native-overlap witness layer. -/
theorem DAGNativelyComponentWitnessed.to_natively_witnessed
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω} {Q : CausalSupportCut V}
    (h : DAGNativelyComponentWitnessed C Q) :
    DAGNativelyWitnessed Ω Q := by
  rcases h with ⟨hs, hf, ho, hl, hp, hk, hx⟩
  rcases hs with ⟨s⟩
  rcases hf with ⟨f⟩
  rcases ho with ⟨o⟩
  rcases hl with ⟨l⟩
  rcases hp with ⟨p⟩
  rcases hk with ⟨k⟩
  rcases hx with ⟨x⟩
  exact ⟨C.witness_of_components Q s f o l p k x⟩

/-- Component-anchored native certified-family readiness. -/
def DAGNativeComponentCertifiedFamilyReadyAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ)
    (C : DAGNativeCertificateComponentContext Ω) (x : V) : Prop :=
  ∃ Q, DAGNativelyComponentWitnessed C Q ∧ DAGReadyAt G Q x

/-- Component-anchored readiness refines native-overlap certified readiness. -/
theorem DAGNativeComponentCertifiedFamilyReadyAt.to_native_overlap_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω} {x : V}
    (h : DAGNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x) :
    DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x := by
  rcases h with ⟨Q, hcomp, hready⟩
  exact ⟨Q, DAGNativelyComponentWitnessed.to_natively_witnessed hcomp, hready⟩

/-- Component-anchored readiness refines independent certified-family readiness. -/
theorem DAGNativeComponentCertifiedFamilyReadyAt.to_independent_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω} {x : V}
    (h : DAGNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x) :
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x := by
  exact DAGNativeOverlapCertifiedFamilyReadyAt.to_independent_ready
    (DAGNativeComponentCertifiedFamilyReadyAt.to_native_overlap_ready h)

/-- Component-anchored readiness is future-monotone. -/
theorem DAGNativeComponentCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ)
    (C : DAGNativeCertificateComponentContext Ω) {x z : V}
    (h : DAGNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x)
    (hxz : G.precedes x z) :
    DAGNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C z := by
  rcases h with ⟨Q, hcomp, hready⟩
  exact ⟨Q, hcomp, DAGReadyAt.future_mono G Q hready hxz⟩

end DAGComponentAnchoring

/-! ## Graph component anchoring -/

section GraphComponentAnchoring

/-- Component-level native certificate context for graph support-cut families. -/
structure GraphNativeCertificateComponentContext
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ) where
  supportComponent : GraphSupportCut G → Type*
  frontierComponent : GraphSupportCut G → Type*
  orientationComponent : GraphSupportCut G → Type*
  ledgerComponent : GraphSupportCut G → Type*
  causalPastComponent : GraphSupportCut G → Type*
  kernelLocalComponent : GraphSupportCut G → Type*
  firewallExposureComponent : GraphSupportCut G → Type*
  witness_of_components :
    ∀ Q,
      supportComponent Q → frontierComponent Q → orientationComponent Q →
      ledgerComponent Q → causalPastComponent Q → kernelLocalComponent Q →
      firewallExposureComponent Q → Ω.witness Q

/-- A graph support cut is component-witnessed when all native component witness
surfaces are inhabited. -/
def GraphNativelyComponentWitnessed
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    (C : GraphNativeCertificateComponentContext Ω)
    (Q : GraphSupportCut G) : Prop :=
  Nonempty (C.supportComponent Q) ∧
  Nonempty (C.frontierComponent Q) ∧
  Nonempty (C.orientationComponent Q) ∧
  Nonempty (C.ledgerComponent Q) ∧
  Nonempty (C.causalPastComponent Q) ∧
  Nonempty (C.kernelLocalComponent Q) ∧
  Nonempty (C.firewallExposureComponent Q)

/-- Component witnesses package into the graph native-overlap witness layer. -/
theorem GraphNativelyComponentWitnessed.to_natively_witnessed
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω} {Q : GraphSupportCut G}
    (h : GraphNativelyComponentWitnessed C Q) :
    GraphNativelyWitnessed Ω Q := by
  rcases h with ⟨hs, hf, ho, hl, hp, hk, hx⟩
  rcases hs with ⟨s⟩
  rcases hf with ⟨f⟩
  rcases ho with ⟨o⟩
  rcases hl with ⟨l⟩
  rcases hp with ⟨p⟩
  rcases hk with ⟨k⟩
  rcases hx with ⟨x⟩
  exact ⟨C.witness_of_components Q s f o l p k x⟩

/-- Component-anchored graph native certified-family readiness. -/
def GraphNativeComponentCertifiedFamilyReadyAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ)
    (C : GraphNativeCertificateComponentContext Ω) (x : GraphVertex G) : Prop :=
  ∃ Q, GraphNativelyComponentWitnessed C Q ∧ GraphReadyAt G Q x

/-- Component-anchored graph readiness refines native-overlap certified readiness. -/
theorem GraphNativeComponentCertifiedFamilyReadyAt.to_native_overlap_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω} {x : GraphVertex G}
    (h : GraphNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x) :
    GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x := by
  rcases h with ⟨Q, hcomp, hready⟩
  exact ⟨Q, GraphNativelyComponentWitnessed.to_natively_witnessed hcomp, hready⟩

/-- Component-anchored graph readiness refines independent certified-family readiness. -/
theorem GraphNativeComponentCertifiedFamilyReadyAt.to_independent_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω} {x : GraphVertex G}
    (h : GraphNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x) :
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x := by
  exact GraphNativeOverlapCertifiedFamilyReadyAt.to_independent_ready
    (GraphNativeComponentCertifiedFamilyReadyAt.to_native_overlap_ready h)

/-- Component-anchored graph readiness is future-monotone. -/
theorem GraphNativeComponentCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ)
    (C : GraphNativeCertificateComponentContext Ω) {x z : GraphVertex G}
    (h : GraphNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C x)
    (hxz : Reachable G x z) :
    GraphNativeComponentCertifiedFamilyReadyAt G Γ M F Ξ Ω C z := by
  rcases h with ⟨Q, hcomp, hready⟩
  exact ⟨Q, hcomp, GraphReadyAt.future_mono G Q hready hxz⟩

end GraphComponentAnchoring

end RA
