import RA_HasseFrontier_FiniteMaxExist

/-!
# RA Incidence Charge v1

Eighth exploratory Lean scaffold for the Selector Closure programme.

The preceding Hasse-frontier files constructed graph-native candidate pasts,
frontiers, and finite maximum data.  This file begins the topological ledger /
charge-sign step in a deliberately conservative way.

It does **not** yet derive the physical sign source from graph topology.  Instead
it formalizes the conditional target:

* an oriented frontier link is a reachable link from a past vertex to a Hasse
  frontier vertex;
* an incidence sign source is a graph-native function assigning `{-1,0,+1}` to
  such oriented links;
* any three-direction signed N1 frontier frame has charge in the seven-value
  signature `{-3,-2,-1,0,+1,+2,+3}`;
* such a frame can be repackaged as a `BoundaryLedger` over the finite
  graph-derived Hasse frontier.

This isolates the remaining hard theorem: derive the incidence sign source from
the oriented local frontier / boundary complex rather than supplying it.
-/

namespace RA

/-- An oriented frontier link from a candidate-past vertex to a Hasse-frontier
vertex reachable above it.  This is a graph-native boundary/link object, not an
arbitrary sampled sign. -/
structure OrientedFrontierLink
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  src : GraphVertex G
  dst : GraphVertex G
  src_in_past : P.contains src
  dst_frontier : IsHasseFrontier P dst
  src_reaches_dst : Reachable G src dst

/-- A graph-native sign source for oriented frontier links.

This is intentionally a function, not a probability distribution.  The hard
future theorem is to construct such a source from finite oriented
frontier/incidence data. -/
structure IncidenceSignSource
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  signOf : OrientedFrontierLink P → IncidenceSign

/-- The sign source is deterministic as a function once supplied.  This is a
small formal marker for the no-primitive-randomness discipline. -/
theorem signSource_deterministic
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (S : IncidenceSignSource P) (l : OrientedFrontierLink P) :
    S.signOf l = S.signOf l :=
  rfl

/-- A frontier link together with its incidence sign. -/
structure SignedFrontierLink
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G)
    extends OrientedFrontierLink P where
  sign : IncidenceSign

/-- Integer N1 contribution of a signed frontier link. -/
def SignedFrontierLink.qN1
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (l : SignedFrontierLink P) : Int :=
  l.sign.toInt

/-- Apply an incidence sign source to an oriented frontier link. -/
def signedLinkOfSource
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (S : IncidenceSignSource P) (l : OrientedFrontierLink P) :
    SignedFrontierLink P :=
  { toOrientedFrontierLink := l
    sign := S.signOf l }

/-- A signed N1 frame with three independent frontier directions.

The `d=4 / 3+1D` electric translation layer uses at most three independent
spatial directions.  This structure records the local three-direction readout;
independence itself is left as future graph/incidence data, not assumed here as
a theorem. -/
structure SignedN1ThreeFrame
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  l0 : SignedFrontierLink P
  l1 : SignedFrontierLink P
  l2 : SignedFrontierLink P

/-- Net signed N1 charge of a three-direction frame. -/
def SignedN1ThreeFrame.qN1
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (F : SignedN1ThreeFrame P) : Int :=
  F.l0.qN1 + F.l1.qN1 + F.l2.qN1

/-- Any sum of three incidence signs lies in the RA seven-value charge
signature. -/
theorem sevenCharge_of_three_incidence_signs
    (a b c : IncidenceSign) :
    SevenCharge (a.toInt + b.toInt + c.toInt) := by
  cases a <;> cases b <;> cases c <;>
    simp [SevenCharge, IncidenceSign.toInt]

/-- A three-direction signed N1 frame has seven-value net charge. -/
theorem signedN1ThreeFrame_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (F : SignedN1ThreeFrame P) :
    SevenCharge F.qN1 := by
  simpa [SignedN1ThreeFrame.qN1, SignedFrontierLink.qN1] using
    sevenCharge_of_three_incidence_signs F.l0.sign F.l1.sign F.l2.sign

/-- Build a signed three-frame from a deterministic incidence sign source and
three oriented frontier links. -/
def signedThreeFrameOfSource
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (S : IncidenceSignSource P)
    (l0 l1 l2 : OrientedFrontierLink P) : SignedN1ThreeFrame P :=
  { l0 := signedLinkOfSource S l0
    l1 := signedLinkOfSource S l1
    l2 := signedLinkOfSource S l2 }

/-- The three-frame built from an incidence sign source has seven-value charge. -/
theorem signedThreeFrameOfSource_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (S : IncidenceSignSource P)
    (l0 l1 l2 : OrientedFrontierLink P) :
    SevenCharge (signedThreeFrameOfSource S l0 l1 l2).qN1 :=
  signedN1ThreeFrame_qN1_seven (signedThreeFrameOfSource S l0 l1 l2)

/-- A three-direction incidence boundary package for a finite graph-derived
Hasse frontier.

`local_conserved` remains abstract here; the next step is to connect it to LLC
and orientation-sensitive incidence conservation. -/
structure ThreeDirectionalIncidenceBoundary
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  frame : SignedN1ThreeFrame P
  local_conserved : Prop

/-- Convert a three-direction incidence boundary into a boundary ledger over the
finite graph-derived Hasse frontier. -/
noncomputable def ledgerOfThreeDirectionalBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : ThreeDirectionalIncidenceBoundary P) :
    BoundaryLedger (candidatePastOfHasse P) (frontierOfFiniteGraph P) :=
  { qN1 := B.frame.qN1
    qN1_seven := signedN1ThreeFrame_qN1_seven B.frame
    local_conserved := B.local_conserved }

/-- The ledger induced by a three-direction incidence boundary has seven-value
N1 charge. -/
theorem ledgerOfThreeDirectionalBoundary_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : ThreeDirectionalIncidenceBoundary P) :
    SevenCharge (ledgerOfThreeDirectionalBoundary B).qN1 :=
  (ledgerOfThreeDirectionalBoundary B).qN1_seven

/-- Repackage a three-direction incidence boundary as candidate-boundary data in
 the selector/frontier layer. -/
noncomputable def boundaryDataOfThreeDirectionalBoundary
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (B : ThreeDirectionalIncidenceBoundary P) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  { past := candidatePastOfHasse P
    frontier := frontierOfFiniteGraph P
    ledger := ledgerOfThreeDirectionalBoundary B }

/-!
## What remains open

This file proves the conditional seven-value theorem for any supplied
three-direction incidence-sign frame.  It does not yet derive the sign source.
The next hard target is:

```text
finite Hasse frontier + oriented boundary/incidence structure
  → IncidenceSignSource
```

Once that source is constructed graph-natively, the signed N1 charge rule will
be topological rather than sampled.
-/

end RA
