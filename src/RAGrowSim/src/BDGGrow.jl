"""
    BDGGrow

Core engine for the BDG growth simulator.

Substrate: a finite labeled DAG. No metric, no signature, no coordinates.
Vertices are added one at a time with a specified set of immediate
predecessors (parents). Transitive closure is maintained incrementally.

The BDG-d=4 score for a candidate vertex v with past P is:

    S(v) = 1 - N_1 + 9 N_2 - 16 N_3 + 8 N_4

where N_k = #{u prec v : interval (u,v) has cardinality k-1}, i.e., the
number of strict predecessors u of v such that exactly k-1 vertices lie
strictly between u and v in the causal order.

Index convention (matches d4u02_enumeration.py):
  N_1 = #{u : 0 strict-between} (immediate predecessors)
  N_2 = #{u : 1 strict-between}
  N_3 = #{u : 2 strict-between}
  N_4 = #{u : 3 strict-between}

Verified test cases (must pass before any dynamics):
  - Empty DAG, first vertex: N=(0,0,0,0), S=1
  - Length-4 chain: at v_5 with parent {v_4}, N=(1,1,1,1), S=1
  - Diamond v_1 < {v_2, v_3}, propose v_4 with parents {v_2,v_3}: N=(2,0,1,0), S=-17
"""
module BDGGrow

export DAG, addvertex!, ancestorsof, profile, bdgscore, BDG_C

# Verified BDG d=4 coefficients (Lean-verified, O14 uniqueness theorem)
const BDG_C = (1, -1, 9, -16, 8)

"""
    DAG

Finite directed acyclic graph with explicit immediate-predecessor sets and
incrementally maintained transitive closures (strict ancestors).

Fields:
  n:          current number of vertices (vertices labeled 1..n)
  parents:    parents[v] = BitSet of immediate predecessors of vertex v
  ancestors:  ancestors[v] = BitSet of strict ancestors of v (transitive closure
              of parents, NOT including v itself)
"""
mutable struct DAG
    n::Int
    parents::Vector{BitSet}
    ancestors::Vector{BitSet}

    DAG() = new(0, BitSet[], BitSet[])
end

"""
    addvertex!(d::DAG, parent_set) -> Int

Add a new vertex to the DAG with the given parent set. Returns the
1-based label of the new vertex. The parent_set is treated as the
immediate predecessors; ancestors are computed as the transitive closure.

The caller is responsible for ensuring parent_set is a valid antichain
of the current DAG when sequential-growth semantics are required (the
DAG type itself does not enforce antichain structure on parents — it
just records what was provided).
"""
function addvertex!(d::DAG, parent_set)
    v = d.n + 1
    parents_v = BitSet(parent_set)
    for p in parents_v
        @assert 1 <= p <= d.n "parent $p not a valid existing vertex (n=$(d.n))"
    end
    # Ancestors of v = parents ∪ ancestors of each parent
    anc_v = BitSet()
    union!(anc_v, parents_v)
    for p in parents_v
        union!(anc_v, d.ancestors[p])
    end
    push!(d.parents, parents_v)
    push!(d.ancestors, anc_v)
    d.n = v
    return v
end

"""
    ancestorsof(d::DAG, v::Int) -> BitSet

Strict ancestors of v (does not include v itself). Empty for an isolated
or initial vertex.
"""
ancestorsof(d::DAG, v::Int) = d.ancestors[v]

"""
    proposed_ancestors(d::DAG, parent_set) -> BitSet

For a hypothetical new vertex v with the given immediate predecessors
(not yet added), compute what its strict-ancestor BitSet would be.
"""
function proposed_ancestors(d::DAG, parent_set)
    anc = BitSet()
    for p in parent_set
        push!(anc, p)
        union!(anc, d.ancestors[p])
    end
    return anc
end

"""
    profile(d::DAG, parent_set) -> NTuple{4,Int}

For a hypothetical new vertex v with given immediate predecessors,
compute (N_1, N_2, N_3, N_4) where N_k = number of strict ancestors u of v
such that the interval (u, v) has cardinality (k-1). Cardinalities ≥ 4 are
not counted (BDG-d=4 truncation).
"""
function profile(d::DAG, parent_set)
    anc_v = proposed_ancestors(d, parent_set)
    n1 = 0; n2 = 0; n3 = 0; n4 = 0
    for u in anc_v
        # interval (u, v) = {w : u prec w prec v}
        # w prec v iff w in anc_v
        # u prec w iff u in d.ancestors[w]
        card = 0
        for w in anc_v
            if w != u && u in d.ancestors[w]
                card += 1
                card > 3 && break    # >=4 doesn't contribute; early exit
            end
        end
        if     card == 0; n1 += 1
        elseif card == 1; n2 += 1
        elseif card == 2; n3 += 1
        elseif card == 3; n4 += 1
        end
    end
    return (n1, n2, n3, n4)
end

"""
    bdgscore(N::NTuple{4,Int}) -> Int

S = 1 - N_1 + 9 N_2 - 16 N_3 + 8 N_4 (BDG-d=4 score with c_0=1).
"""
@inline bdgscore(N::NTuple{4,Int}) =
    BDG_C[1] + BDG_C[2]*N[1] + BDG_C[3]*N[2] + BDG_C[4]*N[3] + BDG_C[5]*N[4]

end # module
