import RA_MotifSupportFamilyRescueTaxonomy

/-!
# RA_MotifComparisonDomainValidity

Track A.3 formal refinement for comparison-domain validity in support-family
rescue analysis.

The v0.7--v0.7.2 metric-repair sequence showed that simulator-side rescue
comparisons can become misleading when strict-parent, family-internal, and
family-targeted quantities are compared across different support-family domains.
`RA_MotifSupportFamilyRescueTaxonomy` then isolated the augmentation versus
replacement distinction.

This module adds an explicit formal surface for **valid comparison domains**.
It deliberately remains qualitative: it asserts no probability law, no rescue
rate, no numerical monotonicity theorem, and no orientation-specific rescue
claim.

A comparison is disciplined when the relevant targeting/exposure conditions are
aligned and when support-family/certificate domains are comparable in the
appropriate sense.  In particular, augmentation comparisons carry a stronger
certificate-preservation condition and can therefore reuse the existing
certified-family monotonicity theorem.
-/

namespace RA

/-! ## DAG comparison-domain validity -/

section O01ComparisonDomainValidity

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Certificate agreement on the overlap of two DAG support-family domains.  This
is the apples-to-apples certificate predicate for cuts that appear in both
families. -/
def DAGCertificateAgreementOnOverlap
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    (Ξ₁ : DAGFamilyCertificateContext G Γ M F₁)
    (Ξ₂ : DAGFamilyCertificateContext G Γ M F₂) : Prop :=
  ∀ Q, F₁.cuts Q → F₂.cuts Q → (Ξ₁.certifies Q ↔ Ξ₂.certifies Q)

/-- General validity predicate for comparing two DAG support-family domains.  The
first two arguments are intentionally abstract Prop-valued guardrails supplied by
the downstream analysis layer:

* `targetingAligned`: the same intervention/targeting domain is being compared;
* `exposureAligned`: the same readiness/certification exposure channel is being
  compared.

The remaining conjuncts require family comparability and certificate agreement
on the overlap of the two support-family domains. -/
def DAGValidFamilyComparison
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    (Ξ₁ : DAGFamilyCertificateContext G Γ M F₁)
    (Ξ₂ : DAGFamilyCertificateContext G Γ M F₂)
    (targetingAligned exposureAligned : Prop) : Prop :=
  targetingAligned ∧
  exposureAligned ∧
  DAGFamilyComparable F₁ F₂ ∧
  DAGCertificateAgreementOnOverlap Ξ₁ Ξ₂

/-- A stronger validity predicate for additive DAG-family augmentation.  This is
the formal Track A.3 surface for no-worse / rescue comparisons where the
comparison family contains the base family and preserves base-family certificate
witnesses. -/
def DAGValidAugmentationComparison
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    (Ξbase : DAGFamilyCertificateContext G Γ M Fbase)
    (Ξaug : DAGFamilyCertificateContext G Γ M Faug)
    (targetingAligned exposureAligned : Prop) : Prop :=
  targetingAligned ∧
  exposureAligned ∧
  DAGCertifiedFamilyAugments Ξbase Ξaug

/-- Replacement-style DAG comparisons are marked by family incomparability.  This
marker records that no inclusion/no-worse theorem follows without additional
hypotheses. -/
def DAGReplacementComparisonDomain
    (F₁ F₂ : DAGSupportCutFamily V) : Prop :=
  DAGFamilyIncomparable F₁ F₂

/-- General valid comparison exposes the targeting-alignment guardrail. -/
theorem DAGValidFamilyComparison.targeting_aligned
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    {Ξ₁ : DAGFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : DAGFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : DAGValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    targetingAligned :=
  h.1

/-- General valid comparison exposes the exposure-alignment guardrail. -/
theorem DAGValidFamilyComparison.exposure_aligned
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    {Ξ₁ : DAGFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : DAGFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : DAGValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    exposureAligned :=
  h.2.1

/-- General valid comparison exposes family comparability. -/
theorem DAGValidFamilyComparison.family_comparable
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    {Ξ₁ : DAGFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : DAGFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : DAGValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    DAGFamilyComparable F₁ F₂ :=
  h.2.2.1

/-- General valid comparison exposes certificate agreement on the overlapping
family domain. -/
theorem DAGValidFamilyComparison.certificate_agreement
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F₁ F₂ : DAGSupportCutFamily V}
    {Ξ₁ : DAGFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : DAGFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : DAGValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    DAGCertificateAgreementOnOverlap Ξ₁ Ξ₂ :=
  h.2.2.2

/-- Valid augmentation exposes the certified-family augmentation witness. -/
theorem DAGValidAugmentationComparison.certified_augmentation
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξbase : DAGFamilyCertificateContext G Γ M Fbase}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    (h : DAGValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned) :
    DAGCertifiedFamilyAugments Ξbase Ξaug :=
  h.2.2

/-- Valid additive comparison preserves family-internal resilience by the existing
certified-augmentation theorem. -/
theorem DAGValidAugmentationComparison.to_family_internal_resilience
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξbase : DAGFamilyCertificateContext G Γ M Fbase}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    {x : V}
    (hvalid : DAGValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned)
    (hres : DAGFamilyInternalResilienceAt G Γ M Fbase Ξbase x) :
    DAGFamilyInternalResilienceAt G Γ M Faug Ξaug x :=
  DAGFamilyInternalResilienceAt.mono_certified_augmentation
    hvalid.certified_augmentation hres

/-- Valid additive comparison plus parent failure produces the Track A.2
augmentation-rescue surface. -/
theorem DAGValidAugmentationComparison.to_augmentation_rescue
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξbase : DAGFamilyCertificateContext G Γ M Fbase}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    {Qparent : CausalSupportCut V} {x : V}
    (hvalid : DAGValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned)
    (hQ : Fbase.cuts Qparent)
    (hnot : ¬ DAGReadyAt G Qparent x)
    (hres : DAGFamilyInternalResilienceAt G Γ M Faug Ξaug x) :
    DAGFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x :=
  ⟨hvalid.certified_augmentation.1, hQ, hnot, hres⟩

/-- Replacement-domain marker exposes family incomparability. -/
theorem DAGReplacementComparisonDomain.incomparable
    {F₁ F₂ : DAGSupportCutFamily V}
    (h : DAGReplacementComparisonDomain F₁ F₂) :
    DAGFamilyIncomparable F₁ F₂ :=
  h

end O01ComparisonDomainValidity

/-! ## Concrete graph comparison-domain validity -/

section GraphComparisonDomainValidity

/-- Certificate agreement on the overlap of two graph support-family domains. -/
def GraphCertificateAgreementOnOverlap
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    (Ξ₁ : GraphFamilyCertificateContext G Γ M F₁)
    (Ξ₂ : GraphFamilyCertificateContext G Γ M F₂) : Prop :=
  ∀ Q, F₁.cuts Q → F₂.cuts Q → (Ξ₁.certifies Q ↔ Ξ₂.certifies Q)

/-- General validity predicate for comparing two graph support-family domains. -/
def GraphValidFamilyComparison
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    (Ξ₁ : GraphFamilyCertificateContext G Γ M F₁)
    (Ξ₂ : GraphFamilyCertificateContext G Γ M F₂)
    (targetingAligned exposureAligned : Prop) : Prop :=
  targetingAligned ∧
  exposureAligned ∧
  GraphFamilyComparable F₁ F₂ ∧
  GraphCertificateAgreementOnOverlap Ξ₁ Ξ₂

/-- Stronger validity predicate for additive graph-family augmentation. -/
def GraphValidAugmentationComparison
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    (Ξbase : GraphFamilyCertificateContext G Γ M Fbase)
    (Ξaug : GraphFamilyCertificateContext G Γ M Faug)
    (targetingAligned exposureAligned : Prop) : Prop :=
  targetingAligned ∧
  exposureAligned ∧
  GraphCertifiedFamilyAugments Ξbase Ξaug

/-- Replacement-style graph comparisons are marked by family incomparability. -/
def GraphReplacementComparisonDomain
    {G : _root_.ActualizationGraph}
    (F₁ F₂ : GraphSupportCutFamily G) : Prop :=
  GraphFamilyIncomparable F₁ F₂

/-- General graph valid comparison exposes the targeting-alignment guardrail. -/
theorem GraphValidFamilyComparison.targeting_aligned
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    {Ξ₁ : GraphFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : GraphFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : GraphValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    targetingAligned :=
  h.1

/-- General graph valid comparison exposes the exposure-alignment guardrail. -/
theorem GraphValidFamilyComparison.exposure_aligned
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    {Ξ₁ : GraphFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : GraphFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : GraphValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    exposureAligned :=
  h.2.1

/-- General graph valid comparison exposes family comparability. -/
theorem GraphValidFamilyComparison.family_comparable
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    {Ξ₁ : GraphFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : GraphFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : GraphValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    GraphFamilyComparable F₁ F₂ :=
  h.2.2.1

/-- General graph valid comparison exposes certificate agreement on the
overlapping family domain. -/
theorem GraphValidFamilyComparison.certificate_agreement
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F₁ F₂ : GraphSupportCutFamily G}
    {Ξ₁ : GraphFamilyCertificateContext G Γ M F₁}
    {Ξ₂ : GraphFamilyCertificateContext G Γ M F₂}
    {targetingAligned exposureAligned : Prop}
    (h : GraphValidFamilyComparison Ξ₁ Ξ₂ targetingAligned exposureAligned) :
    GraphCertificateAgreementOnOverlap Ξ₁ Ξ₂ :=
  h.2.2.2

/-- Valid graph augmentation exposes the certified-family augmentation witness. -/
theorem GraphValidAugmentationComparison.certified_augmentation
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξbase : GraphFamilyCertificateContext G Γ M Fbase}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    (h : GraphValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned) :
    GraphCertifiedFamilyAugments Ξbase Ξaug :=
  h.2.2

/-- Valid additive graph comparison preserves family-internal resilience. -/
theorem GraphValidAugmentationComparison.to_family_internal_resilience
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξbase : GraphFamilyCertificateContext G Γ M Fbase}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    {x : GraphVertex G}
    (hvalid : GraphValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned)
    (hres : GraphFamilyInternalResilienceAt G Γ M Fbase Ξbase x) :
    GraphFamilyInternalResilienceAt G Γ M Faug Ξaug x :=
  GraphFamilyInternalResilienceAt.mono_certified_augmentation
    hvalid.certified_augmentation hres

/-- Valid additive graph comparison plus parent failure produces the Track A.2
augmentation-rescue surface. -/
theorem GraphValidAugmentationComparison.to_augmentation_rescue
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξbase : GraphFamilyCertificateContext G Γ M Fbase}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {targetingAligned exposureAligned : Prop}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (hvalid : GraphValidAugmentationComparison Ξbase Ξaug targetingAligned exposureAligned)
    (hQ : Fbase.cuts Qparent)
    (hnot : ¬ GraphReadyAt G Qparent x)
    (hres : GraphFamilyInternalResilienceAt G Γ M Faug Ξaug x) :
    GraphFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x :=
  ⟨hvalid.certified_augmentation.1, hQ, hnot, hres⟩

/-- Replacement-domain marker exposes graph family incomparability. -/
theorem GraphReplacementComparisonDomain.incomparable
    {G : _root_.ActualizationGraph}
    {F₁ F₂ : GraphSupportCutFamily G}
    (h : GraphReplacementComparisonDomain F₁ F₂) :
    GraphFamilyIncomparable F₁ F₂ :=
  h

end GraphComparisonDomainValidity

end RA
