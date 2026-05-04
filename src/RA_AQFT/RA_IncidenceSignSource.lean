import RA_IncidenceCharge

/-!
# RA Incidence Sign Source v1

Ninth exploratory Lean scaffold for the Selector Closure programme.

`RA_IncidenceCharge_v1` proved the conditional charge theorem: if a
three-direction frontier frame carries deterministic incidence signs in
`{-1,0,+1}`, then the net signed N1 charge lies in the RA seven-value
signature.

This file moves one rung upward.  It does **not** yet derive the physical
orientation of a frontier from the graph.  Instead it formalizes an intermediate
object:

* a frontier orientation chart assigns signs to ordered frontier link endpoints;
* such a chart induces an `IncidenceSignSource` on oriented frontier links;
* the induced sign source deterministically signs three oriented frontier links;
* the resulting three-direction boundary package has seven-value N1 charge.

The hard theorem is now isolated as:

```text
finite Hasse frontier + graph-native orientation/incidence structure
  -> FrontierOrientationChart
```

Once that chart is derived rather than supplied, the charge sign-source becomes
topological rather than sampled.
-/

namespace RA

/-- A deterministic orientation chart for a candidate Hasse frontier.

The chart assigns an incidence sign to an ordered pair of graph vertices.  The
link proof carried by `OrientedFrontierLink` is used later to restrict this
chart to actual oriented frontier links.  This is deliberately deterministic:
there is no probability or sampling field here. -/
structure FrontierOrientationChart
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  signBetween : GraphVertex G → GraphVertex G → IncidenceSign
  orientation_coherent : Prop

/-- A frontier orientation chart induces an incidence sign source on actual
oriented frontier links. -/
def signSourceOfOrientationChart
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (O : FrontierOrientationChart P) : IncidenceSignSource P :=
  { signOf := fun l => O.signBetween l.src l.dst }

/-- Evaluation rule for the induced sign source. -/
theorem signSourceOfOrientationChart_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (O : FrontierOrientationChart P) (l : OrientedFrontierLink P) :
    (signSourceOfOrientationChart O).signOf l = O.signBetween l.src l.dst :=
  rfl

/-- Once a frontier orientation chart is supplied, signs are deterministic. -/
theorem orientationChart_sign_deterministic
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (O : FrontierOrientationChart P) (l : OrientedFrontierLink P) :
    (signSourceOfOrientationChart O).signOf l =
      (signSourceOfOrientationChart O).signOf l :=
  rfl

/-- Three oriented frontier links, before signs are read from the orientation
chart.  This is the graph/topology carrier for the three-direction N1 readout. -/
structure OrientedN1ThreeFrame
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  l0 : OrientedFrontierLink P
  l1 : OrientedFrontierLink P
  l2 : OrientedFrontierLink P

/-- Sign a three-link frontier frame using a deterministic orientation chart. -/
def signedThreeFrameOfOrientationChart
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (O : FrontierOrientationChart P) (F : OrientedN1ThreeFrame P) :
    SignedN1ThreeFrame P :=
  signedThreeFrameOfSource (signSourceOfOrientationChart O) F.l0 F.l1 F.l2

/-- A three-link frame signed by an orientation chart has seven-value N1 charge. -/
theorem signedThreeFrameOfOrientationChart_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (O : FrontierOrientationChart P) (F : OrientedN1ThreeFrame P) :
    SevenCharge (signedThreeFrameOfOrientationChart O F).qN1 :=
  signedN1ThreeFrame_qN1_seven (signedThreeFrameOfOrientationChart O F)

/-- A deterministic oriented incidence boundary.  The remaining hard graph
problem is to construct the chart from intrinsic oriented frontier topology. -/
structure OrientedIncidenceBoundary
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  orientation : FrontierOrientationChart P
  frame : OrientedN1ThreeFrame P
  local_conserved : Prop

/-- Convert an oriented incidence boundary into the three-direction incidence
boundary used in `RA_IncidenceCharge_v1`. -/
def threeDirectionalBoundaryOfOrientation
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : OrientedIncidenceBoundary P) :
    ThreeDirectionalIncidenceBoundary P :=
  { frame := signedThreeFrameOfOrientationChart B.orientation B.frame
    local_conserved := B.local_conserved }

/-- The oriented incidence boundary has seven-value net N1 charge. -/
theorem threeDirectionalBoundaryOfOrientation_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : OrientedIncidenceBoundary P) :
    SevenCharge (threeDirectionalBoundaryOfOrientation B).frame.qN1 :=
  signedN1ThreeFrame_qN1_seven (threeDirectionalBoundaryOfOrientation B).frame

/-- Convert an oriented incidence boundary into a boundary ledger over the
finite graph-derived Hasse frontier. -/
noncomputable def ledgerOfOrientedIncidenceBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : OrientedIncidenceBoundary P) :
    BoundaryLedger (candidatePastOfHasse P) (frontierOfFiniteGraph P) :=
  ledgerOfThreeDirectionalBoundary (threeDirectionalBoundaryOfOrientation B)

/-- The ledger induced by an oriented incidence boundary has seven-value N1
charge. -/
theorem ledgerOfOrientedIncidenceBoundary_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : OrientedIncidenceBoundary P) :
    SevenCharge (ledgerOfOrientedIncidenceBoundary B).qN1 :=
  (ledgerOfOrientedIncidenceBoundary B).qN1_seven

/-- Repackage an oriented incidence boundary as candidate-boundary data in the
selector/frontier layer. -/
noncomputable def boundaryDataOfOrientedIncidenceBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : OrientedIncidenceBoundary P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfFiniteGraph P
    ledger := ledgerOfOrientedIncidenceBoundary B }

/-!
## What remains open

This file does not yet derive `FrontierOrientationChart`.  It proves that such
a deterministic chart is enough to induce the sign source and the seven-value
charge ledger.  The next hard target is:

```text
finite Hasse frontier + RA-native orientation/asymmetry data
  -> FrontierOrientationChart
```

That is the point where the topological ledger rule should meet the existing
causal-orientation and D1 ledger-orientation Lean surfaces.
-/

end RA
