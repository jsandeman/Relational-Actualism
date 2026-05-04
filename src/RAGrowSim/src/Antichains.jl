"""
    Antichains

Enumeration of all antichains of a finite DAG.

Algorithm: recursive extension.
  An antichain is a subset of vertices, no two comparable in the partial
  order. We enumerate by maintaining a "candidate pool" of vertices that
  could be added to the current partial antichain without violating the
  antichain property.

  Starting with candidate pool = all vertices, current = empty:
  - emit current as one valid antichain
  - for each candidate v in pool, recurse with current ∪ {v} and pool
    restricted to candidates strictly later in label order AND not
    comparable to v.

  The "strictly later in label order" rule prevents emitting the same
  antichain twice (it imposes a canonical ordering).

  Comparable-to-v means: v is an ancestor of the candidate, or the
  candidate is an ancestor of v.

  This visits each antichain exactly once.
"""
module Antichains

# BDGGrow is loaded by the parent module (RAGrowSim.jl).
# We reference it via the parent's namespace.
using ..BDGGrow

export all_antichains

"""
    all_antichains(d::DAG) -> Vector{BitSet}

Enumerate every antichain of the DAG, including the empty antichain.
The result is a Vector of BitSet, one per distinct antichain.

Tractable for n up to roughly 30; antichain count grows superpolynomially
(in the worst case, exponentially) with n.
"""
function all_antichains(d::DAG)
    out = BitSet[]
    push!(out, BitSet())  # empty antichain
    if d.n == 0
        return out
    end
    # The "comparable" relation: v and w are comparable iff one is an
    # ancestor of the other.
    current = BitSet()
    initial_pool = BitSet(1:d.n)
    _extend!(out, d, current, initial_pool, 1)
    return out
end

"""
Recursive helper. Tries to extend the current antichain with each
candidate that is (a) at index >= start, (b) in the pool.
"""
function _extend!(out::Vector{BitSet}, d::DAG, current::BitSet,
                  pool::BitSet, start::Int)
    for v in start:d.n
        if !(v in pool); continue; end
        # Add v to current.
        push!(current, v)
        # Restrict the pool: remove v itself, and remove any vertex
        # that is comparable to v (ancestor of v OR descendant of v).
        new_pool = BitSet()
        for w in pool
            if w == v; continue; end
            if w in d.ancestors[v]; continue; end           # w is ancestor of v
            if v in d.ancestors[w]; continue; end           # w is descendant of v
            push!(new_pool, w)
        end
        push!(out, copy(current))
        _extend!(out, d, current, new_pool, v + 1)
        delete!(current, v)
    end
end

end # module
