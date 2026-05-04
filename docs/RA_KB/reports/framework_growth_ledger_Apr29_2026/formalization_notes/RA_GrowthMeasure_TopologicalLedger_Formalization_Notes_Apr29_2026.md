# Formalization Notes: Growth Normal Form and Topological Ledger

Generated: 2026-04-29

## Goal

Turn the current underdetermination into a finite list of Lean/theory tasks.

## Part A — Growth candidate normal form

Define a candidate one-vertex extension by its causal downset/closure, not by an arbitrary
list of explicit parent links.

Suggested objects:

```lean
structure CandidatePast (G : DAG) where
  carrier : Finset G.Vertex
  down_closed : ∀ {u v}, u ≺ v -> v ∈ carrier -> u ∈ carrier

def frontier (P : CandidatePast G) : Finset G.Vertex :=
  {v ∈ P.carrier | ∀ w ∈ P.carrier, ¬ v ≺ w}
```

Target lemmas:

```text
frontier_antichain:
  frontier(P) is an antichain.

closure_from_frontier:
  downward_closure(frontier(P)) = P, under finite past closure assumptions.

bdg_profile_closure_invariant:
  BDG profile of a candidate depends on P, not on redundant parent-subset descriptions.

no_hidden_multiplicity_candidate:
  If two parent descriptions induce the same P and same ledger boundary data,
  they represent the same physical candidate unless explicit shortcut edges are added as
  additional state variables in the native action.
```

## Part B — Measure target

Once the candidate quotient is fixed, define a normalized actualization kernel:

```text
W(P | G) ≥ 0
Σ_P W(P | G) = 1
W(P | G) = 0 if S(P) ≤ 0
```

Candidate families:

```text
uniform_over_closures
uniform_over_frontiers
weight_by_S
weight_by_exp_beta_S
weight_by_BDG_action_functional
```

The key theorem is not a simulation theorem but a governance theorem:

```text
The support and weighting of W must be invariant under graph isomorphism and under
redundant descriptions that do not change closure or ledger boundary data.
```

## Part C — Topological ledger

Define a finite local incidence complex:

```text
C0 = local vertices
C1 = oriented frontier links / cover relations
C2 = branching or winding cells
```

with incidence maps:

```text
∂1 : C1 -> C0
∂2 : C2 -> C1
```

Target equations:

```text
∂1 ∘ ∂2 = 0
div J = 0              -- vertexwise LLC
cut_flux = Σ div J     -- discrete Stokes/cut conservation
```

The signed N1 charge should be an incidence readout:

```text
Q_N1(v) = Σ_{e in frontier(v)} incidence(local_orientation, e)
```

Target conditional theorem:

```text
If rank(frontier_spatial_frame) ≤ 3 and each edge incidence is in {-1,0,+1},
then Q_N1 ∈ {-3,-2,-1,0,+1,+2,+3}.
```

Deeper conjecture:

```text
N2 winding/branching current has an N1 boundary projection, and the electric signature
is the boundary readout of that winding.
```

## Part D — Caution

Do not formalize random signs as the physical rule. Random/EnumerateLLC signs are useful simulator
baselines, but the RA target is graph-induced incidence/orientation.
