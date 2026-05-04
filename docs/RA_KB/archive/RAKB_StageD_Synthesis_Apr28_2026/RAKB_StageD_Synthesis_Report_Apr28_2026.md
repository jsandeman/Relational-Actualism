# RAKB Stage D Synthesis and v0.5.1 Release Readiness Report

Generated: 2026-04-28

## Executive conclusion

RAKB is ready to be treated as a **v0.5.1 release candidate**. The core registry validates after Lean, Python, and paper-audit integration:

```text
claims=39 issues=12 targets=7 framing=3 archived=2
claim_edges=58 all_dependency_edges=97 artifacts=187 claim_artifact_edges=180
```

Stage D does **not** find a structural blocker. It finds four release caveats that should be kept visible rather than hidden:

1. the formal Lean layer builds successfully with no sorry/admit, but one interface axiom remains (`CausalGraph : Type`);
2. the Lake build still has one unused-variable warning in `RA_D3_CosmologicalExpansion.lean`;
3. the Python layer is source-audited and partially smoke-tested, not fully reproduced end-to-end;
4. the canonical TeX suite still has zero explicit `RA-*` IDs, so paper-to-registry mapping is currently curated rather than deterministic.

## Post-Stage-C working state

The validator counts only the core registry tables. After applying the Stage C source-text/restoration upserts, the expected auxiliary layer is:

```text
source_text_references = 245
restoration_candidates = 25
```

These tables are essential for paper synchronization and restoration governance even though they do not change the structural validator headline counts.

## Evidence layer health

| Layer | Stage D status | Notes |
|---|---:|---|
| Lean/formal | pass with caveats | Active Lake closure builds; no sorry/admit; one interface axiom; one warning. |
| Python/computation | pass with reproducibility debt | 61 Python artifacts integrated and 116 claim-artifact edges added in Stage B. Relation types must be preserved. |
| Canonical TeX | pass with determinism gap | 113 sections scanned; 83 mapped; no explicit `RA-*` IDs in TeX. |
| Historical restoration | governed backlog | D09-D51 family assessed; 25 restoration candidates now expected after Stage C. |
| Registry graph | pass | Claim graph remains acyclic and structurally valid. |

## Support-tier distribution

```json
{
  "candidate_or_phenomenology_support": 22,
  "formal_or_lean_support": 18,
  "textual_only_needs_artifact_or_caveat": 13,
  "textual_foundation": 5,
  "formal_support_bridge_reviewed": 1,
  "artifact_linked_but_weakly_typed": 1,
  "unprojected_or_unlinked": 1
}
```

The key interpretation is that RAKB now records several distinct evidence classes. Do not collapse them into a generic `supports` relation. A Lean theorem, a deterministic enumerator, a phenomenology script, and a bridge/cartography note are different kinds of evidence.

## Gap class distribution

```json
{
  "paper_projected_open_or_framing_no_artifact_required_but_track": 8,
  "paper_projected_foundation_no_artifact_needed": 5,
  "paper_projected_textual_only_claim": 5,
  "source_backed_no_canonical_text_projection": 2,
  "not_in_paper_crosswalk_and_no_artifact_edge": 1,
  "registry_release_hardening": 1,
  "lean_hygiene": 1,
  "formal_boundary": 1,
  "paper_crosswalk_determinism": 1,
  "python_reproducibility": 1
}
```

The two most important node-level gaps are:

- `RA-MOTIF-005`: source-backed but not yet projected in canonical TeX crosswalk;
- `RA-NONTARGET-002`: framing policy with source support but no canonical TeX projection.

The most important systemic gap is the absence of explicit RAKB IDs in TeX. This is not a physics problem, but it is a reproducibility problem for future paper audits.

## High-priority promotion/restoration decisions

The queue includes 25 restoration candidates. Stage D prioritizes these as near-term decisions:

- `RA-KIN-BANDWIDTH-001` — decide whether c-as-bandwidth becomes a claim or remains a kinematic candidate.
- `RA-KIN-PROPER-TIME-001` — decide whether proper time as actualization count becomes a claim.
- `RA-D4-CASCADE-001` — decide whether d=4 cascade-exponent uniqueness is an active arithmetic/matter claim or target.
- `RA-GRAV-SINGULARITY-001` — keep as caveated gravitational corollary or map into existing severance claims.
- `RA-MATTER-HADRON-TRIAD-001` — formal source exists and now builds, but it needs an exact claim statement before promotion.

## D2/HadronMassTriad hardening

The current registry snapshot still carries a conservative “pending fresh log” status for `RA_D2_HadronMassTriad.lean`. The Stage C bundle includes the fresh D2-root build log, so Stage D provides a v0.5.1 upsert to harden that status to:

```text
lean_build_confirmed_no_sorry
```

This should still be worded as candidate support for `RA-PRED-002`, not a complete proton-mass derivation.

## v0.5.1 release recommendation

Make a small release commit containing:

1. the already-applied Stage C source-text and restoration-candidate updates;
2. this Stage D report packet;
3. the D2 build-status hardening upsert;
4. optionally, the one-line Lean warning patch;
5. no promotion of restoration candidates into `claims.yaml` yet.

Recommended tag after validation:

```bash
git tag rakb-v0.5.1-source-backed
```

Suggested release description:

> RAKB v0.5.1 is the first source-backed RA knowledge-base release integrating the active Lean build surface, Python computation layer, canonical four-paper TeX crosswalk, and historical restoration backlog. It is structurally valid and release-ready with explicit caveats on the remaining interface axiom, one Lean warning, Python reproducibility debt, and TeX crosswalk determinism.
