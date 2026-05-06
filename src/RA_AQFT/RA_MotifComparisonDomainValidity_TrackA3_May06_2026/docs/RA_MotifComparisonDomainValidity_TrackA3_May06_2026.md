# RA_MotifComparisonDomainValidity — Track A.3

This packet adds a narrow formal bridge for **comparison-domain validity** in the
Track A support-family/certification-resilience line.

The v0.7 metric-repair sequence showed that rescue comparisons can be misleading
when the parent support cut, family-internal readiness, and family-targeted
certification surfaces live in different comparison domains. Track A.2 then
formalized augmentation versus replacement. Track A.3 names the guardrail:
comparison domains must be targeting-aligned, exposure-aligned, family-comparable,
and certificate-disciplined.

## Main Lean surfaces

DAG and Graph parallel pairs:

- `CertificateAgreementOnOverlap`
- `ValidFamilyComparison`
- `ValidAugmentationComparison`
- `ReplacementComparisonDomain`

## Main theorem surface

- valid comparison exposes targeting/exposure alignment;
- valid comparison exposes family comparability;
- valid comparison exposes certificate agreement on overlap;
- valid augmentation exposes certified-family augmentation;
- valid augmentation preserves family-internal resilience;
- valid augmentation plus parent failure yields augmentation rescue;
- replacement-domain comparisons expose family incomparability and therefore do
  not carry a no-worse theorem by inclusion alone.

## Deliberate exclusions

The module asserts no probability law, no numerical rescue-rate formula, no
correlation theorem, no orientation-specific rescue claim, and no Nature-facing
prediction. It is a formal guardrail layer for future simulator comparisons and
paper statements.
