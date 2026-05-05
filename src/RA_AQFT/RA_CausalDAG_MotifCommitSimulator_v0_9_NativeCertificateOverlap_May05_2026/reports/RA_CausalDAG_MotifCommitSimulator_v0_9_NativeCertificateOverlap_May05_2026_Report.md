# RA Causal-DAG Motif-Commit Simulator v0.9 Report

## Purpose

v0.9 anchors the v0.8/v0.8.1 certification-correlation signature to native witness overlap. Instead of assigning a certificate-correlation knob directly, the workbench computes component overlaps among member certificate witnesses and uses the weighted overlap as the effective correlation for independent-member certification.

## Native-overlap components

The simulator computes tokenized proxies for:

- support-cut overlap
- Hasse-frontier/support-frontier overlap
- orientation-incidence-link overlap
- native-ledger-gate overlap
- causal-past overlap
- BDG-LLC local-kernel overlap proxy
- causal-firewall/severance-exposure overlap proxy

These components are operational bridges, not final derived BDG-LLC laws.

## Packet-local validation

- Python tests: 5/5 pass.
- Source audit: no `sorry`, `admit`, or `axiom`; no inherited-theory / consensus operational vocabulary hits.
- Lean bridge: source-level formal bridge pending local compile.

## Packet-local demo

The included demo run used seeds 17..20, 16 steps, max-targets 6, and 9,600 evaluations.

Observed packet-local summary:

```text
support_width_classes = [1, 2, 3, 4]
native_overlap_bins = [high, low, medium]
min_induced_certificate_correlation = 0.215038
max_induced_certificate_correlation = 1.0
native_certification_rescue_rate = 0.044922
native_family_certification_resilience_rate = 0.426107
overlap_signature_monotone_count = 4 / 4
selector_guardrail_passed = true
```

## Interpretation

The packet-local result demonstrates that the workbench can produce nontrivial native-overlap bins and induce a certificate-correlation profile from graph/witness overlap rather than from an external parameter. The canonical claim is pending a larger run.

The intended RA-native hypothesis is:

```text
certification rescue decreases as native certificate-witness overlap increases
```

## Status

- Python workbench: packet-local validated.
- Lean bridge: source-level formal bridge pending local compile.
- RAKB proposals: active-schema-style proposals included; no auto-apply script.
- Nature-level claim: not made.
