# Formalization Notes: Selector Closure Theorem

Generated: 2026-04-29

## 0. Aim

Replace the ambiguous phrase “stochastic actualization” with a precise formal programme:

```text
structured potentia + BDG + LLC + finite frontier/incidence data
  → graph-native selector / relational completion rule
  → apparent probabilities as coarse-grained statistics
```

## 1. Definitions to introduce

### UniverseState

A finite actualized causal DAG together with structured potentia:

```text
U = (G, Π(G))
```

### CandidateExtension

A one-vertex extension of `G`, carrying:

```text
past/closure data
frontier/Hasse boundary
BDG depth profile
LLC ledger boundary data
optional orientation/incidence data
```

### AdmissibleCandidate

A candidate satisfying:

```text
S_BDG > 0
finite actuality
kernel locality
LLC compatibility
```

### ActualHistory

The unique ordered chain of actualization events that produced a vertex/event. Histories may be
classified structurally but not ontologically merged unless the distinction is representational.

### Selector

A graph-native function or relation that identifies one actualization from structured potentia:

```text
Sel(U) = c
```

or, at saturation:

```text
Sel(U) = severance / no unique connected continuation
```

## 2. Weak theorem already easy

If a selector is given as a function from a state to an admissible candidate, then the next actualization
is unique by definition. This is mathematically trivial but useful as a Lean scaffold.

```text
Selector existence ⇒ unique selected candidate
```

## 3. Real theorem target

The nontrivial theorem is not uniqueness once a selector is postulated. The target is:

```text
RA constraints entail a selector.
```

That likely requires a chain of smaller theorems:

1. finite-potentia theorem: admissible candidates are finite;
2. frontier-normal-form theorem: candidate descriptions have canonical boundary/frontier form;
3. no-hidden-multiplicity theorem: redundant descriptions do not create physical weight;
4. incidence-ledger theorem: charge/ledger signs are boundary-incidence readouts;
5. selector-invariance theorem: selector is invariant under graph isomorphism / relabeling;
6. saturation exception theorem: when selectivity collapses, connected continuation fails.

## 4. Proposed theorem statement

```text
Selector Closure Theorem.
Let U=(G,Π(G)) be a finite RA universe-state. If U is below saturation and Π(G) is complete with respect
to BDG admissibility, LLC/frontier incidence, and no-history-quotient constraints, then there exists a
unique RA-native actualization c∈Π(G). If uniqueness fails because the constraints no longer distinguish
a connected continuation, then U is in a saturation/severance regime.
```

## 5. Lean strategy

Create a new exploratory file:

```text
src/RA_AQFT/RA_ActualizationSelector_Scaffold.lean
```

Do not add it to the active Lake roots yet unless it compiles locally.

Recommended stages:

```text
Stage 1: define abstract structures and weak uniqueness theorem.
Stage 2: connect CandidateExtension to existing graph / BDG files.
Stage 3: formalize frontier normal form.
Stage 4: formalize no actual-history quotient.
Stage 5: formulate selector closure as an explicit open theorem target.
```

## 6. Epistemic discipline

Do not claim the Selector Closure Theorem as proven. Current status:

```text
RA-OPEN-SELECTOR-CLOSURE-001
proof_status: open formalization target
support_status: framework-motivated, simulation-motivated
```
