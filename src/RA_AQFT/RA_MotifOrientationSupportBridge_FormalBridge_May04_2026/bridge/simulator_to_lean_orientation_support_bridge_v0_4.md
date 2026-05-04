# Simulator-to-Lean Bridge Note: Orientation Support

The v0.3 simulator introduced selector closure as an experimental implementation layer. The present Lean bridge should guide v0.4 as follows.

## Simulator vocabulary alignment

Use RA-native names that mirror the Lean module:

```text
graph_oriented_motif_support
oriented_support_certified
orientation_supports
orientation_conflict_witness
orientation_actualization_context
orientation_selector_closure
orientation_selected_commitment
orientation_unresolved_incompatibility
```

Avoid making simulator policies primitive in Lean:

```text
greedy tie-break
lexicographic priority
collapse
vote/quorum winner
```

## v0.4 target behavior

A simulator motif should be unsupported unless it has a graph-oriented motif support witness satisfying:

```text
motif carrier lies in candidate past
frontier_sufficient_for_motif gate passes
local_ledger_compatible gate passes
closure.selector_compatible gate passes
closure.no_extra_random_labels gate passes
closure.nativeEvidence.no_particle_label_primitives gate passes
support cut equals finite Hasse frontier
```

Orientation-context incompatibility should be witness-grounded:

```text
incompatible(M1, M2) only if an orientation_conflict_witness exists
```

## Interpretive status

This is an RA-native modeling layer for actualization constraints. It is not a simulation of QM, GR, or distributed consensus. Correspondence comparisons belong only in explicitly marked comparison reports.
