# RA v1.6 Graph-Coupled Orientation-Link Extraction Summary

v1.6 closes the rescue/topology disconnection identified in v1.5.
Rescue and orientation_link_overlap are now extracted from the SAME
v0.9 simulator CausalDAG instance per trial.

## Summary metrics

- version: v1.6
- n_trials: 3840
- n_seeds: 4
- n_severance_seeds: 1
- n_modes: 3
- n_severities: 5
- n_threshold_fractions: 4
- n_family_semantics: 2
- max_targets: 8
- v1_6_posture: rescue_and_orientation_extracted_from_same_dag_per_trial
- n_per_cell_rows: 480
- decoupled_count: 12
- decoupled_total: 12
- graph_coupled_orientation_surface_decoupled: True
- orientation_specificity_resolved_on_matched_graphs: False
- selector_guardrail_passed: True
- v1_6_disconnection_closed: True

## Honesty caveat

v1.6 uses a SUBSET of v0.9's parameter sweep to keep runtime tractable.
Headline result is restricted to that subset. v1.7+ should expand to
the canonical 100-seed v0.9 parameter coverage.