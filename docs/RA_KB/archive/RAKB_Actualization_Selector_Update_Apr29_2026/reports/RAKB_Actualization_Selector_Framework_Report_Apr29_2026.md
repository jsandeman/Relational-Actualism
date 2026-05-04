# RAKB Framework Update: Actualization Selector and Relational Determinacy

Generated: 2026-04-29

## Executive conclusion

The recent RAGrowSim measure-comparison work exposed a genuine kernel-level gap, but the best
interpretation is not that RA needs an arbitrary candidate measure. The stronger RA-native reading is
that the current stochastic-language layer is provisional: the missing object is an **actualization
selector** or **relational completion rule**.

This update therefore reframes the problem:

```text
Old framing:
  choose a probability measure over admitted candidates.

New framing:
  derive the graph-native rule by which structured potentia Π(G) closes into one actualized extension;
  derive apparent probabilities as coarse-grained statistics over incomplete relational descriptions.
```

This is not classical hidden-variable determinism. The proposed reading is **relational determinacy**:
before an interaction, some properties are not hidden but undefined; actualization is the graph event
that makes the relevant relational structure definite.

## Why this is a breakthrough-level reframing

The existing RAKB already contains the ingredients:

- `RA-ONT-001`: finite causal graph ontology;
- `RA-ONT-002`: irreversible actualization;
- `RA-ONT-003`: structured potentia / adjacent possible;
- `RA-KERNEL-001`: four-dimensional BDG acceptance kernel;
- `RA-KERNEL-002`: kernel locality;
- `RA-KERNEL-003`: finite potentia;
- `RA-KERNEL-004`: local selection/frequency-kernel requirement;
- `RA-LLC-001`: Local Ledger Condition;
- `RA-KERNEL-005`: covariance / history-label independence target.

The earlier Axiom-5 language says stochastic actualization, but the current suite also explicitly
marks the Born/frequency law independent of local measure structure as not closed. That makes this
reframing legitimate: the primitive should not be an unexamined random draw.

## Core principles added by this update

### 1. No primitive randomness

RA should not introduce ontic randomness as a primitive mechanism. Apparent randomness must be
derived from unresolved relational structure, inaccessible boundary data, coarse-graining, or ensemble
description.

### 2. Relational determinacy

A property is definite only when the graph contains the relational structure needed to define it.
Actualization is the irreversible inscription of such relational closure into the graph.

### 3. No actual-history quotient

RA may classify histories by BDG profile, motif type, closure, frontier, or incidence data, but it must
not identify distinct actual histories as the same event unless their difference is proven to be purely
representational.

### 4. Selector before measure

The fundamental target is not a free measure over candidates. The target is a graph-native selector or
completion rule:

```text
Selector(G, Π(G), boundary/incidence data) → one actualized extension
```

Probability/frequency laws should then be recovered as coarse-grained shadows of this rule.

## Relation to the simulations

The simulations remain important, but their role changes.

They should not be used to tune an arbitrary measure. They should be used to test candidate selector
principles once those principles are derived from the framework.

The current RAGrowSim evidence showed:

```text
parent-subset, closure, and profile measures produce different finite motif ecologies;
no tested uniform measure matches accepted-conditional independent Poisson in all channels;
parent-subset enumeration creates large representational multiplicities.
```

This motivates the new selector issue, but it does not demote settled claims and does not by itself
choose the correct rule.

## Selector Closure Theorem — programme statement

A sharpened theorem target is now visible:

> **Selector Closure Theorem (programme target).** For any finite, non-saturated RA universe-state
> `U_n = (G_n, Π(G_n))`, the RA-native constraints — causal graph ontology, irreversible actuality,
> structured potentia, BDG admissibility, LLC/frontier incidence, finitary actuality, covariance/no-label
> dependence, and no actual-history quotient — determine a unique next actualization, or else determine
> that connected continuation has failed and a severance/saturation transition is triggered.

This theorem is not yet proven. It is the next critical formalization target.

## Practical impact on RAKB

This packet updates RAKB by adding selector-oriented issues and by revising growth-measure language.
It does **not** modify settled claims, demote Poisson-layer derivations, or promote RAGrowSim results as
claim support.

The new issues are:

```text
RA-OPEN-ACTUALIZATION-SELECTOR-001
RA-OPEN-SELECTOR-CLOSURE-001
RA-OPEN-NO-HISTORY-QUOTIENT-001
RA-OPEN-RELATIONAL-DETERMINACY-001
```

The existing measure/methodology issues are reframed as subordinate to the selector programme.
