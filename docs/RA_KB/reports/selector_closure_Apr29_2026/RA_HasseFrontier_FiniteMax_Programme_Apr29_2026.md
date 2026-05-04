# RA Hasse Frontier FiniteMax Programme

This note records the next Selector Closure theorem step after the compiled `RA_HasseFrontier_Maximal_v1.lean` scaffold.

## Purpose

`RA_HasseFrontier_Maximal_v1.lean` showed that `TopoMaxCertificate` data is sufficient to produce maximal Hasse-frontier covers. `RA_HasseFrontier_FiniteMax_v1.lean` inserts the finite-enumeration layer below that certificate.

The new vocabulary is:

```text
ReachableUpperPastFinset
TopoMaxFromFinsetData
FiniteTopoMaxFrontierData
```

This lets the theorem ladder say:

```text
finite reachable-upper-past enumeration
  + maximum over topo_order
  → TopoMaxCertificate
  → MaximalFrontierCertificate
  → HasseFrontierCover
```

## Status

This file is still a scaffold. It does not yet prove that the maximum exists for every finite nonempty reachable-upper-past set. Instead, it packages exactly the finite data the next theorem must derive.

## Next target

The next hard file should prove a finite maximum theorem, likely by taking a maximum of `G.topo_order` over a finite exact enumeration of the reachable upper past.
