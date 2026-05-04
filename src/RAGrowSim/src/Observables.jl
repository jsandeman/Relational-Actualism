"""
    Observables

Compute observable statistics from a GrowthHistory.

  - profile_means: running mean of (N_1, N_2, N_3, N_4) up to each step n.
  - acceptance_ratios: at each step, n_admitted / n_candidates.
  - max_antichain_width: at each step, the size of the largest antichain
    in the resulting DAG.
"""
module Observables

using ..BDGGrow
using ..Antichains
using ..Dynamics

export running_profile_means, acceptance_ratios, max_antichain_widths,
       step_S_distribution, parent_count_distribution

"""
    running_profile_means(h::GrowthHistory) -> Vector{NTuple{4,Float64}}

Returns a vector v where v[n] is the running mean of (N_1..N_4) over the
first n vertex-additions in the history.
"""
function running_profile_means(h::GrowthHistory)
    out = Vector{NTuple{4,Float64}}(undef, length(h.steps))
    s1 = 0; s2 = 0; s3 = 0; s4 = 0
    for (i, step) in enumerate(h.steps)
        s1 += step.N[1]; s2 += step.N[2]
        s3 += step.N[3]; s4 += step.N[4]
        out[i] = (s1/i, s2/i, s3/i, s4/i)
    end
    return out
end

"""
    acceptance_ratios(h::GrowthHistory) -> Vector{Float64}

The fraction of antichain candidates admitted at each step.
"""
acceptance_ratios(h::GrowthHistory) =
    [step.n_admitted / step.n_candidates for step in h.steps]

"""
    max_antichain_widths(h::GrowthHistory; from_seed::DAG=DAG()) -> Vector{Int}

At each step, the size of the largest antichain in the DAG after adding
that vertex. Computed by replaying growth onto a copy of `from_seed`.

If the history was produced by a vacuum nucleation (`run_growth(target_n, seed)`
or `run_growth(DAG(), ...)`), the default `from_seed=DAG()` is correct.

If the history was produced by a seeded run (e.g. `run_growth(seed_chain(4), ...)`),
the caller must pass the same seed via `from_seed=seed_chain(4)`. Failure to
do so will result in invalid parent references during replay.

Expensive (O(antichains) per step). Use only for total DAG size up to ~25.
"""
function max_antichain_widths(h::GrowthHistory; from_seed::DAG=DAG())
    # Make a copy of the seed so we don't mutate the caller's DAG.
    d = DAG()
    for v in 1:from_seed.n
        addvertex!(d, from_seed.parents[v])
    end
    out = Int[]
    for step in h.steps
        addvertex!(d, step.parent_set)
        max_w = 0
        for A in all_antichains(d)
            l = length(A)
            l > max_w && (max_w = l)
        end
        push!(out, max_w)
    end
    return out
end

"""
    step_S_distribution(histories) -> Dict{Int,Int}

Across multiple histories, count the number of times each S value was
selected (the S of the chosen parent set, NOT the candidate distribution).
"""
function step_S_distribution(histories::AbstractVector{GrowthHistory})
    counts = Dict{Int,Int}()
    for h in histories, step in h.steps
        counts[step.S] = get(counts, step.S, 0) + 1
    end
    return counts
end

"""
    parent_count_distribution(histories) -> Dict{Int,Int}

Across multiple histories, count the number of times each parent-set size
was chosen.
"""
function parent_count_distribution(histories::AbstractVector{GrowthHistory})
    counts = Dict{Int,Int}()
    for h in histories, step in h.steps
        k = length(step.parent_set)
        counts[k] = get(counts, k, 0) + 1
    end
    return counts
end

end # module
