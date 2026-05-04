"""
    Dynamics

The RA growth rule from Paper I §Sequential Growth, with the corrections
identified in the April 28 2026 Lean audit:

  - Candidate parent sets are ALL SUBSETS of existing vertices (per
    Lean enumeration tables in RA_D1_Core_draft.lean lines 453-487),
    NOT just antichains. The BDG filter handles non-antichain subsets
    correctly via the cardinality structure (an ancestor of an immediate
    parent contributes at higher cardinality).

  - For each candidate parent set, the active LedgerRule produces a
    list of edge-ledger assignments. The (parent_set, ledger_assignment)
    pair is the joint candidate.

  - Filter: BDG score S > 0 AND vertex-level qN1 admissibility (LLC
    signature constraint). Per ChatGPT's note (Apr 28), per-vertex LLC
    is enforced over the eventual neighborhood, not at birth — so we
    only check the seven-value signature here, not Σ_in = Σ_out.

  - Pick uniformly among admitted joint candidates.

  - Add the new vertex with the chosen parent set and edge ledger.

Tractability: with all-subsets enumeration, the candidate count grows
as 2^n, which is infeasible past n ≈ 25. The `max_parent_size` parameter
caps enumeration at small subsets. For most BDG-stable motifs from D1,
parent sets have size ≤ 3, so max_parent_size=4 captures all known
canonical motifs while keeping enumeration tractable to n ~ 50. Setting
max_parent_size=typemax(Int) recovers exact dynamics at the cost of
exponential blowup.
"""
module Dynamics

using ..BDGGrow
using ..Ledger
using ..LedgerRules
using Random

export grow!, run_growth, GrowthStep, GrowthHistory, GrowthConfig

# Internal: yield all k-element subsets of 1:n in lexicographic order.
# Each subset returned as Vector{Int}. Memory-efficient: builds incrementally.
function _combinations(n::Int, k::Int)
    @assert k >= 0
    out = Vector{Int}[]
    if k == 0
        push!(out, Int[])
        return out
    end
    if k > n
        return out
    end
    # Standard recursion: combos starting with i ∈ 1..n-k+1
    indices = collect(1:k)
    while true
        push!(out, copy(indices))
        # Find rightmost index that can be incremented
        i = k
        while i >= 1 && indices[i] == n - k + i
            i -= 1
        end
        if i < 1
            break
        end
        indices[i] += 1
        for j in (i+1):k
            indices[j] = indices[j-1] + 1
        end
    end
    return out
end

"""
    GrowthConfig

Configurable parameters for one growth simulation.

Fields:
  ledger_rule::LedgerRule
      Strategy for assigning edge ledgers to candidate parent edges.
      Default: Neutral() — all edges carry zero ledger.

  max_parent_size::Int
      Maximum subset size considered when enumerating candidate parent
      sets. Defaults to 4 (covers all D1 canonical motifs). Set to
      typemax(Int) for exact full enumeration (slow past n~20).

  enforce_llc_signature::Bool
      If true, reject candidates whose qN1 sum lies outside {-3..+3}.
      With Neutral rule this never triggers; with EnumerateLLC it is
      already enforced inside the rule. Default: true (defense-in-depth).
"""
struct GrowthConfig
    ledger_rule::LedgerRule
    max_parent_size::Int
    enforce_llc_signature::Bool
end

GrowthConfig(; ledger_rule=Neutral(), max_parent_size::Int=4,
             enforce_llc_signature::Bool=true) =
    GrowthConfig(ledger_rule, max_parent_size, enforce_llc_signature)

"""
    GrowthStep

Record of a single growth step.

Fields:
  v             : label of the new vertex (1-based)
  parent_set    : BitSet of immediate predecessors of v
  edge_ledger   : Vector{EdgeLedger}, one per parent (in iteration order)
  vertex_qN1    : Int, signed N1-channel sum at v (the seven-value charge)
  N             : the (N_1, N_2, N_3, N_4) BDG profile of v
  S             : the BDG score
  n_candidates  : total joint (parent_set, ledger) candidates considered
  n_admitted    : number that passed all filters
"""
struct GrowthStep
    v::Int
    parent_set::BitSet
    edge_ledger::Vector{EdgeLedger}
    vertex_qN1::Int
    N::NTuple{4,Int}
    S::Int
    n_candidates::Int
    n_admitted::Int
end

"""
    GrowthHistory

Full history of a simulation run.
"""
struct GrowthHistory
    seed::Int
    target_n::Int
    config::GrowthConfig
    steps::Vector{GrowthStep}
end

"""
Internal: enumerate parent-set candidates as Vector{Int}.
Yields subsets of {1..d.n} of size 0..min(max_size, d.n) in canonical
(sorted) order. The empty subset is included.
"""
function enumerate_parent_sets(d::DAG, max_size::Int)
    out = Vector{Int}[Int[]]   # empty subset always first
    upper = min(max_size, d.n)
    for k in 1:upper
        for combo in _combinations(d.n, k)
            push!(out, combo)
        end
    end
    out
end

"""
    grow!(d::DAG, rng::AbstractRNG, config::GrowthConfig) -> GrowthStep

Apply one growth step to the DAG, mutating it. Returns a record.

Algorithm:
  1. Enumerate parent-set candidates (subsets of existing vertices,
     size ≤ config.max_parent_size).
  2. For each parent set:
     a. Compute the BDG profile N and score S.
     b. If S ≤ 0, skip.
     c. Ask the ledger rule for valid edge-ledger assignments.
     d. For each (parent_set, ledger_assignment), check qN1 admissibility.
  3. Uniformly pick among admitted joint candidates.
  4. Add the new vertex.
"""
function grow!(d::DAG, rng::AbstractRNG, config::GrowthConfig)
    parent_candidates = enumerate_parent_sets(d, config.max_parent_size)
    n_total = 0     # total joint candidates considered
    admitted = Tuple{Vector{Int}, Vector{EdgeLedger}, Int, NTuple{4,Int}, Int}[]
    # (parent_set, edge_ledger, vertex_qN1, N, S)

    for pset in parent_candidates
        N = profile(d, pset)
        S = bdgscore(N)
        if S <= 0
            # The ledger rule still produces some assignments, but they
            # all fail BDG filter. We count them in n_total for accurate
            # acceptance ratio reporting.
            ledger_assignments = enumerate_ledger_assignments(
                config.ledger_rule, d, pset)
            n_total += length(ledger_assignments)
            continue
        end
        ledger_assignments = enumerate_ledger_assignments(
            config.ledger_rule, d, pset)
        n_total += length(ledger_assignments)
        for ledger in ledger_assignments
            qN1_sum = sum((e.qN1 for e in ledger); init=0)
            if config.enforce_llc_signature && !(-3 <= qN1_sum <= 3)
                continue
            end
            push!(admitted, (pset, ledger, qN1_sum, N, S))
        end
    end

    @assert !isempty(admitted) "no admitted candidate (empty parent set should always pass with neutral or LLC ledger)"
    pset, ledger, qN1, N, S = rand(rng, admitted)
    v = addvertex!(d, pset)
    return GrowthStep(
        v, BitSet(pset), ledger, qN1, N, S, n_total, length(admitted)
    )
end

"""
    run_growth(seed_dag::DAG, target_n::Int, seed::Int; config=GrowthConfig())
        -> (DAG, GrowthHistory)

Run growth from a seed DAG to `seed_dag.n + target_n` vertices, given
PRNG seed. Returns the final DAG and the history.

The seed DAG is consumed (mutated) — pass a copy if you want to preserve it.

This is the new generic entry point. The convenience method
`run_growth(target_n, seed)` calls this with `vacuum_nucleation()` for
backward compatibility with the older test suite.
"""
function run_growth(seed_dag::DAG, target_n::Int, seed::Int;
                    config::GrowthConfig=GrowthConfig())
    rng = MersenneTwister(seed)
    d = seed_dag
    steps = GrowthStep[]
    for _ in 1:target_n
        step = grow!(d, rng, config)
        push!(steps, step)
    end
    return d, GrowthHistory(seed, target_n, config, steps)
end

# Backward-compatible signature: empty seed, default config.
function run_growth(target_n::Int, seed::Int)
    run_growth(DAG(), target_n, seed)
end

# Backward-compatible grow! with no config: uses default.
grow!(d::DAG, rng::AbstractRNG) = grow!(d, rng, GrowthConfig())

end # module
