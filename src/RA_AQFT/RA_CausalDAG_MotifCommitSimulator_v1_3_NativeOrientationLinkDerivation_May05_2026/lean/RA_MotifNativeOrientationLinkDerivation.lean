import RA_MotifOrientationLinkSurface
import RA_CausalOrientation_Core
import RA_D1_NativeLedgerOrientation
import RA_D1_NativeClosure

/-!
# RA_MotifNativeOrientationLinkDerivation

A conservative Lean-facing bridge for v1.3 native orientation-link derivation.

`RA_MotifOrientationLinkSurface` introduced an abstract distinct orientation-link
surface.  This module adds a native-orientation catalog layer above it: evidence
from native orientation / ledger / closure modules may refine the abstract
orientation-link surface.

This file deliberately does **not** assert a numerical rescue law or a final
Nature-facing orientation-overlap law.  It only states that native
orientation-catalog evidence can be packaged as orientation-link evidence, which
then refines the generic orientation component surface already present in the
native-certificate component bridge.
-/

namespace RA

section DAGNativeOrientationLinkDerivation

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Native orientation catalog evidence refining the abstract DAG
orientation-link surface.

The fields `usesCausalOrientationCore`, `usesNativeLedgerOrientation`, and
`usesNativeClosure` are qualitative obligations for downstream instantiations;
they keep the bridge tied to the native theorem surfaces without pretending to
extract a numerical overlap law inside Lean. -/
structure DAGNativeOrientationLinkCatalogContext
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    (Λ : DAGOrientationLinkSurfaceContext C) where
  nativeOrientationEvidence : CausalSupportCut V → Type*
  nativeEvidenceRefinesLink : ∀ Q, nativeOrientationEvidence Q → Λ.orientationLinkEvidence Q
  usesCausalOrientationCore : Prop
  usesNativeLedgerOrientation : Prop
  usesNativeClosure : Prop

/-- A cut has a native orientation-link catalog surface when native catalog
evidence is inhabited. -/
def DAGHasNativeOrientationLinkCatalog
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    (K : DAGNativeOrientationLinkCatalogContext Λ)
    (Q : CausalSupportCut V) : Prop :=
  Nonempty (K.nativeOrientationEvidence Q)

/-- Native catalog evidence refines the v1.2 abstract orientation-link surface. -/
theorem DAGHasNativeOrientationLinkCatalog.to_orientation_link_surface
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {Q : CausalSupportCut V}
    (h : DAGHasNativeOrientationLinkCatalog K Q) :
    DAGHasOrientationLinkSurface Λ Q := by
  rcases h with ⟨e⟩
  exact ⟨K.nativeEvidenceRefinesLink Q e⟩

/-- Native catalog evidence therefore also supplies the generic orientation
component surface. -/
theorem DAGHasNativeOrientationLinkCatalog.to_orientation_component
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {Q : CausalSupportCut V}
    (h : DAGHasNativeOrientationLinkCatalog K Q) :
    Nonempty (C.orientationEvidence Q) := by
  exact DAGHasOrientationLinkSurface.to_orientation_component
    (DAGHasNativeOrientationLinkCatalog.to_orientation_link_surface h)

/-- Qualitative DAG profile for native-orientation-catalog overlap. -/
structure DAGNativeOrientationCatalogOverlapProfile
    (Q₁ Q₂ : CausalSupportCut V) where
  nativeCatalogOverlap : Prop
  separatesFromSupportFrontier : Prop
  refinesOrientationLinkOverlap : Prop

end DAGNativeOrientationLinkDerivation

section GraphNativeOrientationLinkDerivation

/-- Native orientation catalog evidence refining the abstract graph
orientation-link surface. -/
structure GraphNativeOrientationLinkCatalogContext
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    (Λ : GraphOrientationLinkSurfaceContext C) where
  nativeOrientationEvidence : GraphSupportCut G → Type*
  nativeEvidenceRefinesLink : ∀ Q, nativeOrientationEvidence Q → Λ.orientationLinkEvidence Q
  usesCausalOrientationCore : Prop
  usesNativeLedgerOrientation : Prop
  usesNativeClosure : Prop

/-- A graph cut has a native orientation-link catalog surface when native catalog
evidence is inhabited. -/
def GraphHasNativeOrientationLinkCatalog
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    (K : GraphNativeOrientationLinkCatalogContext Λ)
    (Q : GraphSupportCut G) : Prop :=
  Nonempty (K.nativeOrientationEvidence Q)

/-- Native catalog evidence refines the v1.2 graph orientation-link surface. -/
theorem GraphHasNativeOrientationLinkCatalog.to_orientation_link_surface
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {Q : GraphSupportCut G}
    (h : GraphHasNativeOrientationLinkCatalog K Q) :
    GraphHasOrientationLinkSurface Λ Q := by
  rcases h with ⟨e⟩
  exact ⟨K.nativeEvidenceRefinesLink Q e⟩

/-- Native graph catalog evidence therefore also supplies the generic orientation
component surface. -/
theorem GraphHasNativeOrientationLinkCatalog.to_orientation_component
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext G Γ M F Ξ Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {Q : GraphSupportCut G}
    (h : GraphHasNativeOrientationLinkCatalog K Q) :
    Nonempty (C.orientationEvidence Q) := by
  exact GraphHasOrientationLinkSurface.to_orientation_component
    (GraphHasNativeOrientationLinkCatalog.to_orientation_link_surface h)

/-- Qualitative graph profile for native-orientation-catalog overlap. -/
structure GraphNativeOrientationCatalogOverlapProfile
    {G : _root_.ActualizationGraph} (Q₁ Q₂ : GraphSupportCut G) where
  nativeCatalogOverlap : Prop
  separatesFromSupportFrontier : Prop
  refinesOrientationLinkOverlap : Prop

end GraphNativeOrientationLinkDerivation

end RA
