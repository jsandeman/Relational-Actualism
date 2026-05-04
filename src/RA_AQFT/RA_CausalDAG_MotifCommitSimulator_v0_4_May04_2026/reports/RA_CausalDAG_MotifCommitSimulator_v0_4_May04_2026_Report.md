# RA Causal-DAG Motif-Commit Simulator v0.4 Report

Date: May 04, 2026

## Purpose

v0.4 connects the motif-commit simulator to the orientation-support bridge by making support certification depend on an explicit graph-oriented witness.

This implements the next RA-native simulator ladder:

```text
candidate motif
  -> finite Hasse-frontier support cut
  -> graph-oriented support witness
  -> orientation-gated support certification
  -> causal readiness
  -> strict commitment or strict exclusion
  -> selector closure
  -> selected commitment
```

## What changed from v0.3

v0.3 already separated:

```text
finite support set
```

from:

```text
certified causal support cut
```

v0.4 further separates:

```text
ordinary graph support certification
```

from:

```text
orientation-gated graph support certification
```

A candidate now needs a `GraphOrientedMotifSupport` witness with a valid `OrientationClosureCertificate`.

## New support gates

The key new gates are:

```text
orientation_witness_declared
orientation_witness_names_motif
orientation_candidate_past_matches_declared
orientation_support_cut_matches_supplied
orientation_support_cut_is_hasse_frontier
orientation_carrier_represented_by_frontier
orientation_frontier_sufficient_for_motif
orientation_local_ledger_compatible
orientation_selector_compatible
orientation_no_extra_random_labels
orientation_no_particle_label_primitives
orientation_sign_links_valid
orientation_sign_source_covers_support
orientation_qN1_seven
orientation_local_conserved
```

## Conflict discipline

v0.4 also includes witnessed orientation conflicts:

```text
OrientationConflictWitness
OrientationActualizationContext.conflict_witness
```

A conflict is not just a loose label. The simulator records a witness row when the selected component contains motifs sharing an orientation conflict domain.

## Validation

Unit tests:

```text
Ran 8 tests
OK
```

Tested behaviors:

1. Missing orientation witness blocks support.
2. Valid orientation witness allows support.
3. Non-seven qN1 blocks support.
4. Missing sign-source coverage blocks support.
5. Orientation conflict witnesses block strict commitment.
6. Unsupported incompatible competitors do not block certified-ready motifs.
7. Selector stalemate records unresolved equal-rank conflict.
8. Demo run produces orientation witness output.

## Demo result

Default demo with sweep:

```text
nodes=25
edges=33
motifs=41
sites=24
total_strict_committed=328
total_strict_blocked=70
total_selector_committed=363
total_selector_rejected=35
total_selector_stalemates=0
total_unsupported=140
total_orientation_failures=68
mean_support_width=1.0
```

## Interpretation

The key result is methodological and architectural:

```text
A motif candidate cannot become certified-ready merely by naming a support cut.
It must pass graph support gates and orientation witness gates.
```

This makes the simulator closer to the formal orientation-support bridge while keeping the semantics RA-native.

## Known limitation

The simulator's `orientation_carrier_represented_by_frontier` gate is an operational proxy for the Lean bridge's carrier obligation. It checks frontier-to-carrier reachability plus an explicit witness bit rather than direct membership of the carrier in the candidate past.

This is intentional for the simulator's site-carrier representation and should be revisited if the simulator motif carrier is changed to match the Lean `GraphMotifCandidate` carrier more literally.
