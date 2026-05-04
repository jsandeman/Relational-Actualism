import RA_HasseFrontier_v1

/-!
# RA Hasse Frontier Maximal v1

Fifth exploratory Lean scaffold for the Selector Closure programme.

This file advances the graph-native frontier construction one rung beyond
`RA_HasseFrontier_v1`.  The previous file defined reachability, graph-native
candidate pasts, and Hasse-frontier covers as explicit data.  This file
formalizes the **maximality certificate** that should eventually be derived
from finite nonempty downsets.

The core idea is:

* for every vertex `x` in a candidate past, choose a reachable vertex `f` above
  `x` that is topologically maximal among reachable past vertices;
* such an `f` is a Hasse-frontier vertex;
* therefore topological maximality certificates produce Hasse-frontier covers;
* those covers can feed the existing boundary-ledger / selector-frontier stack.

This file still does **not** prove the full finite-existence theorem.  It proves
that the right certificate is sufficient.  The next hard step is to derive the
certificate from finite graph data, likely via a `Finset`/maximum argument over
reachable vertices in a finite candidate past.
-/

namespace RA

/-- The part of a candidate past reachable above a chosen past vertex `x`. -/
def ReachableUpperPast
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x v : GraphVertex G) : Prop :=
  P.contains v ∧ Reachable G x v

/-- If `x` lies in a candidate past, then `x` itself lies in its reachable upper
past, by reflexivity of reachability. -/
theorem reachableUpperPast_self
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (hx : P.contains x) :
    ReachableUpperPast P x x :=
  ⟨hx, Reachable.refl x⟩

/-- A vertex `f` is a maximal reachable vertex above `x` inside a candidate
past when every same-past vertex reachable from `f` is equal to `f`.

This is the graph-native object that should eventually be derived from finite
nonempty downsets. -/
structure MaximalReachableAbove
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x : GraphVertex G) where
  f : GraphVertex G
  f_in_past : P.contains f
  x_reaches_f : Reachable G x f
  maximal : ∀ {w : GraphVertex G}, P.contains w → Reachable G f w → w = f

/-- A maximal reachable-above witness is a Hasse-frontier vertex. -/
theorem maximalReachableAbove_isFrontier
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (M : MaximalReachableAbove P x) :
    IsHasseFrontier P M.f :=
  ⟨M.f_in_past, by
    intro w hw hfw
    exact M.maximal hw hfw⟩

/-- A global maximal-frontier certificate: every past vertex has a maximal
reachable frontier vertex above it. -/
structure MaximalFrontierCertificate
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  exists_above : ∀ {x : GraphVertex G}, P.contains x → MaximalReachableAbove P x

/-- A maximal-frontier certificate gives the cover condition required by
`frontierOfHassePast`. -/
def coverOfMaximalCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (M : MaximalFrontierCertificate P) : HasseFrontierCover P := by
  intro x hx
  let W := M.exists_above hx
  exact ⟨W.f, maximalReachableAbove_isFrontier W, W.x_reaches_f⟩

/-- The frontier induced by a maximal-frontier certificate. -/
def frontierOfMaximalCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (M : MaximalFrontierCertificate P) :
    Frontier (graphUniverseState G) (reachableCausalOrder G)
      (candidatePastOfHasse P) :=
  frontierOfHassePast P (coverOfMaximalCertificate M)

/-- A frontier vertex produced by a maximal-frontier certificate lies in the
candidate past. -/
theorem maximalCertificate_frontier_in_past
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (M : MaximalFrontierCertificate P) {v : GraphVertex G}
    (hv : (frontierOfMaximalCertificate M).isFrontier v) :
    P.contains v :=
  hv.1

/-- A frontier vertex produced by a maximal-frontier certificate is maximal in
its candidate past. -/
theorem maximalCertificate_frontier_maximal
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (M : MaximalFrontierCertificate P) {v w : GraphVertex G}
    (hv : (frontierOfMaximalCertificate M).isFrontier v)
    (hw : P.contains w) (hvw : Reachable G v w) :
    w = v :=
  hv.2 hw hvw

/-- A topological maximum certificate for the reachable upper past of `x`.

This is the certificate we expect to derive from finite nonempty graph data: `f`
is in the reachable upper past of `x`, and every other reachable upper-past
vertex has topological order no larger than `f`. -/
structure TopoMaxCertificate
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    (x : GraphVertex G) where
  f : GraphVertex G
  f_upper : ReachableUpperPast P x f
  topo_max : ∀ {w : GraphVertex G},
    ReachableUpperPast P x w → G.topo_order w.val ≤ G.topo_order f.val

/-- A topological maximum in the reachable upper past constructs maximal reachable
frontier data.

This returns a structure, not a proposition, so it must be a `def` rather than
a `theorem` in Lean.  The proof term still uses the strict topological increase
along nontrivial reachability: if `f` reached a strictly later `w`, maximality of
`f`'s `topo_order` would be contradicted. -/
def maximalReachableAboveOfTopoMax
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    {x : GraphVertex G} (T : TopoMaxCertificate P x) :
    MaximalReachableAbove P x :=
  { f := T.f
    f_in_past := T.f_upper.1
    x_reaches_f := T.f_upper.2
    maximal := by
      intro w hw hfw
      have hxw : ReachableUpperPast P x w :=
        ⟨hw, reachable_trans T.f_upper.2 hfw⟩
      have hle : G.topo_order w.val ≤ G.topo_order T.f.val :=
        T.topo_max hxw
      have hreach := reachable_eq_or_topo_lt hfw
      rcases hreach with hEq | hLt
      · exact hEq.symm
      · exact False.elim (Nat.not_lt_of_ge hle hLt) }

/-- A global topological-maximum certificate: every past vertex has a topological
maximum in its reachable upper past. -/
structure TopoMaxFrontierCertificate
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  topo_max_above : ∀ {x : GraphVertex G}, P.contains x → TopoMaxCertificate P x

/-- Topological maximum certificates induce maximal-frontier certificates. -/
def maximalCertificateOfTopoMax
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (T : TopoMaxFrontierCertificate P) : MaximalFrontierCertificate P :=
  { exists_above := by
      intro x hx
      exact maximalReachableAboveOfTopoMax (T.topo_max_above hx) }

/-- Topological maximum certificates induce Hasse-frontier covers. -/
def coverOfTopoMaxCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (T : TopoMaxFrontierCertificate P) : HasseFrontierCover P :=
  coverOfMaximalCertificate (maximalCertificateOfTopoMax T)

/-- The frontier induced by topological maximum certificates. -/
def frontierOfTopoMaxCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (T : TopoMaxFrontierCertificate P) :
    Frontier (graphUniverseState G) (reachableCausalOrder G)
      (candidatePastOfHasse P) :=
  frontierOfHassePast P (coverOfTopoMaxCertificate T)

/-- Boundary package for a graph-native candidate past whose Hasse frontier is
obtained from maximality certificates.  The ledger remains supplied data; the
next charge-sign step is to derive it from oriented frontier incidence. -/
structure MaximalHasseBoundaryPackage
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  certificate : MaximalFrontierCertificate P
  ledger : BoundaryLedger (candidatePastOfHasse P)
    (frontierOfMaximalCertificate certificate)

/-- Repackage maximal-Hasse boundary data as generic candidate-boundary data. -/
def boundaryDataOfMaximalHassePackage
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : MaximalHasseBoundaryPackage P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfMaximalCertificate B.certificate
    ledger := B.ledger }

/-- In the conserved-cut case, a maximal-frontier certificate for the cut past
lets us reuse the graph-cut theorem to obtain a zero-flux boundary ledger. -/
noncomputable def cutBoundaryPackageFromMaximal
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (M : MaximalFrontierCertificate (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    HasseBoundaryPackage (cutAsHasseCandidatePast G C) :=
  cutHasseBoundaryPackage (G := G) (C := C)
    (coverOfMaximalCertificate M) h_ledger

/-- The boundary ledger induced by a conserved cut and a maximal-frontier
certificate has seven-value N1 charge.  As before, this conserved-cut value is
zero; nonzero local signs remain the incidence sign-source target. -/
theorem cutBoundaryFromMaximal_qN1_seven
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    (M : MaximalFrontierCertificate (cutAsHasseCandidatePast G C))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    SevenCharge (cutBoundaryPackageFromMaximal M h_ledger).ledger.qN1 :=
  (cutBoundaryPackageFromMaximal M h_ledger).ledger.qN1_seven

/-!
## Hard theorem still open

The central finite-existence theorem is intentionally not asserted here:

```text
finite nonempty candidate past
  → TopoMaxFrontierCertificate
  → MaximalFrontierCertificate
  → HasseFrontierCover
```

The present file proves the second and third arrows.  The next proof step is to
construct `TopoMaxCertificate P x` from finite graph data, probably by taking a
maximum of `G.topo_order` over the finite set of vertices satisfying
`ReachableUpperPast P x`.

That future theorem will be the first real bridge from finite DAG structure to a
derived Hasse frontier, rather than a supplied frontier certificate.
-/

end RA
