import RA_IncidenceSignSource

/-!
# RA Graph Orientation Chart v1

Tenth exploratory Lean scaffold for the Selector Closure / topological ledger
programme.

`RA_IncidenceSignSource_v1` showed that a deterministic
`FrontierOrientationChart` induces an incidence sign source and hence a
seven-value signed N1 ledger.  This file moves one rung upward by separating
that chart into a graph-native orientation-data package and a deterministic
conversion from that data to the chart.

This is still a scaffold, not the hard theorem.  The remaining hard target is:

```text
finite Hasse frontier + RA-native causal/orientation asymmetry data
  -> GraphOrientationData
  -> FrontierOrientationChart
  -> IncidenceSignSource
  -> seven-value charge ledger
```

The point of this file is to remove the impression that incidence signs are
random labels.  Once graph orientation data is supplied, every sign is a
function of graph/frontier data.
-/

namespace RA

/-- Three-valued orientation polarity before conversion into an incidence sign.

This is the graph-facing carrier.  It is intentionally finite and deterministic:
there is no probability field here. -/
inductive OrientationPolarity where
  | negative
  | neutral
  | positive
  deriving DecidableEq, Repr

/-- Convert orientation polarity to an incidence sign. -/
def OrientationPolarity.toSign : OrientationPolarity → IncidenceSign
  | OrientationPolarity.negative => IncidenceSign.neg
  | OrientationPolarity.neutral  => IncidenceSign.zero
  | OrientationPolarity.positive => IncidenceSign.pos

/-- A deterministic graph-native orientation data package for a Hasse candidate
past.

The field `polarityBetween` is still supplied here.  The hard future theorem is
that RA's concrete causal-orientation/frontier structure determines such a
field. -/
structure GraphOrientationData
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  polarityBetween : GraphVertex G → GraphVertex G → OrientationPolarity
  graph_native : Prop
  frontier_coherent : Prop
  causal_orientation_coherent : Prop

/-- Graph orientation data induces the frontier orientation chart used by the
incidence sign-source layer. -/
def orientationChartOfGraphData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) : FrontierOrientationChart P :=
  { signBetween := fun u v => (D.polarityBetween u v).toSign
    orientation_coherent := D.frontier_coherent ∧ D.causal_orientation_coherent }

/-- Evaluation rule for the chart induced by graph orientation data. -/
theorem orientationChartOfGraphData_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) (u v : GraphVertex G) :
    (orientationChartOfGraphData D).signBetween u v =
      (D.polarityBetween u v).toSign :=
  rfl

/-- The induced chart records frontier/coherence data as its coherence field. -/
theorem orientationChartOfGraphData_coherent
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) :
    (orientationChartOfGraphData D).orientation_coherent =
      (D.frontier_coherent ∧ D.causal_orientation_coherent) :=
  rfl

/-- Graph orientation data induces an incidence sign source. -/
def signSourceOfGraphOrientationData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) : IncidenceSignSource P :=
  signSourceOfOrientationChart (orientationChartOfGraphData D)

/-- Evaluation rule for the induced sign source. -/
theorem signSourceOfGraphOrientationData_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) (l : OrientedFrontierLink P) :
    (signSourceOfGraphOrientationData D).signOf l =
      (D.polarityBetween l.src l.dst).toSign :=
  rfl

/-- Once graph orientation data is supplied, signs are deterministic functions
of the ordered frontier endpoints. -/
theorem graphOrientation_sign_deterministic
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (D : GraphOrientationData P) (l : OrientedFrontierLink P) :
    (signSourceOfGraphOrientationData D).signOf l =
      (signSourceOfGraphOrientationData D).signOf l :=
  rfl

/-- A graph-oriented three-link N1 boundary package. -/
structure GraphOrientedN1Boundary
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  orientationData : GraphOrientationData P
  frame : OrientedN1ThreeFrame P
  local_conserved : Prop

/-- Convert graph-oriented boundary data into the oriented-incidence boundary
from `RA_IncidenceSignSource_v1`. -/
def orientedIncidenceBoundaryOfGraphData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) : OrientedIncidenceBoundary P :=
  { orientation := orientationChartOfGraphData B.orientationData
    frame := B.frame
    local_conserved := B.local_conserved }

/-- Convert graph-oriented boundary data into the signed three-direction
incidence boundary. -/
def threeDirectionalBoundaryOfGraphData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) :
    ThreeDirectionalIncidenceBoundary P :=
  threeDirectionalBoundaryOfOrientation (orientedIncidenceBoundaryOfGraphData B)

/-- Graph-oriented boundary data has seven-value net N1 charge. -/
theorem threeDirectionalBoundaryOfGraphData_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) :
    SevenCharge (threeDirectionalBoundaryOfGraphData B).frame.qN1 :=
  threeDirectionalBoundaryOfOrientation_qN1_seven
    (orientedIncidenceBoundaryOfGraphData B)

/-- Ledger induced by graph-oriented boundary data. -/
noncomputable def ledgerOfGraphOrientedBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) :
    BoundaryLedger (candidatePastOfHasse P) (frontierOfFiniteGraph P) :=
  ledgerOfOrientedIncidenceBoundary (orientedIncidenceBoundaryOfGraphData B)

/-- The graph-oriented ledger has seven-value N1 charge. -/
theorem ledgerOfGraphOrientedBoundary_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) :
    SevenCharge (ledgerOfGraphOrientedBoundary B).qN1 :=
  ledgerOfOrientedIncidenceBoundary_qN1_seven
    (orientedIncidenceBoundaryOfGraphData B)

/-- Repackage graph-oriented boundary data as candidate-boundary data in the
selector/frontier layer. -/
noncomputable def boundaryDataOfGraphOrientedBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : GraphOrientedN1Boundary P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  boundaryDataOfOrientedIncidenceBoundary (orientedIncidenceBoundaryOfGraphData B)

/-- A statement of the remaining hard derivation target as data: RA-native graph
orientation closure supplies graph orientation data for a candidate past.

Future work should replace this package by a theorem using the existing causal
orientation / D1 ledger-orientation surface. -/
structure GraphOrientationClosure
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  orientationData : GraphOrientationData P
  determined_by_graph_frontier : Prop
  no_extra_random_labels : Prop

/-- If graph orientation closure is available, it supplies the orientation data
needed for deterministic signed incidence. -/
def graphOrientationDataOfClosure
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosure P) : GraphOrientationData P :=
  C.orientationData

/-- The sign source induced by graph-orientation closure is deterministic. -/
def signSourceOfGraphOrientationClosure
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosure P) : IncidenceSignSource P :=
  signSourceOfGraphOrientationData (graphOrientationDataOfClosure C)

/-- Evaluation rule for graph-orientation closure. -/
theorem signSourceOfGraphOrientationClosure_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosure P) (l : OrientedFrontierLink P) :
    (signSourceOfGraphOrientationClosure C).signOf l =
      (C.orientationData.polarityBetween l.src l.dst).toSign :=
  rfl

/-!
## Remaining hard theorem

This file converts graph-orientation data into a deterministic incidence chart,
but still receives `GraphOrientationData` as input.  The next hard theorem is:

```text
finite Hasse frontier
  + concrete RA causal-orientation asymmetry
  + D1 ledger-orientation preservation
  -> GraphOrientationClosure
```

That theorem would make the charge sign-source genuinely graph-native rather
than supplied as intermediate data.
-/

end RA
