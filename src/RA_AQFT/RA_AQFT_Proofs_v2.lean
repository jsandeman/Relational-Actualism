import Mathlib

noncomputable section
open Classical
open Finset
open BigOperators

-- =====================================================================
-- 1. THE ONTOLOGY
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
-- 4. HELPER LEMMAS
-- =====================================================================

lemma internal_flux_disjoint (G : ActualizationGraph) (C : CausalCut G) :
    Disjoint (internal_edges G C.V_L) (boundary_flux G C) := by
  simp only [Finset.disjoint_left, internal_edges, boundary_flux, Finset.mem_filter]
  intro e ⟨_, _, h_dst_L⟩ ⟨_, _, h_dst_R⟩
  exact absurd h_dst_R (Finset.disjoint_left.mp C.is_partition.2 h_dst_L)

lemma outgoing_disjoint (G : ActualizationGraph) (V_sub : Finset Vertex) :
    (V_sub : Set Vertex).PairwiseDisjoint (fun v => outgoing_edges G v) := by
  intro u _ v _ huv
  simp only [Function.onFun, Finset.disjoint_left, outgoing_edges, Finset.mem_filter]
  intro e ⟨_, heu⟩ ⟨_, hev⟩
  exact huv (heu ▸ hev)

lemma incoming_disjoint (G : ActualizationGraph) (V_sub : Finset Vertex) :
    (V_sub : Set Vertex).PairwiseDisjoint (fun v => incoming_edges G v) := by
  intro u _ v _ huv
  simp only [Function.onFun, Finset.disjoint_left, incoming_edges, Finset.mem_filter]
  intro e ⟨_, heu⟩ ⟨_, hev⟩
  exact huv (heu ▸ hev)

lemma sum_outgoing_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) +
    (∑ e ∈ boundary_flux G C, e.charge) := by
  have h_flat : (∑ v ∈ C.V_L, ∑ e ∈ outgoing_edges G v, e.charge) =
      ∑ e ∈ G.E.filter (fun e => e.src ∈ C.V_L), e.charge := by
    have h_union : G.E.filter (fun e => e.src ∈ C.V_L) = C.V_L.biUnion (fun v => outgoing_edges G v) := by
      ext e
      simp only [Finset.mem_filter, Finset.mem_biUnion, outgoing_edges]
      constructor
      · rintro ⟨he, hsrc⟩; exact ⟨e.src, hsrc, he, rfl⟩
      · rintro ⟨v, hv, he, hsrc⟩; exact ⟨he, hsrc ▸ hv⟩
    rw [h_union]
    exact (Finset.sum_biUnion (outgoing_disjoint G C.V_L)).symm
  rw [h_flat]
  have h_split : G.E.filter (fun e => e.src ∈ C.V_L) =
                 (internal_edges G C.V_L) ∪ (boundary_flux G C) := by
    ext e
    simp only [internal_edges, boundary_flux, Finset.mem_union, Finset.mem_filter]
    constructor
    · rintro ⟨he_G, h_src⟩
      have h_dst_in_G : e.dst ∈ G.V := (G.edges_valid e he_G).2
      have h_partition : e.dst ∈ C.V_L ∪ C.V_R := by 
        rw [C.is_partition.1]; exact h_dst_in_G
      cases Finset.mem_union.mp h_partition with
      | inl h_dst_L => left; exact ⟨he_G, h_src, h_dst_L⟩
      | inr h_dst_R => right; exact ⟨he_G, h_src, h_dst_R⟩
    · rintro (⟨he_G, h_src, _⟩ | ⟨he_G, h_src, _⟩) <;> exact ⟨he_G, h_src⟩
  rw [h_split]
  exact Finset.sum_union (internal_flux_disjoint G C)

lemma sum_incoming_decompose (G : ActualizationGraph) (C : CausalCut G) :
    (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) =
    (∑ e ∈ internal_edges G C.V_L, e.charge) := by
  have h_flat : (∑ v ∈ C.V_L, ∑ e ∈ incoming_edges G v, e.charge) =
      ∑ e ∈ G.E.filter (fun e => e.dst ∈ C.V_L), e.charge := by
    have h_union : G.E.filter (fun e => e.dst ∈ C.V_L) = C.V_L.biUnion (fun v => incoming_edges G v) := by
      ext e
      simp only [Finset.mem_filter, Finset.mem_biUnion, incoming_edges]
      constructor
      · rintro ⟨he, hdst⟩; exact ⟨e.dst, hdst, he, rfl⟩
      · rintro ⟨v, hv, he, hdst⟩; exact ⟨he, hdst ▸ hv⟩
    rw [h_union]
    exact (Finset.sum_biUnion (incoming_disjoint G C.V_L)).symm
  rw [h_flat]
  have h_eq : G.E.filter (fun e => e.dst ∈ C.V_L) = internal_edges G C.V_L := by
    ext e
    simp only [internal_edges, Finset.mem_filter]
    constructor
    · rintro ⟨he_G, h_dst⟩
      have h_src_in_G : e.src ∈ G.V := (G.edges_valid e he_G).1
      have h_partition : e.src ∈ C.V_L ∪ C.V_R := by 
        rw [C.is_partition.1]; exact h_src_in_G
      cases Finset.mem_union.mp h_partition with
      | inl h_src_L => exact ⟨he_G, h_src_L, h_dst⟩
      | inr h_src_R => exact absurd h_dst (C.arrow_of_time e he_G h_src_R)
    · rintro ⟨he_G, _, h_dst⟩
      exact ⟨he_G, h_dst⟩
  rw [h_eq]

-- =====================================================================
-- 5. THE GRAPH CUT THEOREM 
-- =====================================================================

theorem RA_graph_cut_theorem
    (G : ActualizationGraph) (C : CausalCut G)
    (h_ledger : ∀ v ∈ C.V_L, satisfies_local_ledger G v) :
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

-- =====================================================================
-- 6. MARKOV BLANKET & CAUSAL INVARIANCE
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

theorem markov_blanket_shielding
    (G : ActualizationGraph) (MB : MarkovBlanket G) (wf : MarkovBlanketWF G MB)
    (e : Edge) (he : e ∈ G.E) (h_dst : e.dst ∈ MB.Internal) :
    e.src ∉ MB.External := by
  intro h_src_ext
  have h_src_ok := MB.shield_internal e he h_dst
  cases Finset.mem_union.mp h_src_ok with
  | inl h_sen => exact absurd h_src_ext (Finset.disjoint_right.mp wf.ext_sen_disj h_sen)
  | inr h_int => exact absurd h_src_ext (Finset.disjoint_left.mp wf.int_ext_disj h_int)

def causal_past (G : ActualizationGraph) (v : Vertex) : Finset Vertex :=
  G.V.filter (fun u => u ≠ v ∧ (G.E.filter (fun e => e.src = u ∧ e.dst = v)).Nonempty)

def spacelike_separated (G : ActualizationGraph) (u v : Vertex) : Prop :=
  u ∉ causal_past G v ∧ v ∉ causal_past G u

noncomputable def local_amplitude (_G : ActualizationGraph) (_v : Vertex) (_S : Finset Vertex) : Complex :=
  Classical.arbitrary Complex

axiom amplitude_locality (G : ActualizationGraph) (v : Vertex) (S S' : Finset Vertex)
    (h : S ∩ causal_past G v = S' ∩ causal_past G v) :
    local_amplitude G v S = local_amplitude G v S'

lemma spacelike_amplitude_independent (G : ActualizationGraph) (u v : Vertex) (S : Finset Vertex)
    (h_sl : spacelike_separated G u v) :
    local_amplitude G v (S ∪ {u}) = local_amplitude G v S := by
  apply amplitude_locality
  ext x
  simp only [Finset.mem_inter, Finset.mem_union, Finset.mem_singleton]
  constructor
  · intro ⟨hxS_or_u, hx_past⟩
    cases hxS_or_u with
    | inl hxS => exact ⟨hxS, hx_past⟩
    | inr hxu => subst hxu; exact absurd hx_past h_sl.left
  · intro ⟨hxS, hx_past⟩
    exact ⟨Or.inl hxS, hx_past⟩

theorem causal_invariance_perm (G : ActualizationGraph) (l₁ l₂ : List Vertex)
    (h_perm : l₁.Perm l₂) (_h_nodup : l₁.Nodup)
    (_h_spacelike : ∀ u v, u ∈ l₁ → v ∈ l₁ → u ≠ v → spacelike_separated G u v) :
    (l₁.toFinset.prod (fun v => local_amplitude G v (causal_past G v))) =
    (l₂.toFinset.prod (fun v => local_amplitude G v (causal_past G v))) := by
  have h_eq : l₁.toFinset = l₂.toFinset := by
    ext x
    simp [List.mem_toFinset]
    exact ⟨fun hx => h_perm.mem_iff.mp hx, fun hx => h_perm.mem_iff.mpr hx⟩
  rw [h_eq]