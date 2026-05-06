import RA_MotifCertificationResilienceConsolidation

/-!
# RA_MotifSupportFamilyRescueTaxonomy

Track A.2 formal refinement for support-family inclusion and rescue taxonomy.

The preceding Track A modules established:

* support-cut families and family inclusion;
* certified family readiness;
* strict-parent rescue versus family-internal resilience;
* qualitative certificate-fate and native-overlap bridges.

This module isolates the support-family taxonomy used by the robust positive
resilience line.  It deliberately excludes the retracted orientation-specific
rescue branch and asserts no numerical/probabilistic rescue law.

The central distinction is:

* **augmentation**: a new family contains the old family; readiness/resilience is
  no-worse when certificates are also included;
* **replacement / incomparability**: a new family need not preserve the old cuts,
  so no no-worse theorem is available without extra hypotheses;
* **augmentation rescue**: the parent cut fails, but an augmented certified
  family remains ready.
-/

namespace RA

/-! ## DAG inclusion taxonomy and rescue refinements -/

section O01SupportFamilyRescueTaxonomy

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Two DAG support-cut families are extensionally equivalent when each includes
the other. -/
def DAGFamilyEquivalent
    (F F' : DAGSupportCutFamily V) : Prop :=
  DAGFamilyIncluded F F' ∧ DAGFamilyIncluded F' F

/-- `Faug` strictly augments `F` when it includes `F` but is not included back in
`F`.  This is the formal surface for true additive family expansion. -/
def DAGFamilyStrictlyAugments
    (Faug F : DAGSupportCutFamily V) : Prop :=
  DAGFamilyIncluded F Faug ∧ ¬ DAGFamilyIncluded Faug F

/-- Two DAG support-cut families are comparable when one includes the other. -/
def DAGFamilyComparable
    (F F' : DAGSupportCutFamily V) : Prop :=
  DAGFamilyIncluded F F' ∨ DAGFamilyIncluded F' F

/-- Two DAG support-cut families are incomparable when neither includes the other.
This is the replacement-style regime where no augmentation/no-worse theorem is
available from inclusion alone. -/
def DAGFamilyIncomparable
    (F F' : DAGSupportCutFamily V) : Prop :=
  ¬ DAGFamilyIncluded F F' ∧ ¬ DAGFamilyIncluded F' F

/-- Equivalence of support-cut families is reflexive. -/
theorem DAGFamilyEquivalent.refl
    (F : DAGSupportCutFamily V) : DAGFamilyEquivalent F F :=
  ⟨DAGFamilyIncluded.refl F, DAGFamilyIncluded.refl F⟩

/-- Equivalence of support-cut families is symmetric. -/
theorem DAGFamilyEquivalent.symm
    {F F' : DAGSupportCutFamily V}
    (h : DAGFamilyEquivalent F F') : DAGFamilyEquivalent F' F :=
  ⟨h.2, h.1⟩

/-- Strict augmentation records ordinary inclusion from the base family into the
augmented family. -/
theorem DAGFamilyStrictlyAugments.included
    {Faug F : DAGSupportCutFamily V}
    (h : DAGFamilyStrictlyAugments Faug F) :
    DAGFamilyIncluded F Faug :=
  h.1

/-- Strict augmentation records failure of reverse inclusion. -/
theorem DAGFamilyStrictlyAugments.not_reverse_included
    {Faug F : DAGSupportCutFamily V}
    (h : DAGFamilyStrictlyAugments Faug F) :
    ¬ DAGFamilyIncluded Faug F :=
  h.2

/-- A certified-family augmentation includes the base family and preserves all
base-family certificate witnesses in the augmented certificate context. -/
def DAGCertifiedFamilyAugments
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F Faug : DAGSupportCutFamily V}
    (Ξ : DAGFamilyCertificateContext G Γ M F)
    (Ξaug : DAGFamilyCertificateContext G Γ M Faug) : Prop :=
  DAGFamilyIncluded F Faug ∧ ∀ Q, Ξ.certifies Q → Ξaug.certifies Q

/-- Certified-family augmentation preserves family-internal resilience. -/
theorem DAGFamilyInternalResilienceAt.mono_certified_augmentation
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {F Faug : DAGSupportCutFamily V}
    {Ξ : DAGFamilyCertificateContext G Γ M F}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {x : V}
    (haug : DAGCertifiedFamilyAugments Ξ Ξaug)
    (h : DAGFamilyInternalResilienceAt G Γ M F Ξ x) :
    DAGFamilyInternalResilienceAt G Γ M Faug Ξaug x := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, haug.2 Q hcert, hready⟩

/-- Augmentation rescue: a base-family parent cut fails, but an augmented
certified family remains ready.  This is the formal Track A surface for
additive support-family rescue. -/
def DAGFamilyAugmentationRescueAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V)
    (Fbase Faug : DAGSupportCutFamily V)
    (Ξaug : DAGFamilyCertificateContext G Γ M Faug)
    (Qparent : CausalSupportCut V) (x : V) : Prop :=
  DAGFamilyIncluded Fbase Faug ∧
  Fbase.cuts Qparent ∧
  ¬ DAGReadyAt G Qparent x ∧
  DAGIndependentCertifiedFamilyReadyAt G Γ M Faug Ξaug x

/-- Augmentation rescue is a strict-parent rescue in the augmented family. -/
theorem DAGFamilyAugmentationRescueAt.to_strict_parent_rescue
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    DAGStrictParentRescueAt G Γ M Faug Ξaug Qparent x := by
  exact ⟨h.1 Qparent h.2.1, h.2.2.1, h.2.2.2⟩

/-- Augmentation rescue implies family-internal resilience in the augmented
family. -/
theorem DAGFamilyAugmentationRescueAt.to_family_internal_resilience
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    DAGFamilyInternalResilienceAt G Γ M Faug Ξaug x :=
  h.2.2.2

/-- Augmentation rescue implies ordinary certified-family readiness in the
augmented family. -/
theorem DAGFamilyAugmentationRescueAt.to_certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V}
    {Fbase Faug : DAGSupportCutFamily V}
    {Ξaug : DAGFamilyCertificateContext G Γ M Faug}
    {Qparent : CausalSupportCut V} {x : V}
    (h : DAGFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    DAGCertifiedFamilyReadyAt G Γ M Faug x :=
  DAGIndependentCertifiedFamilyReadyAt.to_certified_family_ready h.2.2.2

end O01SupportFamilyRescueTaxonomy

/-! ## Concrete graph inclusion taxonomy and rescue refinements -/

section GraphSupportFamilyRescueTaxonomy

/-- Concrete graph support-cut family equivalence. -/
def GraphFamilyEquivalent
    {G : _root_.ActualizationGraph}
    (F F' : GraphSupportCutFamily G) : Prop :=
  GraphFamilyIncluded F F' ∧ GraphFamilyIncluded F' F

/-- Concrete graph strict augmentation. -/
def GraphFamilyStrictlyAugments
    {G : _root_.ActualizationGraph}
    (Faug F : GraphSupportCutFamily G) : Prop :=
  GraphFamilyIncluded F Faug ∧ ¬ GraphFamilyIncluded Faug F

/-- Concrete graph family comparability. -/
def GraphFamilyComparable
    {G : _root_.ActualizationGraph}
    (F F' : GraphSupportCutFamily G) : Prop :=
  GraphFamilyIncluded F F' ∨ GraphFamilyIncluded F' F

/-- Concrete graph family incomparability. -/
def GraphFamilyIncomparable
    {G : _root_.ActualizationGraph}
    (F F' : GraphSupportCutFamily G) : Prop :=
  ¬ GraphFamilyIncluded F F' ∧ ¬ GraphFamilyIncluded F' F

/-- Graph-family equivalence is reflexive. -/
theorem GraphFamilyEquivalent.refl
    {G : _root_.ActualizationGraph}
    (F : GraphSupportCutFamily G) : GraphFamilyEquivalent F F :=
  ⟨GraphFamilyIncluded.refl F, GraphFamilyIncluded.refl F⟩

/-- Graph-family equivalence is symmetric. -/
theorem GraphFamilyEquivalent.symm
    {G : _root_.ActualizationGraph}
    {F F' : GraphSupportCutFamily G}
    (h : GraphFamilyEquivalent F F') : GraphFamilyEquivalent F' F :=
  ⟨h.2, h.1⟩

/-- Strict graph augmentation records ordinary inclusion. -/
theorem GraphFamilyStrictlyAugments.included
    {G : _root_.ActualizationGraph}
    {Faug F : GraphSupportCutFamily G}
    (h : GraphFamilyStrictlyAugments Faug F) :
    GraphFamilyIncluded F Faug :=
  h.1

/-- Strict graph augmentation records failure of reverse inclusion. -/
theorem GraphFamilyStrictlyAugments.not_reverse_included
    {G : _root_.ActualizationGraph}
    {Faug F : GraphSupportCutFamily G}
    (h : GraphFamilyStrictlyAugments Faug F) :
    ¬ GraphFamilyIncluded Faug F :=
  h.2

/-- A concrete graph certified-family augmentation includes the base family and
preserves all base-family certificate witnesses in the augmented certificate
context. -/
def GraphCertifiedFamilyAugments
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F Faug : GraphSupportCutFamily G}
    (Ξ : GraphFamilyCertificateContext G Γ M F)
    (Ξaug : GraphFamilyCertificateContext G Γ M Faug) : Prop :=
  GraphFamilyIncluded F Faug ∧ ∀ Q, Ξ.certifies Q → Ξaug.certifies Q

/-- Concrete graph certified-family augmentation preserves family-internal
resilience. -/
theorem GraphFamilyInternalResilienceAt.mono_certified_augmentation
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {F Faug : GraphSupportCutFamily G}
    {Ξ : GraphFamilyCertificateContext G Γ M F}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {x : GraphVertex G}
    (haug : GraphCertifiedFamilyAugments Ξ Ξaug)
    (h : GraphFamilyInternalResilienceAt G Γ M F Ξ x) :
    GraphFamilyInternalResilienceAt G Γ M Faug Ξaug x := by
  rcases h with ⟨Q, hcert, hready⟩
  exact ⟨Q, haug.2 Q hcert, hready⟩

/-- Concrete graph augmentation rescue: a base-family parent cut fails, but an
augmented certified family remains ready. -/
def GraphFamilyAugmentationRescueAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G)
    (Fbase Faug : GraphSupportCutFamily G)
    (Ξaug : GraphFamilyCertificateContext G Γ M Faug)
    (Qparent : GraphSupportCut G) (x : GraphVertex G) : Prop :=
  GraphFamilyIncluded Fbase Faug ∧
  Fbase.cuts Qparent ∧
  ¬ GraphReadyAt G Qparent x ∧
  GraphIndependentCertifiedFamilyReadyAt G Γ M Faug Ξaug x

/-- Concrete graph augmentation rescue is strict-parent rescue in the augmented
family. -/
theorem GraphFamilyAugmentationRescueAt.to_strict_parent_rescue
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    GraphStrictParentRescueAt G Γ M Faug Ξaug Qparent x := by
  exact ⟨h.1 Qparent h.2.1, h.2.2.1, h.2.2.2⟩

/-- Concrete graph augmentation rescue implies family-internal resilience in the
augmented family. -/
theorem GraphFamilyAugmentationRescueAt.to_family_internal_resilience
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    GraphFamilyInternalResilienceAt G Γ M Faug Ξaug x :=
  h.2.2.2

/-- Concrete graph augmentation rescue implies ordinary certified-family
readiness in the augmented family. -/
theorem GraphFamilyAugmentationRescueAt.to_certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G}
    {Fbase Faug : GraphSupportCutFamily G}
    {Ξaug : GraphFamilyCertificateContext G Γ M Faug}
    {Qparent : GraphSupportCut G} {x : GraphVertex G}
    (h : GraphFamilyAugmentationRescueAt G Γ M Fbase Faug Ξaug Qparent x) :
    GraphCertifiedFamilyReadyAt G Γ M Faug x :=
  GraphIndependentCertifiedFamilyReadyAt.to_certified_family_ready h.2.2.2

end GraphSupportFamilyRescueTaxonomy

end RA
