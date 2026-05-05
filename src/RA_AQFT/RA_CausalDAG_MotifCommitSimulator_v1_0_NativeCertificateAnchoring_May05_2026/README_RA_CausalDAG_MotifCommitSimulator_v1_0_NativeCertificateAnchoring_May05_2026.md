# RA Causal-DAG Motif Commit Simulator v1.0 — Native Certificate Anchoring

This packet consolidates the v0.9 native certificate-overlap line into a v1.0 anchoring layer.

It does **not** add a new rescue mechanism. It packages the component surfaces that the v0.9 simulator already used and records the resolved v0.9.2 posture:

- `augmented_exact_k` is the primary signal-carrier semantics.
- `at_least_k` is retained as a monotone guardrail semantics.
- native-overlap bins are qualitative structural bins, not exact external certificate-correlation values.
- selector stress remains outside support/certification-family rescue.

## Formal layer

`lean/RA_MotifNativeCertificateComponents.lean` imports:

```lean
import RA_MotifNativeCertificateOverlapBridge
```

and introduces component-level native certificate contexts for both the DAG and graph layers:

- support component
- frontier component
- orientation component
- ledger component
- causal-past component
- kernel-local component
- firewall / severance-exposure component

The bridge is qualitative. It does not assert a probability law or a numerical overlap metric.

## Analysis layer

Run against canonical v0.9 outputs, optionally with v0.9.2 calibration outputs:

```bash
python scripts/run_native_certificate_anchoring_v1_0.py   --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs   --calibration-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_2_NativeOverlapCalibration_May05_2026/outputs   --output-dir outputs
```

## Outputs

- `ra_native_certificate_components_v1_0.csv`
- `ra_native_overlap_profile_v1_0.csv`
- `ra_component_attribution_by_mode_v1_0.csv`
- `ra_augmented_exactk_signal_v1_0.csv`
- `ra_atleastk_guardrail_v1_0.csv`
- `ra_native_overlap_calibration_status_v1_0.csv`
- `ra_native_certificate_anchoring_summary_v1_0.csv`
- `ra_native_certificate_anchoring_summary_v1_0.md`
- `ra_native_certificate_anchoring_state_v1_0.json`

## Canonical success criteria

1. Lean bridge compiles with no proof-placeholder declarations.
2. Component-level overlap surfaces are populated.
3. `augmented_exact_k` remains the primary signal carrier.
4. `at_least_k` remains an informative monotone guardrail.
5. Native-overlap calibration is recorded as qualitative, not absolute.
6. Selector guardrail remains passed.
