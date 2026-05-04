"""
    Seeds

Initial-condition constructors for the BDG growth simulator.

Per RA, every DAG nucleates from a parent — either as a vacuum
nucleation (no inherited ledger) or as a severance daughter (ledger
inherited from a parent black-hole horizon). The simulator distinguishes
these explicitly via separate constructors.

Additionally, for testing and exploration, this module provides
canonical-motif seeds: the chain-4 motif, the symmetric-branch motif,
and the asymmetric-branch motif from Paper I §D1.

Per the kernel saturation theorem, the empty-DAG starting condition
under strict S>0 collapses to all-isolated growth (this is what the
April 28 2026 simulator runs demonstrated, and is consistent with the
Lean strict-S>0 convention). This module's seeds give the simulator
non-empty initial conditions matching the canonical RA assumption that
DAGs nucleate at saturation.
"""
module Seeds

using ..BDGGrow
using ..Ledger
import Random

export vacuum_nucleation, severance_daughter
export seed_chain, seed_sym_branch, seed_asym_branch
export seed_dense_random
export local_mu

"""
    vacuum_nucleation() -> DAG

The vacuum nucleation case: an empty DAG with no inherited ledger.
Equivalent to `DAG()` but explicit about its semantic role.

Note: as the April 28 2026 simulator runs showed, growth from this
seed under strict S>0 collapses to isolated vertices. This is not a
useful seed for studying RA dynamics; it's provided only for completeness.
"""
vacuum_nucleation() = DAG()

"""
    severance_daughter(parent_boundary_ledger) -> DAG

A daughter DAG nucleated from a parent severance event, carrying
inherited boundary ledger.

Currently, the inherited ledger is recorded but not yet used to seed
graph structure — this is a stub for the architecture. Once the
sign-source rule (RA-OPEN-CHARGE-SIGN-001) is formalized, this will
build initial vertices reflecting the parent's boundary state.

Returns an empty DAG with a note about the inherited ledger.
"""
function severance_daughter(parent_boundary_ledger::VertexLedger)
    d = DAG()
    # TODO: once the sign-source rule is formalized, populate initial
    # vertices reflecting the inherited ledger. For now, this is a
    # placeholder marking the boundary case.
    # Inherited ledger is recorded in the return for tracking purposes
    # via a future field on DAG; for now, the caller is responsible.
    d
end

# ----------------------------------------------------------------------
# Canonical D1 motif seeds (from Paper I §D1, Lean: RA_D1_Core_draft.lean)
# ----------------------------------------------------------------------

"""
    seed_chain(k::Int) -> DAG

A length-k chain: vertices 1 → 2 → ... → k. The k-th vertex has BDG
profile depending on k:
  - k=1: N=(0,0,0,0), S=1 (isolated)
  - k=2: N=(1,0,0,0), S=0 (boundary)
  - k=3: N=(1,1,0,0), S=9 (chain-2 stable motif)
  - k=4: N=(1,1,1,0), S=-7 (chain-3 filtered)
  - k≥5: N=(1,1,1,1), S=1 (chain-4 fixed point, BDG window saturated)
"""
function seed_chain(k::Int)
    @assert k >= 1
    d = DAG()
    addvertex!(d, Int[])
    for i in 2:k
        addvertex!(d, [i-1])
    end
    d
end

"""
    seed_sym_branch() -> DAG

The symmetric-branch base graph from Paper I §D1b:
  vertices 1, 2 (incomparable), 3 with parents {1, 2}, 4 with parent {3}.

Vertex 4 has BDG profile N=(1, 2, 0, 0), S=18: the symmetric-branch motif.
"""
function seed_sym_branch()
    d = DAG()
    addvertex!(d, Int[])      # v_1
    addvertex!(d, Int[])      # v_2
    addvertex!(d, [1, 2])     # v_3
    addvertex!(d, [3])        # v_4
    d
end

"""
    seed_asym_branch() -> DAG

The asymmetric-branch base graph from Paper I §D1b:
  vertices 1 → 2, then 3 (incomparable to 1), then 4 with parents {2, 3}.

Vertex 4 has BDG profile N=(2, 1, 0, 0), S=8: the asymmetric-branch motif.
"""
function seed_asym_branch()
    d = DAG()
    addvertex!(d, Int[])      # v_1
    addvertex!(d, [1])        # v_2
    addvertex!(d, Int[])      # v_3
    addvertex!(d, [2, 3])     # v_4
    d
end

"""
    seed_dense_random(n::Int; rng=...) -> DAG

A randomly-grown saturated initial DAG of size n.

Method: build n vertices, each with a random subset of all current
vertices as its parents (each vertex included with probability p = 0.5).
This produces a high-density DAG that is NOT BDG-filtered — it is meant
purely as a saturated initial condition for studying what the dynamics
does given an already-rich graph.

This seed does not respect the BDG filter or LLC at construction time.
It is the analog of "high-mu starting condition" — saturated, with no
pretense that it was produced by RA dynamics.
"""
function seed_dense_random(n::Int; rng=Random.default_rng(), p::Float64=0.5)
    d = DAG()
    addvertex!(d, Int[])  # v_1 always isolated
    for v in 2:n
        # Pick parents from {1..v-1} with probability p each
        parents = Int[i for i in 1:(v-1) if rand(rng) < p]
        addvertex!(d, parents)
    end
    d
end

# ----------------------------------------------------------------------
# Local density estimator (mu)
# ----------------------------------------------------------------------

"""
    local_mu(d::DAG, v::Int) -> Float64

A simple local-density estimator for vertex v, defined as
    |ancestors(v)| / max(1, depth(v))
where depth(v) is the longest chain length ending at v.

This is a heuristic stand-in for the formal density parameter μ that
appears in the Poisson-CSG approximation. It approaches 1 for a sparse
chain-like region and grows for densely-branched regions.

For now this is a quick-and-dirty observable; a proper RA-native local-
density definition is itself a piece of the simulator-vs-Lean alignment
work.
"""
function local_mu(d::DAG, v::Int)
    anc = d.ancestors[v]
    if isempty(anc)
        return 0.0
    end
    # Compute longest chain length ending at v: 1 + max_u_in_anc(longest chain to u)
    # Since the DAG is small, we can do this with memoization.
    longest = Dict{Int, Int}()
    function depth_of(u::Int)::Int
        if haskey(longest, u); return longest[u]; end
        anc_u = d.ancestors[u]
        if isempty(anc_u)
            longest[u] = 0
            return 0
        end
        max_d = 0
        for w in anc_u
            d_w = depth_of(w) + 1
            if d_w > max_d; max_d = d_w; end
        end
        longest[u] = max_d
        return max_d
    end
    chain_len = 0
    for u in anc
        d_u = depth_of(u) + 1   # +1 for the edge u -> v
        if d_u > chain_len; chain_len = d_u; end
    end
    return length(anc) / max(1, chain_len)
end

# Random module imported at top for seed_dense_random

end # module
