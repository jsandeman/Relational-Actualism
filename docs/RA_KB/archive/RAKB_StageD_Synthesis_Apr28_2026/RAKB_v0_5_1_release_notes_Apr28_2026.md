# RAKB v0.5.1 Release Notes

## Status

Release readiness: **ready with caveats**.

Validated core state:

```text
claims=39 issues=12 targets=7 framing=3 archived=2
claim_edges=58 all_dependency_edges=97 artifacts=187 claim_artifact_edges=180
```

Expected auxiliary state after Stage C:

```text
source_text_references=245
restoration_candidates=25
```

## What changed since v0.5

- Lean/formal evidence layer integrated and build-confirmed.
- Python computation layer integrated with relation-typed claim-artifact edges.
- Canonical four-paper TeX suite crosswalked into source-text references.
- Historical over-pruning backlog separated into restoration candidates rather than silently re-promoted.
- D2/HadronMassTriad build status ready for hardening to `lean_build_confirmed_no_sorry`.

## Release caveats

- One interface axiom remains: `CausalGraph : Type`.
- One non-blocking Lean warning remains: unused `hN2` in `RA_D3_CosmologicalExpansion.lean`.
- Python scripts are not yet uniformly CLI-hardened or fully reproduced end-to-end.
- Canonical TeX has no explicit `RA-*` IDs; Stage D supplies a comment insertion plan.

## Do not do in this release

- Do not promote all restoration candidates into `claims.yaml`.
- Do not flatten Python candidate support into proof support.
- Do not treat bridge/cartography scripts as native derivations.
- Do not restore D09-D12 GR/RACL field-equation chain as active native theorem support without a new derivation.
