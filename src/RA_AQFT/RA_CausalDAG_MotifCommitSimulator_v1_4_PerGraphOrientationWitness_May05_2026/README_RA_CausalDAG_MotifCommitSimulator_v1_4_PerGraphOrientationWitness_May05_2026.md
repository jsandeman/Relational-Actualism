# RA Causal-DAG Motif-Commit Simulator v1.4 — Per-Graph Orientation-Link Witness Extraction

This packet advances the orientation-link line one step beyond v1.3.

- v1.2 supplied a synthetic distinct orientation-link surface.
- v1.3 supplied a native theorem/sign-source catalog surface.
- v1.4 extracts per-graph/per-support-family-member orientation-link witness records from simulator state rows, using the native catalog as the vocabulary source.

This is still not a final Lean/native graph extraction theorem. It is an operational per-graph witness-surface prototype: witness records are keyed by simulator graph instance, motif, site, support-family member, and native catalog tokens. The next step is to replace the simulator-state extraction with concrete RA graph/cut/orientation witness data.

## Main command

```bash
python scripts/run_per_graph_orientation_witness_v1_4.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs \
  --native-manifest-dir ../RA_CausalDAG_MotifCommitSimulator_v1_3_NativeOrientationLinkDerivation_May05_2026/outputs \
  --native-lean-dir /path/to/src/RA_AQFT \
  --output-dir outputs
```

## Success criteria

1. Per-graph/member orientation witnesses are extracted from simulator state rows.
2. `per_graph_orientation_link_overlap` is distinct from support/frontier overlap.
3. Matched support/frontier strata contain multiple orientation-link bins.
4. Orientation-degradation rescue decreases as per-graph orientation-link overlap increases.
5. Ledger failure remains a control rather than being explained by orientation-link overlap.
6. Selector stress remains outside certification rescue.
7. Lean bridge compiles if installed into the active RA Lean project.

## Caveat

v1.4 is stronger than v1.3 because it is per-graph/member keyed, but it still uses simulator state rows and native-catalog tokens. It is not yet a theorem that concrete `ActualizationGraph` instances carry these exact orientation-link witnesses.
