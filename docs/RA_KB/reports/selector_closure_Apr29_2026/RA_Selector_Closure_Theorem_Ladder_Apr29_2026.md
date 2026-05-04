# Selector Closure Theorem Ladder

Generated: 2026-04-29

## Thesis

The recent RAGrowSim work exposed a kernel-level question: the fundamental object should not be an arbitrary probability measure over candidates. The stronger RA-native target is an actualization selector:

```text
structured potentia + BDG + LLC + frontier/incidence + no-history-quotient
  -> one connected actualization below saturation
  -> severance when connected selectivity collapses
```

The theorem is not proved yet. This ladder breaks it into formal stages that can be attacked without overclaiming.

## T0. Finite potentia

**Claim.** For a finite actualized graph and a finite one-vertex extension rule, the candidate set is finite.

**Lean target.** Define `UniverseState`, `Potentia`, and `Admissible` as finite objects.

**Status in v1 file.** Scaffolded.

## T1. Selector type

**Claim.** A selector is not a measure. It is a rule returning one admissible candidate.

**Lean target.** Define `ActualizationSelector U Π` with field:

```lean
choose : Admissible Π
```

**Status in v1 file.** Defined.

## T2. Weak selector closure

**Claim.** If a selector is given, the selected candidate is unique.

**Lean target.** Prove:

```lean
theorem selected_candidate_unique
```

**Status in v1 file.** Proved.

## T3. Constraint closure implies selector

**Claim.** If the full RA constraints determine a unique valid candidate below saturation, they induce a selector.

**Lean target.** Package constraints as `CandidateConstraints`, prove:

```lean
def selectorFromClosureData
theorem weak_selector_closure
```

**Status in v1 file.** Proved conditionally.

This is the first rigorous bridge:

```text
unique valid candidate from RA constraints -> selector -> unique selected candidate
```

## T4. No actual-history quotient

**Claim.** Structural classification does not imply ontological identification of actual histories. Equal motif/profile labels do not merge distinct actual histories unless the classifier is proven injective.

**Lean target.** Define `HistoryClassifier` and prove:

```lean
same_class_implies_same_history_of_injective
not_injective_of_classifies_but_does_not_quotient
```

**Status in v1 file.** Proved abstractly.

## T5. Candidate normal form

**Claim.** Candidate descriptions may contain representational redundancy, but distinct actual histories cannot be quotiented unless the redundancy is formally identified.

**Lean target.** Define `CandidateNormalForm` with:

```lean
normalize : Candidate -> Normal
physically_equiv : Candidate -> Candidate -> Prop
equiv_iff_same_normal : physically_equiv c d <-> normalize c = normalize d
```

**Status in v1 file.** Scaffolded with forward/backward lemmas.

## T6. Frontier/incidence normal form

**Claim.** The physical candidate object is likely not a raw parent list; it is a finite local boundary/frontier/incidence object that preserves actual-history distinction while eliminating representational redundancy.

**Lean target.** Replace abstract normal forms with graph-native objects:

```text
CandidatePast
HasseFrontier
BoundaryIncidence
LedgerBoundary
```

**Status.** Not yet formalized.

## T7. Incidence ledger

**Claim.** Charge/ledger signs should be incidence readouts on the local frontier, not sampled labels.

**Lean target.** Define signed incidence on frontier links and prove the seven-value N1 signature conditionally from at most three independent signed directions.

**Status.** Open.

## T8. Hard Selector Closure Theorem

**Target statement.** For any finite, non-saturated RA state, the concrete RA constraints determine a unique connected completion. If the constraints no longer distinguish a connected completion, the outcome is severance.

**Status.** Open; the main kernel theorem programme.

## Practical next Lean step

Add the v1 file as a non-root exploratory source first:

```text
src/RA_AQFT/RA_ActualizationSelector_v1.lean
```

Then test locally. If it compiles, add a temporary Lake root only after review.

