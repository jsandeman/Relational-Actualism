# RA Causal-DAG Motif Commit Simulator v1.3 — Native Orientation-Link Derivation

This packet follows v1.2's identifiability demonstration.  v1.2 showed that the audit machinery can resolve orientation-specific certification behavior **if** given a distinct orientation-link surface, but its surface was generated from row metadata.  v1.3 replaces that row-metadata surface with a native Lean theorem/sign-source catalog surface extracted from RA native orientation, ledger, and closure modules.

## Status

- Analysis layer: canonical/demo runnable.
- Lean bridge: source-level pending local compile in this container.
- Python tests: pass.
- RAKB proposals: active-schema style, no auto-apply script.

## Main conceptual status

v1.3 is stronger than v1.2, but it is still an intermediate anchoring step:

```text
v1.2 synthetic orientation-link surface
  → v1.3 native Lean theorem/sign-source catalog surface
  → future per-graph native orientation-link witness extraction
```

It does **not** yet prove that every concrete support-family member has per-graph orientation links extracted from RA_CausalOrientation_Core or NativeLedgerOrientation. It demonstrates that a native theorem-catalog-derived orientation surface is distinct from support/frontier overlap and supports orientation-specific diagnostics.

## Inputs

The analysis expects the v1.0 component output:

```text
ra_native_certificate_components_v1_0.csv
```

and optionally a Lean source directory containing native files such as:

```text
RA_CausalOrientation_Core.lean
RA_D1_NativeLedgerOrientation.lean
RA_D1_NativeClosure.lean
RA_D1_GraphCutCombinatorics.lean
RA_D3_CausalSevrence.lean
RA_D4_CausalFirewall.lean
```

If a Lean directory is unavailable, the analysis falls back to a minimal native orientation manifest.

## Run

```bash
python scripts/run_native_orientation_derivation_v1_3.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_0_NativeCertificateAnchoring_May05_2026/outputs \
  --native-lean-dir /path/to/src/RA_AQFT \
  --output-dir outputs
```

## Local demo result

The included run, using available v1.0 outputs and uploaded native Lean files, produced:

```text
native_orientation_catalog_manifest_used = true
native_orientation_surface_decoupled = true
matched_orientation_variation_available = true
orientation_specificity_resolved = true
selector_guardrail_passed = true
native_orientation_residual_std ≈ 0.174
legacy_orientation_residual_std ≈ 3.7e-16
v1_3_posture = native_catalog_orientation_surface_ready_for_per_graph_witness_derivation
```

## Outputs

```text
ra_native_orientation_theorem_manifest_v1_3.csv
ra_native_orientation_link_surface_v1_3.csv
ra_native_orientation_support_decoupling_audit_v1_3.csv
ra_native_orientation_matched_strata_v1_3.csv
ra_native_orientation_specificity_after_support_control_v1_3.csv
ra_native_orientation_partial_correlation_v1_3.csv
ra_native_orientation_component_rank_v1_3.csv
ra_native_orientation_derivation_summary_v1_3.csv
ra_native_orientation_derivation_summary_v1_3.md
ra_native_orientation_derivation_state_v1_3.json
```

## Caveat

The v1.3 orientation-link surface is derived from a native Lean theorem/sign-source catalog, not from per-graph extracted orientation-link witness instances. It is a bridge from synthetic proxy to native-catalog proxy, not yet a final native orientation-overlap law.
