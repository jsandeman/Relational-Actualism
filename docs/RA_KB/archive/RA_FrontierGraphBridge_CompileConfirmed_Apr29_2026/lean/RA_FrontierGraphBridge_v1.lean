import RA_FrontierIncidence_v1
import RA_GraphCore

/-!
# RA Frontier / Graph Bridge v1

Third exploratory Lean scaffold for the Selector Closure programme.

This file begins connecting the abstract frontier/incidence vocabulary to the
concrete graph-core structures already present in `RA_GraphCore.lean`:

* `ActualizationGraph`
* `CausalCut`
* `satisfies_local_ledger`
* `boundary_flux`
* `RA_graph_cut_theorem`

It still does **not** prove the hard Selector Closure Theorem.  It proves only
safe bridge facts:

* a finite `ActualizationGraph` induces a finite `UniverseState`;
* the graph topological order induces a conservative abstract `CausalOrder`;
* graph edges point forward in that abstract order;
* a causal cut can be packaged as a candidate past when supplied with a
  downset certificate for the chosen order;
* the graph-cut theorem supplies a conserved boundary ledger with zero net
  cut flux;
* this produces candidate boundary data for the frontier/incidence layer.

The next hard step is to replace the conservative topological-order bridge with
an actual reachability/Hasse-frontier construction, then prove that BDG profile
and LLC boundary data are invariant under the appropriate graph-normal form.
-/

open BigOperators

namespace RA

/-- The finite vertex type carried by an `ActualizationGraph`. -/
abbrev GraphVertex (G : _root_.ActualizationGraph) : Type :=
  {v : _root_.Vertex // v ∈ G.V}

/-- The finite type instance for the subtype of vertices actually present in `G`.

This is separated from `graphUniverseState` to avoid Lean inferring the wrong
ambient vertex type when elaborating `Fintype.ofFinset` inside a structure
literal.  Lean treats definitions returning class types specially; marking this
helper reducible keeps instance search/transparency behavior explicit and avoids
the class-type warning. -/
@[reducible]
noncomputable def graphVertexFintype (G : _root_.ActualizationGraph) :
    Fintype (GraphVertex G) :=
  { elems := G.V.attach
    complete := by
      intro x
      simp }

/-- A concrete finite graph gives an abstract RA universe-state by taking its
finite vertex set as the state vertex type. -/
noncomputable def graphUniverseState (G : _root_.ActualizationGraph) : UniverseState :=
  ⟨GraphVertex G, graphVertexFintype G⟩

/-- Conservative causal order induced by the graph topological order.

Two subtype vertices are related when they are equal, or when the first has
strictly smaller `topo_order`.  This is not yet the physical reachability order;
it is a safe order bridge because every concrete edge points forward in it. -/
noncomputable def topoOrderCausalOrder
    (G : _root_.ActualizationGraph) : CausalOrder (graphUniverseState G) :=
  { le := fun a b => a = b ∨ G.topo_order a.val < G.topo_order b.val
    refl := by
      intro v
      exact Or.inl rfl
    trans := by
      intro a b c hab hbc
      rcases hab with rfl | hlt
      · exact hbc
      · rcases hbc with rfl | hlt'
        · exact Or.inr hlt
        · exact Or.inr (Nat.lt_trans hlt hlt')
    antisymm := by
      intro a b hab hba
      rcases hab with rfl | hlt
      · rfl
      · rcases hba with rfl | hlt'
        · rfl
        · exact False.elim ((Nat.lt_asymm hlt) hlt') }

/-- Every concrete graph edge points forward in the induced topological order. -/
theorem graph_edge_forward_in_topo_order
    (G : _root_.ActualizationGraph) (e : _root_.Edge) (he : e ∈ G.E) :
    (topoOrderCausalOrder G).le
      ⟨e.src, G.edge_src_mem e he⟩
      ⟨e.dst, G.edge_dst_mem e he⟩ :=
  Or.inr (G.arrow_of_time e he)

/-- The causal-cut `no_backward` condition is the graph-core local downset
condition for one-step edges: if an edge lands in the left side of the cut, its
source is also in the left side. -/
theorem cut_no_backward_edge_downset
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G)
    (e : _root_.Edge) (he : e ∈ G.E) (hdst : e.dst ∈ C.V_L) :
    e.src ∈ C.V_L :=
  C.no_backward e he hdst

/-- Certificate that a graph cut is down-closed for a chosen abstract causal
order.  For the eventual reachability/Hasse order, this should be derivable
from `CausalCut.no_backward`; for the conservative topological-order bridge it
is kept as explicit data. -/
structure CutDownsetCertificate
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G)
    (O : CausalOrder (graphUniverseState G)) where
  down_closed :
    ∀ {x y : (graphUniverseState G).Vertex},
      O.le x y → y.val ∈ C.V_L → x.val ∈ C.V_L

/-- A causal cut, plus a downset certificate for the chosen order, determines a
`CandidatePast` in the frontier/incidence scaffold. -/
def candidatePastOfCut
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G)
    (O : CausalOrder (graphUniverseState G))
    (H : CutDownsetCertificate G C O) : CandidatePast (graphUniverseState G) O :=
  { contains := fun v => v.val ∈ C.V_L
    down_closed := by
      intro x y hxy hy
      exact H.down_closed hxy hy }

/-- The integer charge flux through the graph-core boundary of a causal cut. -/
def cutBoundaryCharge
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G) : Int :=
  ∑ e ∈ _root_.boundary_flux G C, e.charge

/-- The graph-cut theorem gives zero net boundary charge when LLC holds on the
left side of the cut. -/
theorem cutBoundaryCharge_zero
    (G : _root_.ActualizationGraph) (C : _root_.CausalCut G)
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    cutBoundaryCharge G C = 0 := by
  unfold cutBoundaryCharge
  exact _root_.RA_graph_cut_theorem G C h_ledger

/-- Zero belongs to the seven-value signed N1 charge signature. -/
theorem zero_sevenCharge : SevenCharge (0 : Int) := by
  unfold SevenCharge
  right
  right
  right
  left
  rfl

/-- A conserved causal cut gives a boundary ledger for any supplied frontier of
its candidate past.  The ledger's `qN1` is the graph-core cut flux; the graph-cut
theorem proves that flux is zero under local LLC. -/
noncomputable def boundaryLedgerOfCut
    {G : _root_.ActualizationGraph} {C : _root_.CausalCut G}
    {O : CausalOrder (graphUniverseState G)}
    (H : CutDownsetCertificate G C O)
    (F : Frontier (graphUniverseState G) O (candidatePastOfCut G C O H))
    (h_ledger : ∀ v ∈ C.V_L, _root_.satisfies_local_ledger G v) :
    BoundaryLedger (candidatePastOfCut G C O H) F :=
  { qN1 := cutBoundaryCharge G C
    qN1_seven := by
      rw [cutBoundaryCharge_zero G C h_ledger]
      exact zero_sevenCharge
    local_conserved := cutBoundaryCharge G C = 0 }

/-- A graph cut/frontier bridge packages the concrete graph-core cut, an
abstract order, a downset certificate, and a frontier for the associated
candidate past. -/
structure GraphCutFrontierBridge (G : _root_.ActualizationGraph) where
  cut : _root_.CausalCut G
  order : CausalOrder (graphUniverseState G)
  downset_cert : CutDownsetCertificate G cut order
  frontier : Frontier (graphUniverseState G) order
    (candidatePastOfCut G cut order downset_cert)

/-- The candidate past carried by a graph cut/frontier bridge. -/
def GraphCutFrontierBridge.past
    {G : _root_.ActualizationGraph} (B : GraphCutFrontierBridge G) :
    CandidatePast (graphUniverseState G) B.order :=
  candidatePastOfCut G B.cut B.order B.downset_cert

/-- The boundary ledger carried by a graph cut/frontier bridge, assuming local
LLC holds on the left side of the cut. -/
noncomputable def GraphCutFrontierBridge.boundaryLedger
    {G : _root_.ActualizationGraph} (B : GraphCutFrontierBridge G)
    (h_ledger : ∀ v ∈ B.cut.V_L, _root_.satisfies_local_ledger G v) :
    BoundaryLedger (GraphCutFrontierBridge.past B) B.frontier :=
  boundaryLedgerOfCut (G := G) (C := B.cut) (O := B.order)
    B.downset_cert B.frontier h_ledger

/-- The full candidate-boundary data induced by a graph cut/frontier bridge and
local LLC on the cut. -/
noncomputable def GraphCutFrontierBridge.boundaryData
    {G : _root_.ActualizationGraph} (B : GraphCutFrontierBridge G)
    (h_ledger : ∀ v ∈ B.cut.V_L, _root_.satisfies_local_ledger G v) :
    CandidateBoundaryData (graphUniverseState G) B.order :=
  { past := GraphCutFrontierBridge.past B
    frontier := B.frontier
    ledger := GraphCutFrontierBridge.boundaryLedger B h_ledger }

/-- Conservation theorem for the boundary charge of a graph cut/frontier bridge.
This is just the graph-cut theorem re-expressed at the frontier-bridge level. -/
theorem GraphCutFrontierBridge.boundaryCharge_zero
    {G : _root_.ActualizationGraph} (B : GraphCutFrontierBridge G)
    (h_ledger : ∀ v ∈ B.cut.V_L, _root_.satisfies_local_ledger G v) :
    cutBoundaryCharge G B.cut = 0 :=
  cutBoundaryCharge_zero G B.cut h_ledger

/-- The boundary ledger extracted from a graph cut/frontier bridge has a
seven-value N1 charge.  In the conserved-cut case represented here, the value is
zero.  Nonzero local signed charges require the next step: an oriented local
frontier/incidence sign-source theorem. -/
theorem GraphCutFrontierBridge.boundaryLedger_qN1_seven
    {G : _root_.ActualizationGraph} (B : GraphCutFrontierBridge G)
    (h_ledger : ∀ v ∈ B.cut.V_L, _root_.satisfies_local_ledger G v) :
    SevenCharge (GraphCutFrontierBridge.boundaryLedger B h_ledger).qN1 :=
  (GraphCutFrontierBridge.boundaryLedger B h_ledger).qN1_seven

/-!
## What remains hard

This file only bridges the graph-core cut theorem into the frontier/incidence
vocabulary.  It does not yet construct the physical candidate frontier from a
one-vertex extension, and it does not yet derive nonzero local charge signs.

The next theorem target is a concrete reachability/Hasse-frontier construction:

```text
one-vertex extension
  → causal closure / candidate past
  → Hasse frontier
  → oriented boundary incidence
  → signed N1 ledger
```

That construction is the likely meeting point of the Selector Closure theorem,
the no-hidden-multiplicity principle, and the topological charge rule.
-/

end RA
