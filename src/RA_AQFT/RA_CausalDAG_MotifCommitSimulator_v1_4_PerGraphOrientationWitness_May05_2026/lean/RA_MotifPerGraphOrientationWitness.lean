import RA_MotifNativeOrientationLinkDerivation

/-!
# RA_MotifPerGraphOrientationWitness

A conservative Lean-facing bridge for v1.4 per-graph orientation-link witness
extraction.

Earlier layers introduced an abstract orientation-link surface and then a native
orientation theorem/catalog surface.  This module adds a still-abstract but more
localized vocabulary: orientation-link evidence may be indexed by a graph
instance and by a support-family member.  Such per-graph/member evidence refines
the native orientation catalog surface, which in turn refines the generic
orientation component surface.

The module deliberately does **not** define a numerical overlap metric or a
rescue law.  It is a type-safe refinement surface for downstream graph/cut
extractors.
-/

namespace RA

section DAGPerGraphOrientationWitness

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Per-graph/member orientation-link witness data refining the native catalog
orientation surface.  `graphInstance` and `memberIndex` remain abstract so that
future extractors can choose their concrete graph/cut indexing scheme. -/
structure DAGPerGraphOrientationWitnessContext
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    (K : DAGNativeOrientationLinkCatalogContext Λ) where
  graphInstance : Type*
  memberIndex : CausalSupportCut V → Type*
  perGraphOrientationEvidence :
    graphInstance → (Q : CausalSupportCut V) → memberIndex Q → Type*
  refinesNativeCatalog :
    ∀ g Q i, perGraphOrientationEvidence g Q i → K.nativeOrientationEvidence Q

/-- A cut has per-graph/member orientation-link witness evidence when some
member witness is inhabited for the given graph instance. -/
def DAGHasPerGraphOrientationWitness
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    (Π : DAGPerGraphOrientationWitnessContext K)
    (g : Π.graphInstance) (Q : CausalSupportCut V) : Prop :=
  ∃ i : Π.memberIndex Q, Nonempty (Π.perGraphOrientationEvidence g Q i)

/-- Per-graph/member orientation evidence refines native-catalog evidence. -/
theorem DAGHasPerGraphOrientationWitness.to_native_catalog
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {Π : DAGPerGraphOrientationWitnessContext K}
    {g : Π.graphInstance} {Q : CausalSupportCut V}
    (h : DAGHasPerGraphOrientationWitness Π g Q) :
    DAGHasNativeOrientationLinkCatalog K Q := by
  rcases h with ⟨i, hi⟩
  rcases hi with ⟨e⟩
  exact ⟨Π.refinesNativeCatalog g Q i e⟩

/-- Per-graph/member orientation evidence refines the abstract orientation-link
surface. -/
theorem DAGHasPerGraphOrientationWitness.to_orientation_link_surface
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {Π : DAGPerGraphOrientationWitnessContext K}
    {g : Π.graphInstance} {Q : CausalSupportCut V}
    (h : DAGHasPerGraphOrientationWitness Π g Q) :
    DAGHasOrientationLinkSurface Λ Q := by
  exact DAGHasNativeOrientationLinkCatalog.to_orientation_link_surface
    (DAGHasPerGraphOrientationWitness.to_native_catalog h)

/-- Qualitative overlap profile for two per-graph/member orientation witnesses. -/
structure DAGPerGraphOrientationWitnessOverlapProfile
    (Q₁ Q₂ : CausalSupportCut V) where
  perGraphOrientationOverlap : Prop
  separatesFromSupportFrontier : Prop
  refinesNativeCatalogOverlap : Prop

end DAGPerGraphOrientationWitness

section GraphPerGraphOrientationWitness

/-- Per-graph/member orientation-link witness data refining the native catalog
orientation surface for graph-native support cuts. -/
structure GraphPerGraphOrientationWitnessContext
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    (K : GraphNativeOrientationLinkCatalogContext Λ) where
  graphInstance : Type*
  memberIndex : GraphSupportCut G → Type*
  perGraphOrientationEvidence :
    graphInstance → (Q : GraphSupportCut G) → memberIndex Q → Type*
  refinesNativeCatalog :
    ∀ g Q i, perGraphOrientationEvidence g Q i → K.nativeOrientationEvidence Q

/-- A graph support cut has per-graph/member orientation-link evidence when some
member witness is inhabited for the given graph instance. -/
def GraphHasPerGraphOrientationWitness
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    (Π : GraphPerGraphOrientationWitnessContext K)
    (g : Π.graphInstance) (Q : GraphSupportCut G) : Prop :=
  ∃ i : Π.memberIndex Q, Nonempty (Π.perGraphOrientationEvidence g Q i)

/-- Per-graph/member graph orientation evidence refines native-catalog evidence. -/
theorem GraphHasPerGraphOrientationWitness.to_native_catalog
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {Π : GraphPerGraphOrientationWitnessContext K}
    {g : Π.graphInstance} {Q : GraphSupportCut G}
    (h : GraphHasPerGraphOrientationWitness Π g Q) :
    GraphHasNativeOrientationLinkCatalog K Q := by
  rcases h with ⟨i, hi⟩
  rcases hi with ⟨e⟩
  exact ⟨Π.refinesNativeCatalog g Q i e⟩

/-- Per-graph/member graph orientation evidence refines the orientation-link surface. -/
theorem GraphHasPerGraphOrientationWitness.to_orientation_link_surface
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {Π : GraphPerGraphOrientationWitnessContext K}
    {g : Π.graphInstance} {Q : GraphSupportCut G}
    (h : GraphHasPerGraphOrientationWitness Π g Q) :
    GraphHasOrientationLinkSurface Λ Q := by
  exact GraphHasNativeOrientationLinkCatalog.to_orientation_link_surface
    (GraphHasPerGraphOrientationWitness.to_native_catalog h)

/-- Qualitative graph-native overlap profile for two per-graph/member witnesses. -/
structure GraphPerGraphOrientationWitnessOverlapProfile
    {G : _root_.ActualizationGraph} (Q₁ Q₂ : GraphSupportCut G) where
  perGraphOrientationOverlap : Prop
  separatesFromSupportFrontier : Prop
  refinesNativeCatalogOverlap : Prop

end GraphPerGraphOrientationWitness

end RA
