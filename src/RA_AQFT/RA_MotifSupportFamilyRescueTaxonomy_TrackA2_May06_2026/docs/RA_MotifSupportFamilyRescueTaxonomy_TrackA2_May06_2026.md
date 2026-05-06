# RA_MotifSupportFamilyRescueTaxonomy — Track A.2

This packet refines the robust Track A support-family/certification-family line by separating support-family **inclusion**, **augmentation**, **replacement/incomparability**, **strict-parent rescue**, and **family-internal resilience**.

It is deliberately conservative:

- no probability laws;
- no numerical rescue-rate claims;
- no orientation-specific rescue claims;
- no new simulator semantics;
- no Nature-facing prediction.

## Formal point

A support-family extension is no-worse only when it is genuinely an augmentation:

```text
F ⊆ Faug
```

and, for certificate-family resilience, when certificate witnesses are preserved:

```text
Ξ.certifies Q → Ξaug.certifies Q
```

The module then formalizes augmentation rescue:

```text
base parent cut not ready
+ augmented certified family ready
⇒ strict-parent rescue in augmented family
⇒ family-internal resilience
⇒ certified-family readiness
```

This captures the robust positive lesson of the v0.7.x metric-repair sequence: support-family resilience is meaningful only when the comparison domain is disciplined. Replacement families and incomparable families do not inherit no-worse behavior from inclusion alone.

## Main Lean declarations

DAG:

```text
DAGFamilyEquivalent
DAGFamilyStrictlyAugments
DAGFamilyComparable
DAGFamilyIncomparable
DAGCertifiedFamilyAugments
DAGFamilyAugmentationRescueAt
```

Graph:

```text
GraphFamilyEquivalent
GraphFamilyStrictlyAugments
GraphFamilyComparable
GraphFamilyIncomparable
GraphCertifiedFamilyAugments
GraphFamilyAugmentationRescueAt
```

## Main theorem surface

```text
Family equivalence is reflexive/symmetric.
Strict augmentation implies base-family inclusion and not reverse inclusion.
Certified-family augmentation preserves family-internal resilience.
Augmentation rescue refines to strict-parent rescue.
Augmentation rescue refines to family-internal resilience.
Augmentation rescue refines to certified-family readiness.
```

## Relation to prior Track A modules

```text
RA_MotifCertificationResilienceConsolidation
  strict-parent rescue vs family-internal resilience

RA_MotifCertificateCorrelationBridge
  shared-fate / member-distinct certificate-fate structure

RA_MotifNativeOverlapCorrelationBridge
  high native-overlap endpoint → shared-fate family

RA_MotifSupportFamilyRescueTaxonomy
  support-family inclusion / augmentation / replacement taxonomy
```

## Epistemic status

Source-level pending local compile until checked in the RA Lean environment.
