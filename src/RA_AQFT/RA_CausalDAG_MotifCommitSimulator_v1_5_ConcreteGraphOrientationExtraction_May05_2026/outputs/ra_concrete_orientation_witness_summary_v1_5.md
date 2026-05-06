# RA v1.5 Concrete-Graph Orientation-Link Witness Extraction Summary

v1.5 derives orientation-link witnesses from CONCRETE DAG TOPOLOGY
(parent/child edges with topology-derived signs) on a small reference
corpus of 58 deterministically-generated DAGs.

## Summary metrics

- version: v1.5
- input_dir: ../RA_CausalDAG_MotifCommitSimulator_v1_0_NativeCertificateAnchoring_May05_2026/outputs
- corpus_size: 58
- v1_0_input_rows: 480
- concrete_component_rows: 480
- decoupling_rows: 12
- decoupled_count: 12
- decoupled_total: 12
- concrete_orientation_surface_decoupled: True
- matched_orientation_variation_available: True
- orientation_specificity_resolved: True
- selector_guardrail_passed: True
- mean_concrete_orientation_residual_std: 0.038893
- v1_5_posture: concrete_graph_topology_orientation_witness_extraction_complete_pending_v0_9_simulator_graph_integration

## Honesty caveat

The reference corpus is synthetic-deterministic, not extracted from
the v0.9 simulator's actual ActualizationDAG instances. Witnesses are
derived from real graph topology (parent/child edges with depth-derived
signs), but the corpus itself is a parallel construction. v1.6+ should
integrate with v0.9 simulator graphs OR with a derived RA_GraphCore
Lean-side extractor.