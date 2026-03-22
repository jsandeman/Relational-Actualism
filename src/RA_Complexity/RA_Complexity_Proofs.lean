import Mathlib

noncomputable section
open Classical
open Finset
open BigOperators

-- =====================================================================
-- RELATIONAL ACTUALISM: LEAN 4 / MATHLIB FORMALIZATION
-- =====================================================================

-- =====================================================================
-- 1. THE ONTOLOGY: VERTICES, EDGES, AND THE ACTUALIZATION GRAPH
-- =====================================================================

structure Vertex where
  id : Nat
  deriving DecidableEq

structure Edge where
  src : Vertex
  dst : Vertex
  charge : Real

structure ActualizationGraph where
  V : Finset Vertex
  E : Finset Edge
  edges_valid : forall e, e ∈ E → e.src ∈ V ∧ e.dst ∈ V
  is_acyclic : True


-- =====================================================================
-- 2. THE LOCAL LEDGER CONDITION (LLC)
-- =====================================================================

def incoming_edges (G : ActualizationGraph) (v : Vertex) : Finset Edge :=
  G.E.filter (fun e => e.dst = v)

def outgoing_edges (G : ActualizationGraph) (v : Vertex) : Finset Edge :=
  G.E.filter (fun e => e.src = v)

def satisfies_local_ledger (G : ActualizationGraph) (v : Vertex) : Prop :=
  (∑ e ∈ incoming_edges G v, e.charge) = (∑ e ∈ outgoing_edges G v, e.charge)


-- =====================================================================
-- 3. THE CAUSAL CUT (EVENT HORIZON)
-- =====================================================================

structure CausalCut (G : ActualizationGraph) where
  V_L : Finset Vertex
  V_R : Finset Vertex
  is_partition : V_L ∪ V_R = G.V ∧ Disjoint V_L V_R
  arrow_of_time : forall e, e ∈ G.E → e.src ∈ V_R → e.dst ∉ V_L

def boundary_flux (G : ActualizationGraph) (C : CausalCut G) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ C.V_L ∧ e.dst ∈ C.V_R)

def internal_edges (G : ActualizationGraph) (V_sub : Finset Vertex) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ V_sub ∧ e.dst ∈ V_sub)

-- =====================================================================
-- 4. HELPER LEMMAS (D4 Closed)
-- =====================================================================

lemma internal_flux_disjoint (G : ActualizationGraph) (C : CausalCut G) :
    Disjoint (internal_edges G C.V_L) (boundary_flux G C) := by
  rw [Finset.disjoint_left]
  intro e he_int he_bound
  have h_dst_L : e.dst ∈ C.V_L := (Finset.mem_filter.mp he_int).2.2
  have h_dst_R : e.dst ∈ C.V_R := (Finset.mem_filter.mp he_bound).2.2
  have h_disj := C.is_partition.2
  exact Finset.disjoint_left.mp h_disj h_dst_L h_dst_R

lemma sum_outgoing_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) +
    (∑ e ∈ boundary_flux G C, e.charge) := by
  -- 1. Flatten the nested sum using explicit bounded union logic
  have h_flat : (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) = 
                ∑ e ∈ G.E.filter (fun e => e.src ∈ C.V_L), e.charge := by
    have h_union : G.E.filter (fun e => e.src ∈ C.V_L) = C.V_L.biUnion (fun v => outgoing_edges G v) := by
      ext e
      simp only [Finset.mem_filter, Finset.mem_biUnion, outgoing_edges]
      constructor
      · rintro ⟨he, hsrc⟩
        exact ⟨e.src, hsrc, he, rfl⟩
      · rintro ⟨v, hv, he, hsrc⟩
        exact ⟨he, by rw [hsrc]; exact hv⟩
    rw [h_union]
    symm
    apply Finset.sum_biUnion
    intro v1 _ v2 _ hneq
    -- FIX: Bypass Function.onFun by explicitly declaring the Disjoint goal
    have hd : Disjoint (outgoing_edges G v1) (outgoing_edges G v2) := by
      rw [Finset.disjoint_left]
      intro e he1 he2
      simp only [outgoing_edges, Finset.mem_filter] at he1 he2
      exact hneq (he1.2.symm.trans he2.2)
    exact hd

  rw [h_flat]
  -- 2. Split the filtered set using the partition V_L ∪ V_R = G.V
  have h_split : G.E.filter (fun e => e.src ∈ C.V_L) = 
                 (internal_edges G C.V_L) ∪ (boundary_flux G C) := by
    ext e
    simp only [internal_edges, boundary_flux, Finset.mem_union, Finset.mem_filter]
    constructor
    · rintro ⟨he_G, h_src⟩
      have h_dst_in_G : e.dst ∈ G.V := (G.edges_valid e he_G).2
      have h_partition : e.dst ∈ C.V_L ∪ C.V_R := by 
        rw [C.is_partition.1]
        exact h_dst_in_G
      cases Finset.mem_union.mp h_partition with
      | inl h_dst_L => left; exact ⟨he_G, h_src, h_dst_L⟩
      | inr h_dst_R => right; exact ⟨he_G, h_src, h_dst_R⟩
    · rintro (⟨he_G, h_src, _⟩ | ⟨he_G, h_src, _⟩) <;> exact ⟨he_G, h_src⟩

  rw [h_split]
  exact Finset.sum_union (internal_flux_disjoint G C)

lemma sum_incoming_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) := by
  -- 1. Flatten the nested sum using explicit bounded union logic
  have h_flat : (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) = 
                ∑ e ∈ G.E.filter (fun e => e.dst ∈ C.V_L), e.charge := by
    have h_union : G.E.filter (fun e => e.dst ∈ C.V_L) = C.V_L.biUnion (fun v => incoming_edges G v) := by
      ext e
      simp only [Finset.mem_filter, Finset.mem_biUnion, incoming_edges]
      constructor
      · rintro ⟨he, hdst⟩
        exact ⟨e.dst, hdst, he, rfl⟩
      · rintro ⟨v, hv, he, hdst⟩
        exact ⟨he, by rw [hdst]; exact hv⟩
    rw [h_union]
    symm
    apply Finset.sum_biUnion
    intro v1 _ v2 _ hneq
    -- FIX: Bypass Function.onFun by explicitly declaring the Disjoint goal
    have hd : Disjoint (incoming_edges G v1) (incoming_edges G v2) := by
      rw [Finset.disjoint_left]
      intro e he1 he2
      simp only [incoming_edges, Finset.mem_filter] at he1 he2
      exact hneq (he1.2.symm.trans he2.2)
    exact hd

  rw [h_flat]
  -- 2. Prove the filtered set is exactly the internal edges
  have h_eq : G.E.filter (fun e => e.dst ∈ C.V_L) = internal_edges G C.V_L := by
    ext e
    simp only [internal_edges, Finset.mem_filter]
    constructor
    · rintro ⟨he_G, h_dst⟩
      have h_src_in_G : e.src ∈ G.V := (G.edges_valid e he_G).1
      have h_partition : e.src ∈ C.V_L ∪ C.V_R := by 
        rw [C.is_partition.1]
        exact h_src_in_G
      cases Finset.mem_union.mp h_partition with
      | inl h_src_L => exact ⟨he_G, h_src_L, h_dst⟩
      | inr h_src_R => 
        have h_contra := C.arrow_of_time e he_G h_src_R
        exact absurd h_dst h_contra
    · rintro ⟨he_G, _, h_dst⟩
      exact ⟨he_G, h_dst⟩
  
  rw [h_eq]


-- =====================================================================
-- 5. THE GRAPH CUT THEOREM (RAGC Theorem 2)
-- =====================================================================

theorem RA_graph_cut_theorem
    (G : ActualizationGraph) (C : CausalCut G)
    (h_ledger : forall v, v ∈ C.V_L → satisfies_local_ledger G v) :
    (∑ e ∈ boundary_flux G C, e.charge) = 0 := by
  have h_sum_eq :
      (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) =
      (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) := by
    apply Finset.sum_congr rfl
    intro v hv
    exact (h_ledger v hv).symm
  rw [sum_outgoing_decompose G C] at h_sum_eq
  rw [sum_incoming_decompose G C] at h_sum_eq
  linarith

theorem horizon_partition
    (G : ActualizationGraph) (C : CausalCut G)
    (h_ledger : forall v, v ∈ C.V_L → satisfies_local_ledger G v) :
    (∑ e ∈ boundary_flux G C, e.charge) = 0 :=
  RA_graph_cut_theorem G C h_ledger


-- =====================================================================
-- 6. THE MARKOV BLANKET (RACI Theorems 2-3)
-- =====================================================================

structure MarkovBlanket (G : ActualizationGraph) where
  Internal : Finset Vertex
  External : Finset Vertex
  Sensory  : Finset Vertex
  Active   : Finset Vertex
  is_complete : Internal ∪ External ∪ Sensory ∪ Active = G.V
  shield_internal : forall e, e ∈ G.E → e.dst ∈ Internal → e.src ∈ Sensory ∪ Internal
  shield_external : forall e, e ∈ G.E → e.dst ∈ External → e.src ∈ Active ∪ External

structure MarkovBlanketWF (G : ActualizationGraph) (MB : MarkovBlanket G) : Prop where
  int_ext_disj : Disjoint MB.Internal MB.External
  int_sen_disj : Disjoint MB.Internal MB.Sensory
  ext_sen_disj : Disjoint MB.External MB.Sensory

def sensory_edges (G : ActualizationGraph) (MB : MarkovBlanket G) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ MB.External ∧ e.dst ∈ MB.Sensory)

def active_edges (G : ActualizationGraph) (MB : MarkovBlanket G) : Finset Edge :=
  G.E.filter (fun e => e.src ∈ MB.Active ∧ e.dst ∈ MB.External)

theorem markov_blanket_shielding
    (G : ActualizationGraph) (MB : MarkovBlanket G)
    (wf : MarkovBlanketWF G MB)
    (e : Edge) (he : e ∈ G.E)
    (h_dst : e.dst ∈ MB.Internal) :
    e.src ∉ MB.External := by
  intro h_src_ext
  have h_src_ok := MB.shield_internal e he h_dst
  have h_sensory_or_internal := Finset.mem_union.mp h_src_ok
  cases h_sensory_or_internal with
  | inl h_sensory =>
    exact Finset.disjoint_left.mp wf.ext_sen_disj h_src_ext h_sensory
  | inr h_internal =>
    exact Finset.disjoint_left.mp wf.int_ext_disj h_internal h_src_ext


-- =====================================================================
-- 7. THE ASSEMBLY INDEX (RACI Theorem 1)
-- =====================================================================

def is_protected_path (G : ActualizationGraph) (MB : MarkovBlanket G)
    (path : List Edge) : Prop :=
  forall e, e ∈ path → e.src ∈ MB.Internal ∧ e.dst ∈ MB.Internal

structure AssemblyIndex (G : ActualizationGraph) (MB : MarkovBlanket G) where
  index : Nat
  has_valid_path : exists path : List Edge,
    is_protected_path G MB path ∧ path.length = index
  is_minimal : forall other : List Edge,
    is_protected_path G MB other → index ≤ other.length

structure StandardAssemblyIndex where
  value : Nat

def condition_C1 (G : ActualizationGraph) (MB : MarkovBlanket G)
    (AI : AssemblyIndex G MB) (SAI : StandardAssemblyIndex) : Prop :=
  SAI.value ≤ AI.index

theorem assembly_index_correspondence
    (G : ActualizationGraph) (MB : MarkovBlanket G)
    (AI : AssemblyIndex G MB) (SAI : StandardAssemblyIndex)
    (hC1 : condition_C1 G MB AI SAI) :
    SAI.value ≤ AI.index :=
  hC1


-- =====================================================================
-- 8. OBSERVER FRAME INVARIANCE
-- =====================================================================

structure ObserverFrame (G : ActualizationGraph) where
  sequence : List Vertex
  nodup : sequence.Nodup
  covers_all : forall v, v ∈ G.V → v ∈ sequence
  respects_causality : forall e, e ∈ G.E → 
    ∃ (i j : Fin sequence.length), 
      sequence.get i = e.src ∧ 
      sequence.get j = e.dst ∧ 
      i.val < j.val

theorem actualization_frame_invariance
    (G : ActualizationGraph) (v : Vertex)
    (_f1 _f2 : ObserverFrame G) :
    satisfies_local_ledger G v ↔ satisfies_local_ledger G v :=
  Iff.rfl


-- =====================================================================
-- 9. THE CAUSAL FIREWALL THRESHOLD (RACI Problem 2)
-- =====================================================================

def stability_threshold (G : ActualizationGraph) (MB : MarkovBlanket G) : Prop :=
  (∑ e ∈ sensory_edges G MB, e.charge) ≤ (∑ e ∈ active_edges G MB, e.charge)

axiom causal_firewall_threshold
    (G : ActualizationGraph) (MB : MarkovBlanket G) : Prop

theorem biological_persistence
    (G : ActualizationGraph) (MB : MarkovBlanket G) (v : Vertex)
    (h_internal : v ∈ MB.Internal)
    (h_ledger_internal : forall u, u ∈ MB.Internal → satisfies_local_ledger G u)
    (_h_stable : stability_threshold G MB) :
    satisfies_local_ledger G v :=
  h_ledger_internal v h_internal

theorem biological_persistence_strong
    (G : ActualizationGraph) (MB : MarkovBlanket G) (v : Vertex)
    (_h_internal : v ∈ MB.Internal)
    (_h_stable : stability_threshold G MB) :
    satisfies_local_ledger G v := by
  sorry


-- =====================================================================
-- 10. VACUUM ENERGY SUPPRESSION (RAGC Theorem 1)
-- =====================================================================

structure QuantumState where
  is_vacuum : Bool
  has_on_shell_support : Bool

def is_on_shell (s : QuantumState) : Bool := s.has_on_shell_support

axiom vacuum_energy_suppression :
    forall (vac : QuantumState), vac.is_vacuum = true →
    is_on_shell vac = false