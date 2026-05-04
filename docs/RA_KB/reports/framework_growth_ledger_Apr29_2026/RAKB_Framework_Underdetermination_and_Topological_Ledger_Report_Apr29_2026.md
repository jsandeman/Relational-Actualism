# RAKB Framework Analysis: Growth Measure and Ledger Rule Underdetermination

Generated: 2026-04-29

## Executive conclusion

The current simulations are not showing that RA is a guessing game. They are showing that the
current formal framework has not yet specified a **candidate equivalence relation** and a
**normalized actualization measure**.

The BDG action currently tells us which local profiles are admissible or favored. The LLC tells us
which ledger flows are conserved. Neither, by itself, tells us which finite graph extensions count
as distinct physical alternatives, nor how to assign probabilities among admitted alternatives.

That is why the rule feels underdetermined.

The important point is that this underdetermination is localizable. It is not a global failure of
RA. It is concentrated in four missing theory objects:

1. the RA-native sample space of one-vertex extensions;
2. the equivalence relation among redundant representations of a causal extension;
3. the normalized actualization kernel over that quotient;
4. the finite incidence/orientation rule that sources signed ledger contributions.

## Why the rule is underdetermined right now

### 1. The BDG action is a filter/kernel input, not yet a measure

For a candidate vertex with profile `(N1,N2,N3,N4)`, the d=4 BDG score is

```text
S = 1 - N1 + 9 N2 - 16 N3 + 8 N4.
```

The simulator can use `S > 0` as an acceptance filter. But `S > 0` does not determine whether the
actualization measure is:

```text
uniform over admitted candidates,
uniform over causal closures,
uniform over profile classes,
weighted by S,
weighted by exp(beta S),
or something else.
```

This is already anticipated by the existing issue `RA-KERNEL-004`, which says RA requires a
normalized local selection weight on admissible one-vertex extensions.

### 2. Parent subsets, closures, and frontiers are not equivalent sample spaces

The current simulator makes the parent set explicit. But the BDG profile only sees the induced
causal past/closure. This creates a hidden multiplicity problem: many explicit parent subsets can
represent the same closure or the same profile.

The latest candidate-measure diagnostics show that this effect is large. At step 25, averaged over
the diagnostic runs:

```text
total parent subsets:                 22594
admitted parent subsets:              9578
unique closures:                      850
admitted unique closures:             419
unique profiles:                      152
admitted unique profiles:             77
mean admitted closure multiplicity:   27.61
max admitted closure multiplicity:    676.41
```

So `uniform over parent subsets` is not a neutral choice. It strongly weights structures with many
redundant parent-set representations.

### 3. The LLC is conservation, not a sign-source

The Local Ledger Condition says that ledger quantities balance locally and therefore across cuts.
It does not by itself say whether a particular incoming edge contributes `+1`, `0`, or `-1` to the
signed N1 charge.

The current source layer supports the seven-value signature

```text
Q_N1 ∈ {-3,-2,-1,0,+1,+2,+3}
```

but the function

```text
s(edge, local_context) -> {-1,0,+1}
```

is still open. This is why `EnumerateLLC` is a bookkeeping baseline, not a physical rule.

### 4. The scalar profile loses orientation data

The BDG profile `(N1,N2,N3,N4)` is scalar and interval-cardinality based. Charge signs, however,
require orientation/incidence information. If charge is topological, its sign cannot be recovered
from the unsigned profile alone. It must be recovered from an oriented local star, frontier, cut, or
finite incidence complex.

### 5. Poisson-CSG is not the primitive dynamics

The corrected simulation comparison uses accepted-conditional Poisson,

```text
E[N_k | μ, S > 0],
```

not raw Poisson. Even after this correction, the tested finite-growth measures do not match
accepted-conditional independent Poisson channel-by-channel.

Using the `mu_v4` estimator, the weighted simulator/accepted-Poisson ratios for the current
parent-subset-uniform run are:

```text
N1 ratio: 1.019
N2 ratio: 0.838
N3 ratio: 1.258
N4 ratio: 1.332
S  ratio: 0.771
```

The implication is not that Poisson-based paper results are wrong. The implication is that the
regime and candidate measure under which Poisson is a valid effective ensemble must be derived,
not assumed.

## Would analysis of the current framework reveal something simulations do not?

Yes. Simulations can only test a measure after we choose one. They cannot determine the physical
equivalence relation for us.

The current framework can impose non-negotiable constraints:

### A. Isomorphism / covariance constraint

The measure should factor through unlabeled causal-graph isomorphism classes. Otherwise label
history affects physics.

### B. No-hidden-multiplicity constraint

If two candidate descriptions induce the same causal closure, the same BDG profile, and the same
ledger boundary data, then counting them with different multiplicity introduces hidden state not
seen by the action or observables.

This suggests a principle:

```text
If explicit shortcut edges are not independently observable, quotient them.
```

Or contrapositively:

```text
If explicit shortcut edges are physical, the native action/ledger must include them.
```

### C. Hasse/frontier normal form

A natural RA-normal form is:

```text
candidate actualization = finite causal downset P
direct parent frontier = Max(P)
```

The direct parent set is then the Hasse frontier of the closure, not an arbitrary subset. This
eliminates many redundant parent-set representations and restores the meaning of "immediate
predecessor."

This does not by itself force Poisson statistics, but it removes a major artificial degree of
freedom.

### D. Local-to-global ledger/Stokes constraint

The charge rule should be compatible with the already-established local-to-cut structure of LLC.
The natural mathematical form is a finite incidence/cochain rule:

```text
local oriented incidence structure
  -> signed N1 boundary contributions
  -> divergence-free ledger current
  -> cut conservation
```

This is topological in the finite graph sense.

### E. Continuum/effective Poisson constraint

Poisson-CSG should be treated as a candidate effective or mean-field ensemble. The framework should
derive when finite RA growth approximates it, rather than making raw Poisson the primitive
dynamics.

## Best current hypothesis

The most RA-native route is:

```text
1. Candidate extensions are closures/downsets.
2. Direct parents are the Hasse frontier Max(P).
3. The stochastic actualization kernel is defined over this quotient, probably with BDG action weighting.
4. Ledger signs are incidence numbers on an oriented local frontier/cut.
5. N2 winding/branching is the deeper strong/baryonic channel.
6. N1 electric charge is a boundary projection/readout of that oriented incidence structure.
```

This makes charge assignment emergent from topology plus local orientation, not an extra random
variable.

## What the RAKB update does

This packet adds or updates issues only. It does not modify settled claims.

Recommended issue additions:

```text
RA-OPEN-GROWTH-MEASURE-001
RA-OPEN-FRONTIER-NORMAL-FORM-001
RA-OPEN-POISSON-DYNAMICS-001
RA-OPEN-MU-ESTIMATOR-001
RA-OPEN-GROWTH-KERNEL-WEIGHT-001
RA-OPEN-CHARGE-SIGN-001
RA-OPEN-TOPOLOGICAL-LEDGER-001
```

These issues preserve the current insight without prematurely demoting or promoting any major RA
claim.

## Immediate next work

1. Test action-weighted closure/profile measures.
2. Formalize closure/downset and Hasse frontier normal form in Lean.
3. Prove BDG profile closure-invariance.
4. State and test a no-hidden-multiplicity principle.
5. Formalize conditional seven-value charge range from a signed local frame.
6. Attempt the finite incidence/cochain derivation of the ledger sign rule.
