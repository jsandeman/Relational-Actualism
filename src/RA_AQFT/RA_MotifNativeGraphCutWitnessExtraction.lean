import RA_MotifComparisonDomainValidity
import RA_GraphOrientationClosure

/-!
# RA_MotifNativeGraphCutWitnessExtraction

Track B.1: graph/cut-local orientation witness extraction surface.

This bridge is intentionally conservative.  It does not assert a probability
law, a rescue-rate theorem, or an orientation-specific certification-rescue
claim.  It provides a typed place to attach per-graph / per-support-cut
orientation-link witness evidence to the existing graph-orientation closure
surface.

The intended simulator correspondence is:

```text
ActualizationGraph + support-family member cut
  -> graph/cut-local oriented frontier links
  -> sign source induced by graph-orientation closure certificate
  -> seven-value N1 ledger surface
```

The hard future theorem is to construct `memberLink` and the closure certificate
from concrete RA graph/frontier/orientation data.  This file only states the
interface and refinement theorems once such data is supplied.
-/

namespace RA

/-- A graph/cut-local orientation witness for one support-family member.

`memberLink` identifies the oriented frontier links used by this member's
orientation witness.  The `link_cut_local` field ensures that supplied links are
anchored to the support cut rather than arbitrary row labels.  The
`graph_cut_derived` and `no_member_index_labels` fields are methodological
witnesses: downstream extractors should prove/record that links are derived from
graph/cut structure and not from arbitrary family-member ordering.
-/
structure GraphCutOrientationWitness
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  supportCut : GraphSupportCut G
  closureCert : GraphOrientationClosureCertificate P
  frame : OrientedN1ThreeFrame P
  local_conserved : Prop
  memberLink : OrientedFrontierLink P → Prop
  link_cut_local : ∀ l, memberLink l → l.src ∈ supportCut.support ∨ l.dst ∈ supportCut.support
  graph_cut_derived : Prop
  graph_cut_derived_proof : graph_cut_derived
  no_member_index_labels : Prop
  no_member_index_labels_proof : no_member_index_labels

/-- A graph/cut witness induces the deterministic sign source supplied by its
orientation-closure certificate. -/
def signSourceOfGraphCutOrientationWitness
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W : GraphCutOrientationWitness P) : IncidenceSignSource P :=
  signSourceOfGraphOrientationClosureCertificate W.closureCert

/-- Evaluation rule for graph/cut witness signs. -/
theorem signSourceOfGraphCutOrientationWitness_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W : GraphCutOrientationWitness P) (l : OrientedFrontierLink P) :
    (signSourceOfGraphCutOrientationWitness W).signOf l =
      (W.closureCert.orientationData.polarityBetween l.src l.dst).toSign :=
  signSourceOfGraphOrientationClosureCertificate_eval W.closureCert l

/-- A graph/cut-local witness inherits the seven-value N1 ledger surface from
its orientation-closure certificate and supplied three-frame. -/
theorem graphCutOrientationWitness_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W : GraphCutOrientationWitness P) :
    SevenCharge
      (ledgerOfGraphOrientedBoundary
        (graphOrientedBoundaryOfClosureCertificate W.closureCert W.frame W.local_conserved)).qN1 :=
  ledgerOfGraphOrientationClosureCertificate_qN1_seven
    W.closureCert W.frame W.local_conserved

/-- Methodological accessor: the witness is graph/cut-derived. -/
theorem GraphCutOrientationWitness.graph_cut_derived_cert
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W : GraphCutOrientationWitness P) : W.graph_cut_derived :=
  W.graph_cut_derived_proof

/-- Methodological accessor: the witness does not use arbitrary member-index labels. -/
theorem GraphCutOrientationWitness.no_member_index_labels_cert
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W : GraphCutOrientationWitness P) : W.no_member_index_labels :=
  W.no_member_index_labels_proof

/-- An overlap profile for two graph/cut-local orientation witnesses.

The actual numerical overlap measure remains simulator-side.  Lean records the
qualitative comparison surface only. -/
structure GraphCutOrientationWitnessOverlapProfile
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (W₁ W₂ : GraphCutOrientationWitness P) where
  low_overlap : Prop
  medium_overlap : Prop
  high_overlap : Prop
  same_graph_cut_domain : Prop
  same_graph_cut_domain_proof : same_graph_cut_domain
  fixed_bin_definition : Prop
  fixed_bin_definition_proof : fixed_bin_definition

/-- A high-overlap profile records that the two witnesses live in the same
comparison domain.  This is a structural guardrail, not a rescue theorem. -/
theorem GraphCutOrientationWitnessOverlapProfile.same_domain_of_high
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {W₁ W₂ : GraphCutOrientationWitness P}
    (Ω : GraphCutOrientationWitnessOverlapProfile W₁ W₂)
    (_h : Ω.high_overlap) : Ω.same_graph_cut_domain :=
  Ω.same_graph_cut_domain_proof

/-- Fixed-bin discipline accessor for witness-overlap comparisons. -/
theorem GraphCutOrientationWitnessOverlapProfile.fixed_bins
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {W₁ W₂ : GraphCutOrientationWitness P}
    (Ω : GraphCutOrientationWitnessOverlapProfile W₁ W₂) : Ω.fixed_bin_definition :=
  Ω.fixed_bin_definition_proof

end RA
