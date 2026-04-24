-- RA_GraphCore.lean  (v2 — sorry closure attempt)
-- Graph-Theoretic Foundations: LLC, Graph Cut, Markov Blanket
--
-- L01: Local Ledger Condition (definitional)
-- L02: Graph Cut Theorem
-- L03: Markov Blanket (structural)
--
-- TARGET: Zero sorry.
-- Strategy: Finset.sum_biUnion for sum exchange, Finset.sum_union for split.
--
-- Author: Joshua F. Sandeman (March 2026)
-- Sorry closure: Claude/Anthropic (April 8, 2026) — MUST BE COMPILE-TESTED

import Mathlib

open BigOperators

-- ═══════════════════════════════════════════════════════════════
-- SECTION 1: BASIC STRUCTURES
-- ═══════════════════════════════════════════════════════════════

structure Vertex where
  id : ℕ
  deriving DecidableEq, Hashable

structure Edge where
  src : Vertex
  dst : Vertex
  charge : ℤ
  deriving DecidableEq

structure ActualizationGraph where
  V : Finset Vertex
  E : Finset Edge
  edge_src_mem : ∀ e ∈ E, e.src ∈ V
  edge_dst_mem : ∀ e ∈ E, e.dst ∈ V
  topo_order : Vertex → ℕ
  arrow_of_time : ∀ e ∈ E, topo_order e.src < topo_order e.dst

-- ═══════════════════════════════════════════════════════════════
-- SECTION 2: EDGE CLASSIFICATION
-- ═══════════════════════════════════════════════════════════════

def outgoing_edges (G : ActualizationGraph) (v : Vertex) : Finset Edge :=
  G.E.filter (fun e => e.src = v)

def incoming_edges (G : ActualizationGraph) (v : Vertex) : Finset Edge :=
  G.E.filter (fun e => e.dst = v)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 3: LOCAL LEDGER CONDITION (L01)
-- ═══════════════════════════════════════════════════════════════

def satisfies_local_ledger (G : ActualizationGraph) (v : Vertex) : Prop :=
  ∑ e ∈ outgoing_edges G v, e.charge = ∑ e ∈ incoming_edges G v, e.charge

-- ═══════════════════════════════════════════════════════════════
-- SECTION 4: CAUSAL CUT
-- ═══════════════════════════════════════════════════════════════

structure CausalCut (G : ActualizationGraph) where
  V_L : Finset Vertex
  V_R : Finset Vertex
  is_partition : V_L ∪ V_R = G.V ∧ Disjoint V_L V_R
  no_backward : ∀ e ∈ G.E, e.dst ∈ V_L → e.src ∈ V_L

def internal_edges (G : ActualizationGraph) (S : Finset Vertex) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ S ∧ e.dst ∈ S)

def boundary_flux (G : ActualizationGraph) (C : CausalCut G) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ C.V_L ∧ e.dst ∈ C.V_R)

/-- Edges with source in V_L. -/
def src_in_VL (G : ActualizationGraph) (C : CausalCut G) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ C.V_L)

/-- Edges with destination in V_L. -/
def dst_in_VL (G : ActualizationGraph) (C : CausalCut G) : Finset Edge :=
  G.E.filter (fun e => e.dst ∈ C.V_L)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 5: KEY LEMMAS
-- ═══════════════════════════════════════════════════════════════

/-- Outgoing edge sets for distinct vertices are disjoint. -/
lemma outgoing_pairwise_disjoint (G : ActualizationGraph) :
    Set.PairwiseDisjoint (Set.univ : Set Vertex) (fun v => outgoing_edges G v) := by
  intro v _ w _ hvw
  simp only [Function.onFun, Finset.disjoint_left, outgoing_edges, Finset.mem_filter]
  intro e ⟨_, hsv⟩ ⟨_, hsw⟩
  exact hvw (hsv.symm.trans hsw)

/-- Incoming edge sets for distinct vertices are disjoint. -/
lemma incoming_pairwise_disjoint (G : ActualizationGraph) :
    Set.PairwiseDisjoint (Set.univ : Set Vertex) (fun v => incoming_edges G v) := by
  intro v _ w _ hvw
  simp only [Function.onFun, Finset.disjoint_left, incoming_edges, Finset.mem_filter]
  intro e ⟨_, hdv⟩ ⟨_, hdw⟩
  exact hvw (hdv.symm.trans hdw)

/-- Pairwise disjointness restricted to V_L. -/
lemma outgoing_pairwise_disjoint_VL (G : ActualizationGraph) (C : CausalCut G) :
    Set.PairwiseDisjoint (↑C.V_L) (fun v => outgoing_edges G v) := by
  intro v hv w hw hvw
  exact outgoing_pairwise_disjoint G (Set.mem_univ v) (Set.mem_univ w) hvw

lemma incoming_pairwise_disjoint_VL (G : ActualizationGraph) (C : CausalCut G) :
    Set.PairwiseDisjoint (↑C.V_L) (fun v => incoming_edges G v) := by
  intro v hv w hw hvw
  exact incoming_pairwise_disjoint G (Set.mem_univ v) (Set.mem_univ w) hvw

/-- The biUnion of outgoing edges over V_L equals edges with src ∈ V_L. -/
lemma biUnion_outgoing_eq_src_in_VL (G : ActualizationGraph) (C : CausalCut G) :
    C.V_L.biUnion (fun v => outgoing_edges G v) = src_in_VL G C := by
  ext e
  simp only [Finset.mem_biUnion, outgoing_edges, Finset.mem_filter, src_in_VL]
  constructor
  · rintro ⟨v, hv, he, rfl⟩; exact ⟨he, hv⟩
  · rintro ⟨he, hsrc⟩; exact ⟨e.src, hsrc, he, rfl⟩

/-- The biUnion of incoming edges over V_L equals edges with dst ∈ V_L. -/
lemma biUnion_incoming_eq_dst_in_VL (G : ActualizationGraph) (C : CausalCut G) :
    C.V_L.biUnion (fun v => incoming_edges G v) = dst_in_VL G C := by
  ext e
  simp only [Finset.mem_biUnion, incoming_edges, Finset.mem_filter, dst_in_VL]
  constructor
  · rintro ⟨v, hv, he, rfl⟩; exact ⟨he, hv⟩
  · rintro ⟨he, hdst⟩; exact ⟨e.dst, hdst, he, rfl⟩

/-- Internal edges and boundary flux are disjoint. -/
lemma internal_flux_disjoint (G : ActualizationGraph) (C : CausalCut G) :
    Disjoint (internal_edges G C.V_L) (boundary_flux G C) := by
  simp only [Finset.disjoint_left, internal_edges, boundary_flux, Finset.mem_filter]
  intro e ⟨_, _, h_dst_L⟩ ⟨_, _, h_dst_R⟩
  exact absurd h_dst_R (Finset.disjoint_left.mp C.is_partition.2 h_dst_L)

/-- Edges with src ∈ V_L split into internal ∪ boundary. -/
lemma src_in_VL_eq_internal_union_boundary (G : ActualizationGraph) (C : CausalCut G) :
    src_in_VL G C = internal_edges G C.V_L ∪ boundary_flux G C := by
  ext e
  simp only [src_in_VL, internal_edges, boundary_flux,
             Finset.mem_filter, Finset.mem_union]
  constructor
  · rintro ⟨he, hsrc⟩
    -- e.dst is either in V_L or V_R (partition covers all vertices)
    by_cases hdst : e.dst ∈ C.V_L
    · left; exact ⟨he, hsrc, hdst⟩
    · right
      have h_in_V : e.dst ∈ G.V := G.edge_dst_mem e he
      rw [← C.is_partition.1] at h_in_V
      exact ⟨he, hsrc, Finset.mem_union.mp h_in_V |>.resolve_left hdst⟩
  · rintro (⟨he, hsrc, _⟩ | ⟨he, hsrc, _⟩) <;> exact ⟨he, hsrc⟩

/-- Edges with dst ∈ V_L equal internal edges (by no_backward). -/
lemma dst_in_VL_eq_internal (G : ActualizationGraph) (C : CausalCut G) :
    dst_in_VL G C = internal_edges G C.V_L := by
  ext e
  simp only [dst_in_VL, internal_edges, Finset.mem_filter]
  constructor
  · rintro ⟨he, hdst⟩
    exact ⟨he, C.no_backward e he hdst, hdst⟩
  · rintro ⟨he, _, hdst⟩
    exact ⟨he, hdst⟩

-- ═══════════════════════════════════════════════════════════════
-- SECTION 6: SUM DECOMPOSITION LEMMAS (formerly sorry)
-- ═══════════════════════════════════════════════════════════════

/-- Outgoing sum decomposes into internal + boundary. -/
lemma sum_outgoing_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) +
    (∑ e ∈ boundary_flux G C, e.charge) := by
  -- Step 1: exchange double sum to single sum over biUnion
  rw [← Finset.sum_biUnion (outgoing_pairwise_disjoint_VL G C)]
  -- Step 2: biUnion = src_in_VL
  rw [biUnion_outgoing_eq_src_in_VL G C]
  -- Step 3: src_in_VL = internal ∪ boundary
  rw [src_in_VL_eq_internal_union_boundary G C]
  -- Step 4: sum over union = sum + sum (disjoint)
  exact Finset.sum_union (internal_flux_disjoint G C)

/-- Incoming sum equals internal edges only. -/
lemma sum_incoming_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) := by
  -- Step 1: exchange double sum to single sum over biUnion
  rw [← Finset.sum_biUnion (incoming_pairwise_disjoint_VL G C)]
  -- Step 2: biUnion = dst_in_VL
  rw [biUnion_incoming_eq_dst_in_VL G C]
  -- Step 3: dst_in_VL = internal (by no_backward)
  rw [dst_in_VL_eq_internal G C]

-- ═══════════════════════════════════════════════════════════════
-- SECTION 7: GRAPH CUT THEOREM (L02)
-- ═══════════════════════════════════════════════════════════════

/-- **L02 — Graph Cut Theorem**: If the LLC holds at every vertex in V_L,
    then the total charge crossing the causal cut is zero. -/
theorem RA_graph_cut_theorem
    (G : ActualizationGraph) (C : CausalCut G)
    (h_ledger : ∀ v ∈ C.V_L, satisfies_local_ledger G v) :
    ∑ e ∈ boundary_flux G C, e.charge = 0 := by
  have h_sum_eq :
      ∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge =
      ∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge := by
    apply Finset.sum_congr rfl
    intro v hv
    exact (h_ledger v hv)
  rw [sum_outgoing_decompose G C] at h_sum_eq
  rw [sum_incoming_decompose G C] at h_sum_eq
  linarith

theorem horizon_partition
    (G : ActualizationGraph) (C : CausalCut G)
    (h_ledger : ∀ v ∈ C.V_L, satisfies_local_ledger G v) :
    ∑ e ∈ boundary_flux G C, e.charge = 0 :=
  RA_graph_cut_theorem G C h_ledger

-- ═══════════════════════════════════════════════════════════════
-- SECTION 8: MARKOV BLANKET (L03)
-- ═══════════════════════════════════════════════════════════════

structure MarkovBlanket (G : ActualizationGraph) where
  Internal : Finset Vertex
  External : Finset Vertex
  Sensory  : Finset Vertex
  Active   : Finset Vertex
  is_complete : Internal ∪ External ∪ Sensory ∪ Active = G.V
  shield_internal : ∀ e ∈ G.E,
    e.dst ∈ Internal → e.src ∈ Sensory ∪ Internal
  shield_external : ∀ e ∈ G.E,
    e.dst ∈ External → e.src ∈ Active ∪ External

def MarkovBlanket.boundary (G : ActualizationGraph) (M : MarkovBlanket G) :
    Finset Vertex :=
  M.Sensory ∪ M.Active

/-!
## Proof status: ZERO sorry (if this compiles)

All lemmas proved via Finset.sum_biUnion + Finset.sum_union.

Key proof chain:
  outgoing_pairwise_disjoint → biUnion_outgoing_eq → src_in_VL_eq → sum_outgoing_decompose
  incoming_pairwise_disjoint → biUnion_incoming_eq → dst_in_VL_eq → sum_incoming_decompose
  LLC + sum_outgoing + sum_incoming → graph_cut_theorem (linarith)

NOTE: This file must be compile-tested in Lean 4.29 with Mathlib.
The proofs use Finset.sum_biUnion which requires Set.PairwiseDisjoint.
If the exact Mathlib4 API has changed, the simp lemma names may need
adjustment. The proof STRATEGY is correct; only tactic names might differ.
-/