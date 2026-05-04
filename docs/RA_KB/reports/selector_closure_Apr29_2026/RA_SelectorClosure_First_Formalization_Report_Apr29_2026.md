# RA Selector Closure: First Formalization Report

Generated: 2026-04-29

## Result

This packet creates a first Lean formalization of the actualization-selector reframing.

The key conceptual shift is:

```text
old question:
  Which candidate measure should the simulator use?

new question:
  What RA-native selector closes structured potentia into actuality?
```

The Lean file does not prove the substantive Selector Closure Theorem. It proves only safe weak lemmas and provides the vocabulary needed for the theorem ladder.

## Files

```text
lean/RA_ActualizationSelector_v1.lean
formalization_notes/RA_Selector_Closure_Theorem_Ladder_Apr29_2026.md
registry_upserts_selector_v2/*.csv
scripts/apply_selector_v2_upserts.py
```

## What the Lean file proves

The file proves:

1. If an `ActualizationSelector` is given, the selected candidate is unique.
2. If RA constraints determine a unique valid candidate below saturation, then those constraints induce an actualization selector.
3. If a history classifier maps distinct histories to the same structural class, it is not injective and therefore cannot be used to quotient actual histories.
4. Candidate normal forms may express physical equivalence, but only when that equivalence is explicitly part of the formal package.

## What the Lean file deliberately does not prove

It does not prove that RA constraints themselves determine a unique candidate.

That is the hard theorem target:

```text
DAG + structured potentia + BDG + LLC + frontier/incidence + no-history-quotient
  -> unique connected actualization below saturation
  -> severance at saturation
```

## Why this matters

The RAGrowSim runs showed that uniform sampling over parent subsets, closures, or profiles gives different finite-growth ensembles. The correct RA response is not to tune among these measures. The correct response is to identify the graph-native selector, then derive apparent probability as a coarse-grained shadow of relational incompleteness.

## Recommended status

```text
artifact_role: exploratory_formalization_scaffold
verification_status: static_no_sorry_no_admit_no_axiom; local Lean build pending
claim relation: formalization_scaffold_for
```

## Suggested local check

From the RA Lean directory:

```bash
cp <packet>/lean/RA_ActualizationSelector_v1.lean src/RA_AQFT/
cd src/RA_AQFT
lake env lean RA_ActualizationSelector_v1.lean
```

If that succeeds, optionally add a temporary Lake root for local development.

