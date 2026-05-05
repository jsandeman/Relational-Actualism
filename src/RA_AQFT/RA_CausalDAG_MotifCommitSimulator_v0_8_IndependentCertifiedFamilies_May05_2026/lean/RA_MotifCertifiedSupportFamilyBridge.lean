import RA_MotifSupportFamilyMonotonicity

/-!
# RA_MotifCertifiedSupportFamilyBridge

Certificate-family bridge for RA support-cut families.

`RA_MotifSupportFamilyBridge` introduced support-cut families: a motif can be
ready when some member support cut is ready.  The v0.8 simulator studies the
next distinction: support-route redundancy is not the same as certification
redundancy.  A family can only rescue ledger/orientation certification failure
when alternative member cuts carry member-distinct certificates, or some
RA-native equivalent thereof.

This module keeps that layer abstract.  It does not assert a probability law,
and it does not import external reliability, voting, or inherited-theory
apparatus.  The fields below are certificate predicates and soundness conditions
that downstream BDG-LLC / frontier / orientation / ledger modules may refine.
-/

namespace RA

/-! ## DAG certificate-family layer -/

section O01CertifiedFamilyLayer

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- A certificate context for member cuts of a DAG support-cut family.

`certifies Q` means that this family-level certificate layer certifies the
member support cut `Q`.  Soundness requires every certified cut to belong to the
family and to be accepted by the ordinary motif-commit support relation.

The field `member_distinct` is deliberately abstract: it marks the intended
case where member certificates are not merely one shared parent certificate.
A downstream native certificate module may replace this propositional marker
with concrete graph-orientation / ledger witness data. -/
structure DAGFamilyCertificateContext
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V) where
  certifies : CausalSupportCut V → Prop
  sound : ∀ Q, certifies Q → F.cuts Q ∧ Γ.supports M Q
  member_distinct : Prop

/-- A family is independently certified-ready when some member cut is certified
by the family certificate context and causally ready at the site. -/
def DAGIndependentCertifiedFamilyReadyAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F) (x : V) : Prop :=
  ∃ Q, Ξ.certifies Q ∧ DAGReadyAt G Q x

/-- If one certified member cut is ready, the independent certified-family
predicate holds. -/
theorem DAGIndependentCertifiedFamilyReadyAt.of_member
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F} {x : V}
    {Q : CausalSupportCut V}
    (hcert : Ξ.certifies Q) (hready : DAGReadyAt G Q x) :
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x :=
  ⟨Q, hcert, hready⟩

/-- Independent certified-family readiness implies the ordinary certified-family
readiness predicate from the support-family bridge. -/
theorem DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F} {x : V}
    (h : DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    DAGCertifiedFamilyReadyAt G Γ M F x := by
  rcases h with ⟨Q, hcert, hready⟩
  have hs := Ξ.sound Q hcert
  exact ⟨Q, hs.1, hs.2, hready⟩

/-- Independent certified-family readiness implies any-cut family readiness. -/
theorem DAGIndependentCertifiedFamilyReadyAt.to_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F} {x : V}
    (h : DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    DAGFamilyReadyAt G F x := by
  have hc := DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready h
  rcases hc with ⟨Q, hcut, _hsupports, hready⟩
  exact ⟨Q, hcut, hready⟩

/-- If every cut certified by one certificate context is also certified by a
larger certificate context over the same support family, readiness propagates. -/
theorem DAGIndependentCertifiedFamilyReadyAt.mono_certificates
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V}
    {Ξ Ξ' : DAGFamilyCertificateContext G Γ M F} {x : V}
    (hinc : ∀ Q, Ξ.certifies Q → Ξ'.certifies Q)
    (h : DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ' x := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, hinc Q hcert, hready⟩

/-- Family readiness induced by independent certificates is future-monotone. -/
theorem DAGIndependentCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V)
    (Ξ : DAGFamilyCertificateContext G Γ M F) {x z : V}
    (h : DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x)
    (hxz : G.precedes x z) :
    DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ z := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, hcert, DAGReadyAt.future_mono G Q hready hxz⟩

end O01CertifiedFamilyLayer

/-! ## Graph certificate-family layer -/

section GraphCertifiedFamilyLayer

/-- A concrete graph certificate context for member cuts of a graph support-cut
family. -/
structure GraphFamilyCertificateContext
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G) where
  certifies : GraphSupportCut G → Prop
  sound : ∀ Q, certifies Q → F.cuts Q ∧ Γ.supports M Q
  member_distinct : Prop

/-- Concrete graph independent certified-family readiness. -/
def GraphIndependentCertifiedFamilyReadyAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F) (x : GraphVertex G) : Prop :=
  ∃ Q, Ξ.certifies Q ∧ GraphReadyAt G Q x

/-- A certified ready graph member witnesses independent certified-family
readiness. -/
theorem GraphIndependentCertifiedFamilyReadyAt.of_member
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F} {x : GraphVertex G}
    {Q : GraphSupportCut G}
    (hcert : Ξ.certifies Q) (hready : GraphReadyAt G Q x) :
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x :=
  ⟨Q, hcert, hready⟩

/-- Independent graph certified-family readiness implies ordinary graph
certified-family readiness. -/
theorem GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F} {x : GraphVertex G}
    (h : GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    GraphCertifiedFamilyReadyAt G Γ M F x := by
  rcases h with ⟨Q, hcert, hready⟩
  have hs := Ξ.sound Q hcert
  exact ⟨Q, hs.1, hs.2, hready⟩

/-- Independent graph certified-family readiness implies any-cut graph family
readiness. -/
theorem GraphIndependentCertifiedFamilyReadyAt.to_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F} {x : GraphVertex G}
    (h : GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    GraphFamilyReadyAt G F x := by
  have hc := GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready h
  rcases hc with ⟨Q, hcut, _hsupports, hready⟩
  exact ⟨Q, hcut, hready⟩

/-- Graph independent certified-family readiness is monotone under certificate
context enlargement. -/
theorem GraphIndependentCertifiedFamilyReadyAt.mono_certificates
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {Ξ Ξ' : GraphFamilyCertificateContext G Γ M F} {x : GraphVertex G}
    (hinc : ∀ Q, Ξ.certifies Q → Ξ'.certifies Q)
    (h : GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x) :
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ' x := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, hinc Q hcert, hready⟩

/-- Graph independent certified-family readiness is future-monotone along
reachability. -/
theorem GraphIndependentCertifiedFamilyReadyAt.future_mono
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (Ξ : GraphFamilyCertificateContext G Γ M F) {x z : GraphVertex G}
    (h : GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ x)
    (hxz : Reachable G x z) :
    GraphIndependentCertifiedFamilyReadyAt G Γ M F Ξ z := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, hcert, GraphReadyAt.future_mono G Q hready hxz⟩

end GraphCertifiedFamilyLayer

end RA
