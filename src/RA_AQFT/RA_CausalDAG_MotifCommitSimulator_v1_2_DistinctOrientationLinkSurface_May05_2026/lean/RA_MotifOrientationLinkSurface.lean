import RA_MotifNativeCertificateComponents

/-!
# RA_MotifOrientationLinkSurface

A conservative Lean-facing vocabulary for a distinct orientation-link certificate
surface.

The v1.1 audit showed that the v0.9/v1.0 simulator component columns
`support_overlap`, `frontier_overlap`, and `orientation_overlap` were identical.
This module does **not** assert a numerical orientation-rescue law.  It only adds
an abstract orientation-link witness surface that downstream native-orientation
modules can instantiate independently of support/frontier evidence.
-/

namespace RA

section DAGOrientationLinkSurface

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Extra orientation-link evidence for a DAG support cut, separated from the
older component context's generic `orientationEvidence` field.  The data are
Type-valued so downstream orientation modules can retain incidence/sign-source
structure. -/
structure DAGOrientationLinkSurfaceContext
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    (C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω) where
  orientationLinkEvidence : CausalSupportCut V → Type*
  orientationLinkRefinesComponent :
    ∀ Q, orientationLinkEvidence Q → C.orientationEvidence Q

/-- A cut has the distinct orientation-link surface when the link evidence is
inhabited. -/
def DAGHasOrientationLinkSurface
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    (Λ : DAGOrientationLinkSurfaceContext C)
    (Q : CausalSupportCut V) : Prop :=
  Nonempty (Λ.orientationLinkEvidence Q)

/-- Distinct orientation-link evidence can supply the older orientation component
surface. -/
theorem DAGHasOrientationLinkSurface.to_orientation_component
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {Q : CausalSupportCut V}
    (h : DAGHasOrientationLinkSurface Λ Q) :
    Nonempty (C.orientationEvidence Q) := by
  rcases h with ⟨l⟩
  exact ⟨Λ.orientationLinkRefinesComponent Q l⟩

/-- Qualitative profile for orientation-link overlap separated from the
support/frontier components. -/
structure DAGOrientationLinkOverlapProfile
    (Q₁ Q₂ : CausalSupportCut V) where
  orientationLinkOverlap : Prop
  independentOfSupportFrontier : Prop

end DAGOrientationLinkSurface

section GraphOrientationLinkSurface

/-- Extra orientation-link evidence for a graph support cut, separated from the
older generic component context. -/
structure GraphOrientationLinkSurfaceContext
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    (C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω) where
  orientationLinkEvidence : GraphSupportCut G → Type*
  orientationLinkRefinesComponent :
    ∀ Q, orientationLinkEvidence Q → C.orientationEvidence Q

/-- A graph cut has the distinct orientation-link surface when link evidence is
inhabited. -/
def GraphHasOrientationLinkSurface
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    (Λ : GraphOrientationLinkSurfaceContext C)
    (Q : GraphSupportCut G) : Prop :=
  Nonempty (Λ.orientationLinkEvidence Q)

/-- Distinct graph orientation-link evidence supplies the older orientation
component surface. -/
theorem GraphHasOrientationLinkSurface.to_orientation_component
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {Q : GraphSupportCut G}
    (h : GraphHasOrientationLinkSurface Λ Q) :
    Nonempty (C.orientationEvidence Q) := by
  rcases h with ⟨l⟩
  exact ⟨Λ.orientationLinkRefinesComponent Q l⟩

/-- Qualitative graph profile for orientation-link overlap separated from
support/frontier components. -/
structure GraphOrientationLinkOverlapProfile
    {G : _root_.ActualizationGraph} (Q₁ Q₂ : GraphSupportCut G) where
  orientationLinkOverlap : Prop
  independentOfSupportFrontier : Prop

end GraphOrientationLinkSurface

end RA
