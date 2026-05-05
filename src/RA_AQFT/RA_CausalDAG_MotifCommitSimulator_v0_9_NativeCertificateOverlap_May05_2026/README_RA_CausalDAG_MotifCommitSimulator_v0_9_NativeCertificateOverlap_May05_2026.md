# RA Causal-DAG Motif-Commit Simulator v0.9 — Native Certificate Overlap / BDG–LLC Anchoring

This packet is the first native-overlap anchoring layer after v0.8/v0.8.1.

v0.8 used an external simulator parameter, `certificate_correlation`, and showed
that certification rescue decays as that correlation increases. v0.9 replaces
that parameter with an overlap-derived effective correlation computed from
support-family member certificate witnesses.

The v0.9 witness-overlap components are simulator-side proxies for RA-native
structure:

- support-cut overlap
- Hasse-frontier/support-frontier overlap
- orientation-incidence-link overlap
- native-ledger-gate overlap
- causal-past overlap
- BDG–LLC local-kernel overlap proxy
- causal-firewall exposure overlap proxy

This is still a workbench, not a derived physical law. The point is to make the
correlation signature depend on native graph/witness overlap rather than an
external knob.

## Main hypothesis

```text
certification rescue decreases as native certificate-witness overlap increases
```

## Run

```bash
python scripts/run_native_certificate_overlap_v0_9.py   --seed-start 17   --seed-stop 117   --steps 32   --max-targets 12   --threshold-fractions 1.0,0.75,0.5,0.25   --family-semantics at_least_k,augmented_exact_k   --modes ledger_failure,orientation_degradation,selector_stress   --output-dir outputs
```

## Key success criteria

1. Native overlap bins are nontrivial.
2. Certification rescue is higher in low-overlap families than high-overlap families, within populated bins.
3. Parent-shared baseline has no certification rescue.
4. Selector stress remains outside support/certification-family rescue.
5. Witness-overlap component tables expose whether the signature is support/frontier-, orientation-, ledger-, or causal-overlap driven.

## RAKB caution

The overlap calculation is operational. It should be treated as a candidate
bridge toward BDG–LLC/native certificate anchoring, not as a final law of Nature.

## Packet-local demo outputs

The packet includes a small validation run with 9,600 evaluations. It is not canonical. Main outputs:

- `ra_native_certificate_overlap_summary_v0_9.csv`
- `ra_native_certificate_overlap_aggregate_v0_9.csv`
- `ra_witness_overlap_components_v0_9.csv`
- `ra_cert_rescue_by_native_overlap_v0_9.csv`
- `ra_overlap_induced_correlation_curve_v0_9.csv`
- `ra_overlap_vs_external_correlation_comparison_v0_9.csv`
- `ra_native_certificate_overlap_selector_guardrail_v0_9.csv`
- `ra_native_cert_overlap_predictions_v0_9.md`
