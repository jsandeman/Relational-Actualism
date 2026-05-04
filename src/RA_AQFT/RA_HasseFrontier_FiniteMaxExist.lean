import RA_HasseFrontier_FiniteMax

/-!
# RA Hasse Frontier FiniteMaxExist v1

Seventh exploratory Lean scaffold for the Selector Closure programme.

`RA_HasseFrontier_FiniteMax_v1` packaged finite enumeration data and a supplied
maximum over each reachable upper past.  This file proves the first genuine
finite-existence step:

* every reachable upper past in a finite `ActualizationGraph` can be enumerated
  by filtering the finite graph-vertex set;
* every nonempty finite reachable upper past has a vertex maximizing
  `topo_order`;
* therefore every graph-native candidate past has finite topological-maximum
  frontier data;
* therefore Hasse-frontier covers can be constructed from finite graph data,
  rather than supplied as certificate data.

This still does **not** prove the hard Selector Closure Theorem.  It closes the
finite-maximal-frontier existence rung needed before the later incidence-sign
and selector-closure rungs.
-/

namespace RA

/-- Exact finite enumeration of the reachable upper past of `x` inside `P`,
obtained by filtering the finite vertex set of the actualization graph.

This is the first point where the finite nature of `ActualizationGraph.V` is
used to replace a supplied enumeration certificate. -/
noncomputable def reachableUpperPastFinsetOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x : GraphVertex G) :
    ReachableUpperPastFinset P x := by
  classical
  letI : Fintype (GraphVertex G) := graphVertexFintype G
  exact
    { elems := Finset.univ.filter (fun v => ReachableUpperPast P x v)
      complete := by
        intro v
        simp }

/-- A nonempty finite reachable-upper-past enumeration has a vertex maximizing
`topo_order`.

The proof maps the finite set of vertices to the finite set of their
`topo_order` values, takes the maximum natural number, and pulls back a vertex
attaining that value. -/
noncomputable def topoMaxFromReachableUpperPastFinset
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (F : ReachableUpperPastFinset P x)
    (hx : P.contains x) :
    TopoMaxFromFinsetData F := by
  classical
  let vals : Finset Nat := F.elems.image (fun v => G.topo_order v.val)
  have hvals_nonempty : vals.Nonempty := by
    rcases reachableUpperPastFinset_nonempty F hx with ⟨v, hv⟩
    exact ⟨G.topo_order v.val, by
      exact Finset.mem_image.mpr ⟨v, hv, rfl⟩⟩
  let m : Nat := vals.max' hvals_nonempty
  have hm_mem : m ∈ vals := by
    simpa [m] using Finset.max'_mem vals hvals_nonempty
  -- We are constructing data in `Type`, so we cannot `rcases` an existential
  -- proof directly.  Use classical choice to pick a vertex attaining the
  -- maximum topo-order value.
  have h_img : ∃ f ∈ F.elems, G.topo_order f.val = m :=
    Finset.mem_image.mp hm_mem
  let f : GraphVertex G := Classical.choose h_img
  have hf_spec : f ∈ F.elems ∧ G.topo_order f.val = m :=
    Classical.choose_spec h_img
  have hf_mem : f ∈ F.elems := hf_spec.1
  have hf_eq : G.topo_order f.val = m := hf_spec.2
  refine
    { f := f
      f_mem := hf_mem
      topo_max := ?_ }
  intro w hw
  have hw_mem : G.topo_order w.val ∈ vals := by
    exact Finset.mem_image.mpr ⟨w, hw, rfl⟩
  have hle : G.topo_order w.val ≤ m := by
    simpa [m] using Finset.le_max' vals (G.topo_order w.val) hw_mem
  simpa [hf_eq] using hle

/-- Finite graph data alone gives the finite-topological-maximum frontier data
for any graph-native candidate past. -/
noncomputable def finiteTopoMaxFrontierDataOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    FiniteTopoMaxFrontierData P :=
  { upper := fun {x} _hx => reachableUpperPastFinsetOfFiniteGraph P x
    max := fun {x} hx =>
      topoMaxFromReachableUpperPastFinset
        (reachableUpperPastFinsetOfFiniteGraph P x) hx }

/-- A graph-native candidate past has a derived topological-maximum frontier
certificate. -/
noncomputable def topoMaxFrontierCertificateOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    TopoMaxFrontierCertificate P :=
  topoMaxFrontierCertificateOfFiniteData
    (finiteTopoMaxFrontierDataOfFiniteGraph P)

/-- A graph-native candidate past has a derived maximal-frontier certificate. -/
noncomputable def maximalCertificateOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    MaximalFrontierCertificate P :=
  maximalCertificateOfFiniteData (finiteTopoMaxFrontierDataOfFiniteGraph P)

/-- A graph-native candidate past has a derived Hasse-frontier cover. -/
noncomputable def coverOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    HasseFrontierCover P :=
  coverOfFiniteData (finiteTopoMaxFrontierDataOfFiniteGraph P)

/-- The frontier derived directly from finite graph data. -/
noncomputable def frontierOfFiniteGraph
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    Frontier (graphUniverseState G) (reachableCausalOrder G)
      (candidatePastOfHasse P) :=
  frontierOfHassePast P (coverOfFiniteGraph P)

/-- Boundary package whose frontier is derived from finite graph data.  The
ledger is still supplied as boundary data; deriving signed incidence values is
reserved for the charge-sign theorem. -/
structure FiniteGraphHasseBoundaryPackage
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  ledger : BoundaryLedger (candidatePastOfHasse P)
    (frontierOfFiniteGraph P)

/-- Repackage finite-graph Hasse boundary data as generic candidate-boundary
information for the selector/frontier layer. -/
noncomputable def boundaryDataOfFiniteGraphPackage
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : FiniteGraphHasseBoundaryPackage P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfFiniteGraph P
    ledger := B.ledger }

/-- In the conserved-cut case, finite graph data alone gives the Hasse cover
needed to feed the existing graph-cut theorem into the boundary-ledger stack. -/
noncomputable def cutBoundaryPackageFromFiniteGraph
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    HasseBoundaryPackage (cutAsHasseCandidatePast G C) :=
  cutHasseBoundaryPackage
    (coverOfFiniteGraph (cutAsHasseCandidatePast G C)) h_ledger

/-- The boundary ledger induced by a conserved cut and finite graph-derived
Hasse frontier has seven-value N1 charge.  In this conserved-cut bridge the net
charge is zero; nonzero local charge signs remain the oriented-incidence target. -/
theorem cutBoundaryFromFiniteGraph_qN1_seven
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    SevenCharge (cutBoundaryPackageFromFiniteGraph h_ledger).ledger.qN1 :=
  (cutBoundaryPackageFromFiniteGraph h_ledger).ledger.qN1_seven

/-!
## What remains open

This file closes the finite maximum existence step for graph-native candidate
pasts, using the finite graph vertex set.  The next target is not another
maximum-existence certificate; it is the incidence-sign theorem:

```text
finite Hasse frontier + oriented boundary/incidence structure
  → signed N1 edge contributions
  → seven-value charge as boundary projection
```

That is where the selector programme meets the topological ledger rule.
-/

end RA
