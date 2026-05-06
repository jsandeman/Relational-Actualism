# RA v1.6 Graph-Coupled Orientation-Link Extraction Summary

v1.6 closes the rescue/topology disconnection identified in v1.5.
Rescue and orientation_link_overlap are now extracted from the SAME
v0.9 simulator CausalDAG instance per trial.

## Summary metrics

- version: v1.6
- n_trials: 192
- n_seeds: 4
- n_severance_seeds: 1
- n_modes: 3
- n_severities: 1
- n_threshold_fractions: 1
- n_family_semantics: 2
- max_targets: 8
- v1_6_posture: matched_graph_subset_extraction_complete_not_canonical
- v1_6_run_scope: subset_matched_graph_diagnostic_run_not_canonical
- n_per_cell_rows: 24
- decoupled_count: 12
- decoupled_total: 12
- graph_coupled_orientation_surface_decoupled: True
- orientation_specificity_resolved_on_matched_graphs: False
- selector_guardrail_passed: True
- v1_6_disconnection_closed: True

## Honesty caveat

v1.6 default outputs are a SUBSET matched-graph diagnostic run, not a canonical run.
Headline result is restricted to that subset. Larger runs should expand to
the canonical 100-seed v0.9 parameter coverage.