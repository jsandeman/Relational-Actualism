import RA_MotifPerGraphOrientationWitness

/-!
# RA_MotifConcreteGraphOrientationWitness

A conservative Lean-facing bridge for v1.5 concrete-graph orientation-link
witness evidence.

The v1.4 module `RA_MotifPerGraphOrientationWitness` introduced an abstract
`DAGPerGraphOrientationWitnessContext` whose `perGraphOrientationEvidence`
field was Type-valued and opaque. v1.5 adds a concrete edge-pair-sign
instantiation: a witness of the form (parent, child, sign, memberIndex) keyed
by an actual graph instance.

This file deliberately does NOT assert any numerical orientation-rescue law,
probability, or BDG-LLC derivation. It only states that concrete edge-pair-sign
evidence packages as the v1.4 per-graph witness type, which then refines the
v1.3 native catalog and the v1.2 orientation-link surface and the v1.0 generic
orientation component.
-/

namespace RA

section DAGConcreteEdgePairSign

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Concrete edge-pair-sign witness data for a DAG support cut.

Each piece of evidence is parameterised by a vertex pair `(parent, child)`,
a sign `Bool`, and a member index. The refinement morphism `concreteRefinesPerGraph`
shows that this concrete evidence supplies the abstract per-graph orientation
evidence already declared in `DAGPerGraphOrientationWitnessContext`. -/
structure DAGConcreteEdgePairSignContext
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    (P : DAGPerGraphOrientationWitnessContext K) where
  concreteEdgePairSignEvidence :
    P.graphInstance → ∀ Q : CausalSupportCut V, P.memberIndex Q → Type*
  concreteRefinesPerGraph :
    ∀ g Q i, concreteEdgePairSignEvidence g Q i → P.perGraphOrientationEvidence g Q i
  /-- Documentary obligation: the concrete evidence carries actual edge-pair
  data (parent, child, sign) drawn from the underlying graph topology, not
  abstract token strings. -/
  usesGraphTopologyEdges : Prop

/-- A cut on a graph instance has concrete edge-pair-sign witness evidence
when the witness type is inhabited for some member. -/
def DAGHasConcreteEdgePairSignWitness
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {P : DAGPerGraphOrientationWitnessContext K}
    (E : DAGConcreteEdgePairSignContext P)
    (g : P.graphInstance) (Q : CausalSupportCut V) : Prop :=
  ∃ i : P.memberIndex Q, Nonempty (E.concreteEdgePairSignEvidence g Q i)

/-- Concrete edge-pair-sign evidence refines the v1.4 per-graph orientation
witness. -/
theorem DAGHasConcreteEdgePairSignWitness.to_per_graph
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {P : DAGPerGraphOrientationWitnessContext K}
    {E : DAGConcreteEdgePairSignContext P}
    {g : P.graphInstance} {Q : CausalSupportCut V}
    (h : DAGHasConcreteEdgePairSignWitness E g Q) :
    DAGHasPerGraphOrientationWitness P g Q := by
  rcases h with ⟨i, hi⟩
  rcases hi with ⟨e⟩
  exact ⟨i, ⟨E.concreteRefinesPerGraph g Q i e⟩⟩

/-- Therefore concrete edge-pair-sign evidence also refines the v1.3 native
catalog evidence. -/
theorem DAGHasConcreteEdgePairSignWitness.to_native_catalog
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {P : DAGPerGraphOrientationWitnessContext K}
    {E : DAGConcreteEdgePairSignContext P}
    {g : P.graphInstance} {Q : CausalSupportCut V}
    (h : DAGHasConcreteEdgePairSignWitness E g Q) :
    DAGHasNativeOrientationLinkCatalog K Q := by
  exact DAGHasPerGraphOrientationWitness.to_native_catalog
    (DAGHasConcreteEdgePairSignWitness.to_per_graph h)

/-- And refines the v1.2 abstract orientation-link surface. -/
theorem DAGHasConcreteEdgePairSignWitness.to_orientation_link_surface
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ}
    {C : DAGNativeCertificateComponentContext Ω}
    {Λ : DAGOrientationLinkSurfaceContext C}
    {K : DAGNativeOrientationLinkCatalogContext Λ}
    {P : DAGPerGraphOrientationWitnessContext K}
    {E : DAGConcreteEdgePairSignContext P}
    {g : P.graphInstance} {Q : CausalSupportCut V}
    (h : DAGHasConcreteEdgePairSignWitness E g Q) :
    DAGHasOrientationLinkSurface Λ Q := by
  exact DAGHasNativeOrientationLinkCatalog.to_orientation_link_surface
    (DAGHasConcreteEdgePairSignWitness.to_native_catalog h)

/-- Qualitative DAG profile for concrete edge-pair-sign overlap. -/
structure DAGConcreteEdgePairSignOverlapProfile
    (Q₁ Q₂ : CausalSupportCut V) where
  edgePairSignOverlap : Prop
  topologyDerived : Prop
  refinesPerGraphOverlap : Prop

end DAGConcreteEdgePairSign

section GraphConcreteEdgePairSign

/-- Concrete edge-pair-sign witness data for a graph support cut (graph layer
parallel to the DAG version). -/
structure GraphConcreteEdgePairSignContext
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    (P : GraphPerGraphOrientationWitnessContext K) where
  concreteEdgePairSignEvidence :
    P.graphInstance → ∀ Q : GraphSupportCut G, P.memberIndex Q → Type*
  concreteRefinesPerGraph :
    ∀ g Q i, concreteEdgePairSignEvidence g Q i → P.perGraphOrientationEvidence g Q i
  usesGraphTopologyEdges : Prop

/-- A graph cut has concrete edge-pair-sign witness evidence when inhabited. -/
def GraphHasConcreteEdgePairSignWitness
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {P : GraphPerGraphOrientationWitnessContext K}
    (E : GraphConcreteEdgePairSignContext P)
    (g : P.graphInstance) (Q : GraphSupportCut G) : Prop :=
  ∃ i : P.memberIndex Q, Nonempty (E.concreteEdgePairSignEvidence g Q i)

/-- Graph concrete edge-pair-sign refines per-graph evidence. -/
theorem GraphHasConcreteEdgePairSignWitness.to_per_graph
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {P : GraphPerGraphOrientationWitnessContext K}
    {E : GraphConcreteEdgePairSignContext P}
    {g : P.graphInstance} {Q : GraphSupportCut G}
    (h : GraphHasConcreteEdgePairSignWitness E g Q) :
    GraphHasPerGraphOrientationWitness P g Q := by
  rcases h with ⟨i, hi⟩
  rcases hi with ⟨e⟩
  exact ⟨i, ⟨E.concreteRefinesPerGraph g Q i e⟩⟩

/-- And therefore refines the native catalog. -/
theorem GraphHasConcreteEdgePairSignWitness.to_native_catalog
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ}
    {C : GraphNativeCertificateComponentContext Ω}
    {Λ : GraphOrientationLinkSurfaceContext C}
    {K : GraphNativeOrientationLinkCatalogContext Λ}
    {P : GraphPerGraphOrientationWitnessContext K}
    {E : GraphConcreteEdgePairSignContext P}
    {g : P.graphInstance} {Q : GraphSupportCut G}
    (h : GraphHasConcreteEdgePairSignWitness E g Q) :
    GraphHasNativeOrientationLinkCatalog K Q := by
  exact GraphHasPerGraphOrientationWitness.to_native_catalog
    (GraphHasConcreteEdgePairSignWitness.to_per_graph h)

/-- Qualitative graph profile for concrete edge-pair-sign overlap. -/
structure GraphConcreteEdgePairSignOverlapProfile
    {G : _root_.ActualizationGraph} (Q₁ Q₂ : GraphSupportCut G) where
  edgePairSignOverlap : Prop
  topologyDerived : Prop
  refinesPerGraphOverlap : Prop

end GraphConcreteEdgePairSign

end RA
