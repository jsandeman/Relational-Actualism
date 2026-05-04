# RA Frontier / Incidence Normal Form Programme — April 29, 2026

## Purpose

This note records the next step after `RA_ActualizationSelector_v1.lean`: moving from an abstract selector scaffold to a frontier/incidence scaffold.

The philosophical correction is now explicit:

```text
RA should not search among arbitrary probability measures.
RA should derive the actualization selector from graph-native structure.
```

The mathematical object needed next is the local boundary object of a candidate actualization.

## The missing object

The previous simulations exposed an apparent ambiguity:

```text
parent subset
closure/downset
frontier
profile
action-weighted class
```

But this ambiguity is not merely computational. It says we have not yet defined what `Π(G)` contains at the level of one-vertex actualization.

The working hypothesis is:

```text
candidate actualization = candidate past/downset + Hasse frontier + boundary incidence/ledger data
```

The raw parent list is not automatically the physical object. It may contain redundant descriptions, unless explicit shortcut links are themselves physical actualizations. This distinction must be formalized rather than assumed.

## Core principles

### No primitive randomness

Apparent probability should arise from incomplete relational description, coarse-graining, inaccessible boundary data, or ensemble description. It should not be inserted as an ontological primitive.

### No actual-history quotient

Actual events are reached through unique histories. Structural classifiers may classify events by motif/profile/closure, but classification does not identify distinct histories unless injectivity or physical-equivalence data is supplied.

### Frontier normal form

A candidate description should be mapped to a normal object:

```text
CandidatePast = causal downset
Frontier      = maximal/Hasse boundary of that downset
Ledger        = incidence/conservation data on the frontier
```

### No hidden multiplicity

If two descriptions have the same frontier-boundary normal form and are physically equivalent, they should not acquire different physical weight merely because one has more redundant descriptions.

## T6/T7 theorem ladder

```text
T6a. CandidatePast/downset definition.
T6b. HasseFrontier definition.
T6c. CandidateBoundaryData = past + frontier + ledger.
T6d. FrontierNormalForm for candidate descriptions.
T6e. No-hidden-multiplicity as normal-form invariance.
T7a. BoundaryLedger with seven-value N1 signature.
T7b. Replace abstract local_conserved with LLC/divergence-free incidence.
T7c. Derive signed N1 charge from oriented frontier incidence.
```

## What the new Lean file proves

`RA_FrontierIncidence_v1.lean` proves only safe conditional lemmas:

```text
same data ⇒ physical equivalence under a supplied normal-form package
physical equivalence ⇒ same data under that package
same data ⇒ same weight under a normal-form-invariant weight package
frontier constraint closure ⇒ abstract selector closure
```

It does not yet derive the hard selector or the charge-sign rule.

## Next concrete formalization target

The next file should connect this scaffold to the existing graph-core files:

```text
RA_FrontierIncidence_Graph_v1.lean
```

Target definitions:

```text
closureOf(parent set)
maximalElements(closure)
frontierOf(candidate)
```

Target theorem:

```text
BDG profile depends on candidate closure/frontier data, not on redundant representation.
```
