import RA_FrontierGraphBridge

/-!
# RA Hasse Frontier v1

Fourth exploratory Lean scaffold for the Selector Closure programme.

This file begins replacing certificate-style frontier data with graph-native
reachability and Hasse-frontier vocabulary over the concrete `ActualizationGraph`
from `RA_GraphCore.lean`.

It proves only safe structural bridge facts:

* a concrete edge gives a one-step relation between `GraphVertex` values;
* the reflexive/transitive reachability relation is a causal order because every
  concrete edge strictly increases `topo_order`;
* a causal cut is down-closed for reachability, not merely for one-step edges;
* a candidate past can be represented as a graph-native downset;
* a Hasse frontier is the maximal boundary of such a downset, with a cover
  certificate;
* a Hasse frontier can be re-packaged as the abstract `Frontier` used by the
  selector/frontier layer.

This is not the hard Selector Closure Theorem.  It is the next normal-form
bridge: moving from arbitrary parent-list representations toward
closure/frontier objects native to the finite causal graph.
-/

namespace RA

/-- One concrete graph edge from `a` to `b`, restricted to the finite vertex
subtype of an `ActualizationGraph`. -/
def Step (G : _root_.ActualizationGraph) (a b : GraphVertex G) : Prop :=
  ∃ e : _root_.Edge, e ∈ G.E ∧ e.src = a.val ∧ e.dst = b.val

/-- A one-step graph edge strictly increases the graph topological order. -/
theorem step_topo_lt
    (G : _root_.ActualizationGraph) {a b : GraphVertex G}
    (h : Step G a b) :
    G.topo_order a.val < G.topo_order b.val := by
  rcases h with ⟨e, he, hsrc, hdst⟩
  simpa [hsrc, hdst] using G.arrow_of_time e he

/-- Reflexive/transitive reachability through concrete graph edges. -/
inductive Reachable (G : _root_.ActualizationGraph) :
    GraphVertex G → GraphVertex G → Prop where
  | refl (v : GraphVertex G) : Reachable G v v
  | cons {a b c : GraphVertex G} :
      Step G a b → Reachable G b c → Reachable G a c

/-- Reachability is reflexive. -/
theorem reachable_refl
    (G : _root_.ActualizationGraph) (v : GraphVertex G) :
    Reachable G v v :=
  Reachable.refl v

/-- Reachability is transitive. -/
theorem reachable_trans
    {G : _root_.ActualizationGraph} {a b c : GraphVertex G}
    (hab : Reachable G a b) (hbc : Reachable G b c) :
    Reachable G a c := by
  induction hab generalizing c with
  | refl v =>
      exact hbc
  | cons hstep hrest ih =>
      exact Reachable.cons hstep (ih hbc)

/-- If `a` reaches `b`, then either the vertices are equal or topological order
strictly increases. -/
theorem reachable_eq_or_topo_lt
    {G : _root_.ActualizationGraph} {a b : GraphVertex G}
    (h : Reachable G a b) :
    a = b ∨ G.topo_order a.val < G.topo_order b.val := by
  induction h with
  | refl v =>
      exact Or.inl rfl
  | cons hstep hrest ih =>
      have hstep_lt := step_topo_lt G hstep
      rcases ih with hEq | hLt
      · right
        simpa [hEq] using hstep_lt
      · right
        exact Nat.lt_trans hstep_lt hLt

/-- Concrete reachability gives a causal order on the finite vertex subtype. -/
def reachableCausalOrder
    (G : _root_.ActualizationGraph) : CausalOrder (graphUniverseState G) :=
  { le := fun a b => Reachable G a b
    refl := by
      intro v
      exact Reachable.refl v
    trans := by
      intro a b c hab hbc
      exact reachable_trans hab hbc
    antisymm := by
      intro a b hab hba
      have hab' := reachable_eq_or_topo_lt hab
      have hba' := reachable_eq_or_topo_lt hba
      rcases hab' with hEq | hLt
      · exact hEq
      · rcases hba' with hEq' | hLt'
        · exact hEq'.symm
        · exact False.elim (Nat.lt_asymm hLt hLt') }

/-- One-step edges are reachable. -/
theorem step_reachable
    {G : _root_.ActualizationGraph} {a b : GraphVertex G}
    (h : Step G a b) : Reachable G a b :=
  Reachable.cons h (Reachable.refl b)

/-- Concrete graph edges point forward in the reachability causal order. -/
theorem graph_edge_reachable
    (G : _root_.ActualizationGraph) (e : _root_.Edge) (he : e ∈ G.E) :
    (reachableCausalOrder G).le
      ⟨e.src, G.edge_src_mem e he⟩
      ⟨e.dst, G.edge_dst_mem e he⟩ :=
  step_reachable ⟨e, he, rfl, rfl⟩

/-- A causal cut is down-closed for the full reachability relation: if a vertex
in the left side has a reachable predecessor, that predecessor is also in the
left side. -/
theorem cut_down_closed_reachable
    {G : _root_.ActualizationGraph} (C : _root_.CausalCut G)
    {x y : GraphVertex G}
    (hxy : Reachable G x y) (hy : y.val ∈ C.V_L) :
    x.val ∈ C.V_L := by
  induction hxy with
  | refl v =>
      exact hy
  | cons hstep hrest ih =>
      have hb : _ ∈ C.V_L := ih hy
      rcases hstep with ⟨e, he, hsrc, hdst⟩
      have hdstVL : e.dst ∈ C.V_L := by
        simpa [hdst] using hb
      have hsrcVL : e.src ∈ C.V_L := C.no_backward e he hdstVL
      simpa [hsrc] using hsrcVL

/-- The graph-core cut downset certificate derived from full reachability. -/
def cutReachabilityDownsetCertificate
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G) :
    CutDownsetCertificate G C (reachableCausalOrder G) :=
  { down_closed := by
      intro x y hxy hy
      exact cut_down_closed_reachable C hxy hy }

/-- A causal cut gives a candidate past under the concrete reachability order. -/
def candidatePastOfCutReachable
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G) :
    CandidatePast (graphUniverseState G) (reachableCausalOrder G) :=
  candidatePastOfCut G C (reachableCausalOrder G)
    (cutReachabilityDownsetCertificate G C)

/-- A concrete graph-native candidate past: a downset of the reachability order. -/
structure HasseCandidatePast (G : _root_.ActualizationGraph) where
  contains : GraphVertex G → Prop
  down_closed : ∀ {x y : GraphVertex G},
    Reachable G x y → contains y → contains x

/-- Repackage a graph-native downset as the abstract `CandidatePast` used by the
frontier/incidence scaffold. -/
def candidatePastOfHasse
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) :
    CandidatePast (graphUniverseState G) (reachableCausalOrder G) :=
  { contains := P.contains
    down_closed := by
      intro x y hxy hy
      exact P.down_closed hxy hy }

/-- The graph-native candidate past associated with a causal cut. -/
def cutAsHasseCandidatePast
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G) :
    HasseCandidatePast G :=
  { contains := fun v => v.val ∈ C.V_L
    down_closed := by
      intro x y hxy hy
      exact cut_down_closed_reachable C hxy hy }

/-- A vertex is in the Hasse frontier of a candidate past when it is in the past
and no strictly later vertex of the same past is reachable from it.  Equality is
allowed because `Reachable` is reflexive. -/
def IsHasseFrontier
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (v : GraphVertex G) : Prop :=
  P.contains v ∧
    ∀ {w : GraphVertex G}, P.contains w → Reachable G v w → w = v

/-- A cover certificate for a Hasse frontier: every past vertex lies below some
maximal frontier vertex.  This is explicit data in v1; deriving it from finite
nonempty downsets is a later theorem target. -/
def HasseFrontierCover
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) : Prop :=
  ∀ {x : GraphVertex G}, P.contains x →
    ∃ f : GraphVertex G, IsHasseFrontier P f ∧ Reachable G x f

/-- A graph-native Hasse frontier can be repackaged as the abstract `Frontier`
used by the frontier/incidence layer. -/
def frontierOfHassePast
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (cover : HasseFrontierCover P) :
    Frontier (graphUniverseState G) (reachableCausalOrder G)
      (candidatePastOfHasse P) :=
  { isFrontier := fun v => IsHasseFrontier P v
    frontier_in_past := by
      intro v hv
      exact hv.1
    maximal := by
      intro v w hv hw hvw
      exact hv.2 hw hvw
    every_past_below_frontier := by
      intro x hx
      exact cover hx }

/-- Any Hasse frontier vertex lies in the associated candidate past. -/
theorem hasse_frontier_in_past
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {v : GraphVertex G} (hv : IsHasseFrontier P v) :
    P.contains v :=
  hv.1

/-- A Hasse frontier vertex is maximal in its candidate past. -/
theorem hasse_frontier_maximal
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {v w : GraphVertex G}
    (hv : IsHasseFrontier P v) (hw : P.contains w)
    (hvw : Reachable G v w) :
    w = v :=
  hv.2 hw hvw

/-- Boundary package for a graph-native Hasse candidate past.  The ledger is
still supplied as data; deriving it from oriented frontier incidence is the next
charge-sign theorem target. -/
structure HasseBoundaryPackage
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  cover : HasseFrontierCover P
  ledger : BoundaryLedger (candidatePastOfHasse P)
    (frontierOfHassePast P cover)

/-- Repackage graph-native Hasse boundary data as generic candidate-boundary
data. -/
def boundaryDataOfHassePackage
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : HasseBoundaryPackage P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfHassePast P B.cover
    ledger := B.ledger }

/-- In the conserved-cut case, a supplied Hasse cover for the cut past lets us
reuse the existing graph-cut frontier bridge to obtain a zero-flux boundary
ledger. -/
noncomputable def cutHasseBoundaryPackage
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (cover : HasseFrontierCover (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    HasseBoundaryPackage (cutAsHasseCandidatePast G C) :=
  { cover := cover
    ledger :=
      { qN1 := cutBoundaryCharge G C
        qN1_seven := by
          rw [cutBoundaryCharge_zero G C h_ledger]
          exact zero_sevenCharge
        local_conserved := cutBoundaryCharge G C = 0 } }

/-- The boundary ledger induced by a conserved causal cut has seven-value N1
charge.  Here the charge is zero; nonzero local signs remain the incidence
sign-source target. -/
theorem cutHasseBoundary_qN1_seven
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (cover : HasseFrontierCover (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    SevenCharge (cutHasseBoundaryPackage cover h_ledger).ledger.qN1 :=
  (cutHasseBoundaryPackage cover h_ledger).ledger.qN1_seven

/-!
## What remains hard

This file proves that concrete graph reachability supplies a causal order and
that causal cuts are down-closed for that order.  It still assumes a Hasse
frontier cover certificate.  The next theorem target is to derive such covers
from finite nonempty graph downsets, and then to define oriented incidence signs
on the resulting frontier.

The likely next file is:

```text
RA_HasseFrontier_Maximal_v1.lean
```

with goals:

* prove maximal-frontier existence for finite nonempty candidate pasts;
* define frontier links / Hasse boundary links;
* begin deriving signed incidence coefficients from oriented frontier data.
-/

end RA
