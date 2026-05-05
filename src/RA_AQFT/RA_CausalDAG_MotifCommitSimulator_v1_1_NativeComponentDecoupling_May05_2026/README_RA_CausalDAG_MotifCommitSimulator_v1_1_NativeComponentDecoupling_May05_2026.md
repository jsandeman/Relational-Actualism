# RA Causal-DAG Motif-Commit Simulator v1.1 — Native Component Decoupling

This packet is a focused analysis layer over the v1.0 native-certificate anchoring outputs.
It adds no new simulator semantics and no new Lean module.

## Purpose

v1.0 showed that the native certificate-overlap proxy is useful, but it also exposed a
component-attribution limitation: the orientation-overlap surface was numerically tied to
support/frontier overlap. v1.1 audits that limitation directly.

The key question is:

```text
Can orientation-overlap vary independently of support/frontier overlap?
```

If not, the packet reports the confounding honestly rather than asserting orientation-specificity.

## Main outputs

- `ra_component_decoupling_audit_v1_1.csv`
- `ra_orientation_specificity_by_mode_v1_1.csv`
- `ra_component_partial_correlation_v1_1.csv`
- `ra_matched_overlap_strata_v1_1.csv`
- `ra_orientation_ablation_after_support_control_v1_1.csv`
- `ra_ledger_orientation_specificity_comparison_v1_1.csv`
- `ra_native_component_decoupling_summary_v1_1.csv`
- `ra_native_component_decoupling_summary_v1_1.md`

## Canonical run

```bash
python scripts/run_native_component_decoupling_v1_1.py   --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_0_NativeCertificateAnchoring_May05_2026/outputs   --output-dir outputs
```

## Interpretation discipline

v1.1 distinguishes:

```text
ledger attribution:
  clean if ledger overlap is independently resolved from support/frontier

orientation attribution:
  clean only if orientation overlap varies independently of support/frontier
```

If support/frontier/orientation are numerically identical, orientation-degradation should be
reported as carried by a joint support/frontier/orientation proxy rather than by an isolated
orientation component.
