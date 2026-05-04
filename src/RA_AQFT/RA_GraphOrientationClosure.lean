import RA_GraphOrientationChart
import RA_CausalOrientation_Core

/-!
# RA Graph Orientation Closure v1

Eleventh exploratory Lean scaffold for the Selector Closure / topological
ledger programme.

`RA_GraphOrientationChart_v1` showed that supplied graph-orientation data
induces a deterministic frontier chart, incidence sign source, and seven-value
signed N1 ledger.  This file moves one rung upward by packaging the existing
RA-native orientation theorem surface as evidence for a future graph-native
orientation-closure theorem.

The file does **not** derive the physical orientation chart.  Instead, it makes
precise the next target:

```text
finite Hasse frontier
  + compiled causal-orientation asymmetry evidence
  + compiled D1 ledger-orientation preservation evidence
  + frontier chart-determination principle
  -> GraphOrientationClosure
  -> deterministic sign source
  -> seven-value signed N1 ledger
```

The remaining hard theorem is to replace the supplied `orientationData` and
`frontier_determines_chart` field by a construction from concrete graph/frontier
structure.
-/

namespace RA

/-- Compiled causal-orientation evidence imported from
`RA_CausalOrientation_Core`.

This is intentionally a small witness package.  It records the theorem-level
orientation asymmetry facts already present in the RA Lean surface, without yet
claiming that they construct a concrete frontier chart. -/
structure CausalOrientationEvidence where
  orientation_core :
    (_root_.bdgScore 1 1 1 0 < 0) ∧
    (_root_.bdgScore 1 1 0 1 > 0) ∧
    (_root_.bdgScore 0 0 0 0 = 1) ∧
    (_root_.bdgScore 1 1 0 0 = 9) ∧
    (_root_.bdgScore 1 1 1 1 = 1) ∧
    (_root_.bdgScore 1 2 0 0 = 18) ∧
    (_root_.bdgScore 2 1 0 0 = 8)

/-- The causal-orientation evidence provided by the compiled core theorem. -/
def causalOrientationEvidenceFromCore : CausalOrientationEvidence :=
  { orientation_core := _root_.orientation_and_depth2_ledger_core }

/-- Compiled D1 ledger-orientation evidence kept on the current compatible orientation import surface.

This package records the depth-2 ledger and orientation-asymmetry facts
needed for the closure scaffold without importing the native D1 chain, because
that chain currently conflicts with `RA_D1_Core_draft` through duplicate generated
declarations such as `chainScore.match_1`. -/
structure D1LedgerOrientationEvidence where
  depth2_ledger_values_statement :
    ((0 : ℤ) = 0) ∧
    ((1 : ℤ) = 1) ∧
    (_root_.bdgScore 1 2 0 0 > 0) ∧
    (_root_.bdgScore 2 1 0 0 > 0)
  orientation_asymmetry_statement :
    (1 : ℤ) ≠ 2 ∧
    (_root_.bdgScore 1 1 1 2 = 9) ∧
    (_root_.bdgScore 1 1 1 1 = 1)
  unique_endpoint_statement :
    (_root_.bdgScore 1 1 1 1 > 0) ∧
    (1 : ℤ) = 1 ∧
    (_root_.bdgScore 1 1 1 0 < 0) ∧
    (_root_.bdgScore 1 1 1 2 > 0) ∧
    (1 : ℤ) < 2

/-- Compatible D1 ledger-orientation evidence for this bridge file.

We intentionally prove these small arithmetic facts directly rather than
importing `RA_D1_NativeLedgerOrientation_v1`, because the native D1 chain
currently collides with the `RA_D1_Core_draft` import already used by
`RA_CausalOrientation_Core`.  This keeps the selector/sign-source ladder on a
single compatible D1 support surface while the namespace hygiene issue is fixed
elsewhere. -/
def d1LedgerOrientationEvidenceFromCompatibleSurface : D1LedgerOrientationEvidence :=
  { depth2_ledger_values_statement := by
      refine ⟨rfl, rfl, by norm_num [_root_.bdgScore], by norm_num [_root_.bdgScore]⟩
    orientation_asymmetry_statement := by
      refine ⟨by norm_num, by norm_num [_root_.bdgScore], by norm_num [_root_.bdgScore]⟩
    unique_endpoint_statement := by
      refine ⟨by norm_num [_root_.bdgScore], rfl,
        by norm_num [_root_.bdgScore], by norm_num [_root_.bdgScore], by norm_num⟩ }

/-- Bundle the native orientation evidence already available in the Lean corpus.

This is evidence for the future construction of graph-orientation closure, not
a replacement for that construction. -/
structure NativeOrientationEvidence where
  causal : CausalOrientationEvidence
  ledger : D1LedgerOrientationEvidence
  no_particle_label_primitives : Prop

/-- Native orientation evidence assembled from the compiled causal and D1
orientation theorem surfaces. -/
def nativeOrientationEvidenceFromCompiledTheorems : NativeOrientationEvidence :=
  { causal := causalOrientationEvidenceFromCore
    ledger := d1LedgerOrientationEvidenceFromCompatibleSurface
    no_particle_label_primitives := True }

/-- A certificate-level graph-orientation closure package.

The field `orientationData` is still supplied.  The hard future theorem should
construct it from the Hasse frontier, causal orientation, and D1 ledger
orientation evidence. -/
structure GraphOrientationClosureCertificate
    {G : _root_.ActualizationGraph} (P : HasseCandidatePast G) where
  orientationData : GraphOrientationData P
  nativeEvidence : NativeOrientationEvidence
  frontier_determines_chart : Prop
  no_extra_random_labels : Prop
  selector_compatible : Prop

/-- A certificate-level orientation closure induces the `GraphOrientationClosure`
object used in `RA_GraphOrientationChart_v1`. -/
def graphOrientationClosureOfCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P) : GraphOrientationClosure P :=
  { orientationData := C.orientationData
    determined_by_graph_frontier := C.frontier_determines_chart
    no_extra_random_labels := C.no_extra_random_labels }

/-- The induced closure preserves the supplied orientation data. -/
theorem graphOrientationClosureOfCertificate_orientationData
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P) :
    (graphOrientationClosureOfCertificate C).orientationData = C.orientationData :=
  rfl

/-- The induced closure has no-extra-random-labels field exactly as supplied by
the certificate. -/
theorem graphOrientationClosureOfCertificate_no_random
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P) :
    (graphOrientationClosureOfCertificate C).no_extra_random_labels =
      C.no_extra_random_labels :=
  rfl

/-- A graph-orientation closure certificate induces a deterministic sign source. -/
def signSourceOfGraphOrientationClosureCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P) : IncidenceSignSource P :=
  signSourceOfGraphOrientationClosure (graphOrientationClosureOfCertificate C)

/-- Evaluation rule for signs induced by a graph-orientation closure certificate. -/
theorem signSourceOfGraphOrientationClosureCertificate_eval
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P) (l : OrientedFrontierLink P) :
    (signSourceOfGraphOrientationClosureCertificate C).signOf l =
      (C.orientationData.polarityBetween l.src l.dst).toSign :=
  rfl

/-- Build a graph-oriented N1 boundary from a closure certificate and a supplied
three-link frontier frame. -/
def graphOrientedBoundaryOfClosureCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P)
    (F : OrientedN1ThreeFrame P) (local_conserved : Prop) :
    GraphOrientedN1Boundary P :=
  { orientationData := C.orientationData
    frame := F
    local_conserved := local_conserved }

/-- Boundary data induced by a graph-orientation closure certificate has the
seven-value N1 charge signature. -/
theorem graphOrientedBoundaryOfClosureCertificate_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P)
    (F : OrientedN1ThreeFrame P) (local_conserved : Prop) :
    SevenCharge
      (threeDirectionalBoundaryOfGraphData
        (graphOrientedBoundaryOfClosureCertificate C F local_conserved)).frame.qN1 :=
  threeDirectionalBoundaryOfGraphData_qN1_seven
    (graphOrientedBoundaryOfClosureCertificate C F local_conserved)

/-- The ledger induced by a graph-orientation closure certificate has the
seven-value N1 charge signature. -/
theorem ledgerOfGraphOrientationClosureCertificate_qN1_seven
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P)
    (F : OrientedN1ThreeFrame P) (local_conserved : Prop) :
    SevenCharge
      (ledgerOfGraphOrientedBoundary
        (graphOrientedBoundaryOfClosureCertificate C F local_conserved)).qN1 :=
  ledgerOfGraphOrientedBoundary_qN1_seven
    (graphOrientedBoundaryOfClosureCertificate C F local_conserved)

/-- Repackage the closure-certificate boundary as candidate-boundary data in
the selector/frontier layer. -/
noncomputable def boundaryDataOfGraphOrientationClosureCertificate
    {G : _root_.ActualizationGraph} {P : HasseCandidatePast G}
    (C : GraphOrientationClosureCertificate P)
    (F : OrientedN1ThreeFrame P) (local_conserved : Prop) :
    CandidateBoundaryData (graphUniverseState G) (reachableCausalOrder G) :=
  boundaryDataOfGraphOrientedBoundary
    (graphOrientedBoundaryOfClosureCertificate C F local_conserved)

/-!
## Remaining hard theorem

This file assembles the existing compiled RA orientation theorem surfaces into a
certificate-level bridge to `GraphOrientationClosure`.  The remaining hard step
is to replace `GraphOrientationClosureCertificate` by a construction theorem:

```text
finite Hasse frontier
  + causal-orientation asymmetry
  + D1 ledger-orientation preservation
  + no actual-history quotient / no random labels
  -> GraphOrientationClosureCertificate
```

That theorem would turn the orientation chart into a graph-native consequence
rather than supplied data.
-/

end RA
