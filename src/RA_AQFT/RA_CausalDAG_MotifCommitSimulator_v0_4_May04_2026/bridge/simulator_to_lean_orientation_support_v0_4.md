# Simulator v0.4 to Lean Bridge Note

The simulator v0.4 layer is designed to operationalize the formal surface of `RA_MotifOrientationSupportBridge` without claiming that the hard derivation has been completed.

## Lean surface

```text
GraphOrientedMotifSupport
GraphOrientedMotifSupport.certified
GraphOrientationSupports
GraphOrientationConflictWitness
GraphOrientationActualizationContext
GraphOrientationSelectedCommitsAt
GraphOrientationUnresolvedIncompatibilityAt
```

## Simulator surface

```text
GraphOrientedMotifSupport
OrientationClosureCertificate
GraphOrientationSupportCertifier
OrientationConflictWitness
OrientationActualizationContext
MotifCommitProtocol.selected_decision
```

## Certification mapping

Lean:

```text
W.certified Q :=
  W.frontier_sufficient_for_motif
  ∧ W.local_ledger_compatible
  ∧ W.closure.selector_compatible
  ∧ W.closure.no_extra_random_labels
  ∧ W.closure.nativeEvidence.no_particle_label_primitives
  ∧ Q = supportCutOfFiniteHasseFrontier P
```

Simulator:

```text
support_cut_is_hasse_frontier
orientation_frontier_sufficient_for_motif
orientation_local_ledger_compatible
orientation_selector_compatible
orientation_no_extra_random_labels
orientation_no_particle_label_primitives
orientation_qN1_seven
orientation_sign_links_valid
orientation_sign_source_covers_support
```

The simulator adds operational diagnostics beyond the Lean proposition surface. These are not new axioms; they are inspection gates for experimental runs.

## Carrier caveat

The Lean bridge uses `carrier_in_candidate_past`. The simulator treats motif carriers as actualization-site carriers, so it checks frontier-to-carrier reachability plus an explicit representation bit. This keeps support cuts in the causal past of the site and avoids making the support cut trivially equal to the site.

## Methodological discipline

The simulator uses RA-native terms first. Any comparison to inherited theories belongs only in explicitly marked interpretation sections, not in the simulator semantics.
