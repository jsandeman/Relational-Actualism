import RA_HasseFrontier_Maximal_v1

/-!
# RA Hasse Frontier FiniteMax v1

Sixth exploratory Lean scaffold for the Selector Closure programme.

`RA_HasseFrontier_Maximal_v1` proved that a topological-maximum certificate
for each reachable upper past is enough to construct a Hasse-frontier cover.
This file isolates the next finite-data layer:

* represent each reachable upper past by a finite enumerating `Finset`;
* supply a maximum of `topo_order` over that finite enumeration;
* construct the `TopoMaxCertificate` required by the maximal-frontier bridge;
* feed the resulting cover into the boundary-ledger stack.

This still deliberately does **not** prove that every finite candidate past
has such a maximum.  It packages the finite-enumeration theorem target into a
small certificate layer that the next file can discharge using a concrete
`Finset` maximum argument.
-/

namespace RA

/-- A finite enumeration of the reachable upper past of `x` inside candidate
past `P`.

The equivalence field says the finite set is exact: membership in `elems` is
precisely `ReachableUpperPast P x`. -/
structure ReachableUpperPastFinset
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x : GraphVertex G) where
  elems : Finset (GraphVertex G)
  complete : ∀ {v : GraphVertex G}, v ∈ elems ↔ ReachableUpperPast P x v

/-- If `x` is in the candidate past, then the finite reachable-upper-past
enumeration is nonempty. -/
theorem reachableUpperPastFinset_nonempty
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (F : ReachableUpperPastFinset P x)
    (hx : P.contains x) :
    ∃ v : GraphVertex G, v ∈ F.elems := by
  refine ⟨x, ?_⟩
  exact (F.complete).2 (reachableUpperPast_self hx)

/-- A finite maximum certificate for a reachable-upper-past enumeration. -/
structure TopoMaxFromFinsetData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (F : ReachableUpperPastFinset P x) where
  f : GraphVertex G
  f_mem : f ∈ F.elems
  topo_max : ∀ {w : GraphVertex G},
    w ∈ F.elems → G.topo_order w.val ≤ G.topo_order f.val

/-- Finite maximum data over an exact reachable-upper-past enumeration constructs
the `TopoMaxCertificate` used by the maximal-frontier bridge. -/
def topoMaxCertificateOfFinsetData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (F : ReachableUpperPastFinset P x)
    (M : TopoMaxFromFinsetData F) :
    TopoMaxCertificate P x :=
  { f := M.f
    f_upper := (F.complete).1 M.f_mem
    topo_max := by
      intro w hw
      exact M.topo_max ((F.complete).2 hw) }

/-- Candidate-past finite-topological-maximum data: every past vertex has an
exact finite reachable-upper-past enumeration and a topological maximum over it.

This is the certificate layer one step below `TopoMaxFrontierCertificate`. -/
structure FiniteTopoMaxFrontierData
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  upper : ∀ {x : GraphVertex G}, P.contains x → ReachableUpperPastFinset P x
  max : ∀ {x : GraphVertex G} (hx : P.contains x),
    TopoMaxFromFinsetData (upper hx)

/-- Finite topological-maximum data induces the global topological-maximum
frontier certificate. -/
def topoMaxFrontierCertificateOfFiniteData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : FiniteTopoMaxFrontierData P) :
    TopoMaxFrontierCertificate P :=
  { topo_max_above := by
      intro x hx
      exact topoMaxCertificateOfFinsetData (D.upper hx) (D.max hx) }

/-- Finite topological-maximum data induces a maximal-frontier certificate. -/
def maximalCertificateOfFiniteData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : FiniteTopoMaxFrontierData P) :
    MaximalFrontierCertificate P :=
  maximalCertificateOfTopoMax (topoMaxFrontierCertificateOfFiniteData D)

/-- Finite topological-maximum data induces a Hasse-frontier cover. -/
def coverOfFiniteData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : FiniteTopoMaxFrontierData P) :
    HasseFrontierCover P :=
  coverOfMaximalCertificate (maximalCertificateOfFiniteData D)

/-- The frontier induced by finite topological-maximum data. -/
def frontierOfFiniteData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : FiniteTopoMaxFrontierData P) :
    Frontier (graphUniverseState G) (reachableCausalOrder G)
      (candidatePastOfHasse P) :=
  frontierOfHassePast P (coverOfFiniteData D)

/-- Boundary package using a frontier derived from finite topological-maximum
data.  The ledger is still supplied as boundary data; deriving signed incidence
from oriented frontier structure is the later charge-sign theorem. -/
structure FiniteMaxHasseBoundaryPackage
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  data : FiniteTopoMaxFrontierData P
  ledger : BoundaryLedger (candidatePastOfHasse P)
    (frontierOfFiniteData data)

/-- Repackage finite-max boundary data as generic candidate-boundary data. -/
def boundaryDataOfFiniteMaxPackage
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : FiniteMaxHasseBoundaryPackage P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfFiniteData B.data
    ledger := B.ledger }

/-- In the conserved-cut case, finite topological-maximum data for the cut past
feeds the existing graph-cut theorem to obtain a zero-flux boundary ledger. -/
noncomputable def cutBoundaryPackageFromFiniteData
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (D : FiniteTopoMaxFrontierData (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    HasseBoundaryPackage (cutAsHasseCandidatePast G C) :=
  cutHasseBoundaryPackage (G := G) (C := C)
    (coverOfFiniteData D) h_ledger

/-- The boundary ledger induced by a conserved cut and finite topological-maximum
data has seven-value N1 charge.  In this conserved-cut bridge the net value is
zero; nonzero local charge signs remain the oriented-incidence theorem target. -/
theorem cutBoundaryFromFiniteData_qN1_seven
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (D : FiniteTopoMaxFrontierData (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    SevenCharge (cutBoundaryPackageFromFiniteData D h_ledger).ledger.qN1 :=
  (cutBoundaryPackageFromFiniteData D h_ledger).ledger.qN1_seven

/-!
## Hard finite-existence theorem still open

The next file should replace `FiniteTopoMaxFrontierData` with a derived object.
The intended theorem target is:

```text
finite exact enumeration of reachable upper past
  + nonempty reachable upper past
  → TopoMaxFromFinsetData
```

and then, for every finite graph-native candidate past:

```text
finite candidate past
  → FiniteTopoMaxFrontierData
  → TopoMaxFrontierCertificate
  → HasseFrontierCover
```

This will be the first point where the Hasse-frontier cover is derived from
finite DAG data rather than supplied as a certificate.
-/

end RA
