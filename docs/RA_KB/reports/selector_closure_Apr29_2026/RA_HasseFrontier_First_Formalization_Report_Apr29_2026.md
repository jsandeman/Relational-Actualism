# RA Hasse Frontier v1 — First Formalization Report

## Summary

`RA_HasseFrontier_v1.lean` advances the Selector Closure programme from abstract frontier/cut vocabulary to concrete graph reachability.

It imports:

```lean
import RA_FrontierGraphBridge_v1
```

and defines a concrete reachability relation over `GraphVertex G`, proves that reachability is a causal order using the graph's `topo_order`, and proves that a graph-core causal cut is down-closed under full reachability.

## Conservative status

This file is a scaffold / bridge file, not a closure proof.  It contains no executable `sorry`, no `admit`, and no `axiom` in the generated source.

Recommended pre-local-compile status:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After successful local compile and full Lake build, update to:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

or, if warning-free:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom_warning_free
```

## Conceptual contribution

The key result is that the cut/downset bridge no longer needs to remain purely certificate-level:

```lean
theorem cut_down_closed_reachable
```

states that if a vertex lies in the left side of a causal cut, every vertex reachable into it also lies in the left side.  This is the natural graph-native form of candidate-past closure.

The file then packages graph-native downsets as abstract `CandidatePast` values and packages supplied maximal-frontier covers as abstract `Frontier` values.

## Limitations

The file still assumes:

```text
HasseFrontierCover P
```

as data.  It does not yet prove that every finite nonempty downset has such a cover.  That is the next theorem target.

It also does not derive nonzero local charge signs.  It only preserves the conserved-cut zero-boundary-ledger result inherited from the graph-cut theorem.

## Recommended next step

Create:

```text
RA_HasseFrontier_Maximal_v1.lean
```

with finite maximal-element existence for nonempty candidate pasts and the first definition of Hasse boundary links.
