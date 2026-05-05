import RA_MotifCertifiedSupportFamilyBridge

/-!
# RA_MotifNativeCertificateOverlapBridge

Abstract native-overlap bridge for certified support-cut families.

`RA_MotifCertifiedSupportFamilyBridge` made member-certified support families
explicit.  The v0.9 simulator asks how certificate correlation might be induced
by native overlap among member witnesses rather than supplied as an external
parameter.

This module keeps the overlap layer qualitative.  It introduces witness-context
fields and overlap relations, but does not assert a probability law, a numerical
metric, or any empirical claim.  Downstream BDG-LLC / native-ledger / orientation
modules may refine `witness` and `overlaps` into concrete graph evidence.
-/

namespace RA

/-! ## DAG native certificate-overlap layer -/

section O01NativeOverlapLayer

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Native certificate-witness context for a DAG support-cut family.

`witness Q` is Type-valued so later modules can retain data rather than only a
proposition.  `certifies_of_witness` connects native witness data back to the
abstract certificate context from v0.8.  `overlaps` is an abstract relation over
member cuts; the simulator instantiates it with support/frontier/orientation /
ledger/causal-overlap diagnostics, but this Lean bridge does not fix a metric. -/
structure DAGNativeCertificateOverlapContext
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F) where
  witness : CausalSupportCut V → Type*
  certifies_of_witness : ∀ Q, witness Q → Ξ.certifies Q
  overlaps : CausalSupportCut V → CausalSupportCut V → Prop
  overlaps_refl : ∀ Q, F.cuts Q → overlaps Q Q
  member_distinct_from_low_overlap : Prop

/-- A cut is natively witnessed when its Type-valued witness data is inhabited. -/
def DAGNativelyWitnessed
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ)
    (Q : CausalSupportCut V) : Prop :=
  Nonempty (Ω.witness Q)

/-- Native-overlap certified-family readiness: some member has native witness data
and is ready at the site. -/
def DAGNativeOverlapCertifiedFamilyReadyAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ) (x : V) : Prop :=
  ∃ Q, DAGNativelyWitnessed Ω Q ∧ DAGReadyAt G Q x

/-- A native member witness gives native-overlap certified readiness. -/
theorem DAGNativeOverlapCertifiedFamilyReadyAt.of_member
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ} {x : V}
    {Q : CausalSupportCut V}
    (hwit : DAGNativelyWitnessed Ω Q) (hready : DAGReadyAt G Q x) :
    DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x :=
  ⟨Q, hwit, hready⟩

/-- Native-overlap certified readiness refines the v0.8 independent certified
family readiness predicate. -/
theorem DAGNativeOverlapCertifiedFamilyReadyAt.to_independent_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ} {x : V}
    (h : DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x) :
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x := by
  rcases h with ⟨Q, hwit, hready⟩
  rcases hwit with ⟨w⟩
  exact ⟨Q, Ω.certifies_of_witness Q w, hready⟩

/-- Native-overlap certified readiness therefore implies ordinary certified-family
readiness. -/
theorem DAGNativeOverlapCertifiedFamilyReadyAt.to_certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ} {x : V}
    (h : DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x) :
    DAGCertifiedFamilyReadyAt G Γ M F x := by
  exact DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready
    (DAGNativeOverlapCertifiedFamilyReadyAt.to_independent_ready h)

/-- Native-overlap certified readiness is future-monotone. -/
theorem DAGNativeOverlapCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Ω : DAGNativeCertificateOverlapContext G Γ M F Ξ) {x z : V}
    (h : DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x)
    (hxz : G.precedes x z) :
    DAGNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω z := by
  rcases h with ⟨Q, hwit, hready⟩
  exact ⟨Q, hwit, DAGReadyAt.future_mono G Q hready hxz⟩

end O01NativeOverlapLayer

/-! ## Graph native certificate-overlap layer -/

section GraphNativeOverlapLayer

/-- Graph-native certificate-overlap context for support-cut families. -/
structure GraphNativeCertificateOverlapContext
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F) where
  witness : GraphSupportCut G → Type*
  certifies_of_witness : ∀ Q, witness Q → Ξ.certifies Q
  overlaps : GraphSupportCut G → GraphSupportCut G → Prop
  overlaps_refl : ∀ Q, F.cuts Q → overlaps Q Q
  member_distinct_from_low_overlap : Prop

/-- A graph support cut is natively witnessed when its witness type is inhabited. -/
def GraphNativelyWitnessed
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ)
    (Q : GraphSupportCut G) : Prop :=
  Nonempty (Ω.witness Q)

/-- Graph native-overlap certified-family readiness. -/
def GraphNativeOverlapCertifiedFamilyReadyAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ) (x : GraphVertex G) : Prop :=
  ∃ Q, GraphNativelyWitnessed Ω Q ∧ GraphReadyAt G Q x

/-- A graph native member witness gives native-overlap certified readiness. -/
theorem GraphNativeOverlapCertifiedFamilyReadyAt.of_member
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ} {x : GraphVertex G}
    {Q : GraphSupportCut G}
    (hwit : GraphNativelyWitnessed Ω Q) (hready : GraphReadyAt G Q x) :
    GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x :=
  ⟨Q, hwit, hready⟩

/-- Graph native-overlap certified readiness refines independent certified-family
readiness. -/
theorem GraphNativeOverlapCertifiedFamilyReadyAt.to_independent_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ} {x : GraphVertex G}
    (h : GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x) :
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x := by
  rcases h with ⟨Q, hwit, hready⟩
  rcases hwit with ⟨w⟩
  exact ⟨Q, Ω.certifies_of_witness Q w, hready⟩

/-- Graph native-overlap certified readiness implies ordinary graph certified-family
readiness. -/
theorem GraphNativeOverlapCertifiedFamilyReadyAt.to_certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ} {x : GraphVertex G}
    (h : GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x) :
    GraphCertifiedFamilyReadyAt G Γ M F x := by
  exact GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready
    (GraphNativeOverlapCertifiedFamilyReadyAt.to_independent_ready h)

/-- Graph native-overlap certified readiness is future-monotone along reachability. -/
theorem GraphNativeOverlapCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Ω : GraphNativeCertificateOverlapContext G Γ M F Ξ) {x z : GraphVertex G}
    (h : GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω x)
    (hxz : Reachable G x z) :
    GraphNativeOverlapCertifiedFamilyReadyAt G Γ M F Ξ Ω z := by
  rcases h with ⟨Q, hwit, hready⟩
  exact ⟨Q, hwit, GraphReadyAt.future_mono G Q hready hxz⟩

end GraphNativeOverlapLayer

end RA
