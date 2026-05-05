# Simulator-to-RAKB Bridge: v0.9.2 Native Overlap Calibration / Family-Semantics Audit

v0.9.2 is an analysis-only audit layer. It closes the v0.9.1 family-semantics caveat by making three distinctions explicit:

1. Native-overlap rescue signal strength by support-family semantics.
2. Native-bin calibration against the v0.8.1 external certificate-correlation baseline.
3. Candidate semantics for v1.0 BDG–LLC/native-certificate anchoring.

The central RAKB posture should be cautious:

- `augmented_exact_k` may be promoted only as the current primary signal-carrier semantics, not as a final RA law.
- `at_least_k` should remain as a monotone guardrail semantics even when it collapses to zero signal in particular ledger slices.
- Native-overlap bins qualitatively align with external-correlation curves, but absolute calibration remains proxy-level.
