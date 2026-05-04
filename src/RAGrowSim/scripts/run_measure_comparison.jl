#!/usr/bin/env julia
# scripts/run_measure_comparison.jl
#
# Compare BDG growth under three candidate measures:
#   parent_subset_uniform  -- current RAGrowSim dynamics
#   closure_uniform        -- quotient duplicate parent subsets by induced causal closure
#   profile_uniform        -- quotient further by BDG profile
#
# Neutral ledger only. This is a methodology diagnostic for RA-OPEN-GROWTH-MEASURE-001.
#
# Usage:
#   julia --project=. scripts/run_measure_comparison.jl [target_extra_n] [n_seeds] [outdir] [max_parent_size]

using Printf
using Statistics
using Random

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

const BDG = RAGrowSim.BDGGrow
const DYN = RAGrowSim.Dynamics

target_extra_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 25
n_seeds = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 50
outdir = length(ARGS) >= 3 ? ARGS[3] : "outputs/measure_comparison"
max_parent_size = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 4

mkpath(outdir)

seed_builders = Dict(
    "chain2" => () -> seed_chain(2),
    "chain4" => () -> seed_chain(4),
    "sym_branch" => () -> seed_sym_branch(),
    "asym_branch" => () -> seed_asym_branch(),
)

measures = ["parent_subset_uniform", "closure_uniform", "profile_uniform"]

function closure_key(anc::BitSet)::String
    xs = sort(collect(anc))
    return isempty(xs) ? "" : join(xs, ";")
end

function profile_key(N::NTuple{4,Int})::String
    return string(N[1], "|", N[2], "|", N[3], "|", N[4])
end

function frontier_of_closure(d::DAG, closure::BitSet)::Vector{Int}
    out = Int[]
    for x in closure
        maximal = true
        for y in closure
            if x != y && (x in d.ancestors[y])
                maximal = false
                break
            end
        end
        if maximal
            push!(out, x)
        end
    end
    sort!(out)
    return out
end

struct Cand
    orig_pset::Vector{Int}
    frontier_pset::Vector{Int}
    closure_key::String
    profile_key::String
    N::NTuple{4,Int}
    S::Int
end

function admitted_candidates(d::DAG; max_parent_size::Int=4)
    out = Cand[]
    for pset in DYN.enumerate_parent_sets(d, max_parent_size)
        N = profile(d, pset)
        S = bdgscore(N)
        if S <= 0
            continue
        end
        anc = BDG.proposed_ancestors(d, pset)
        f = frontier_of_closure(d, anc)
        push!(out, Cand(copy(pset), f, closure_key(anc), profile_key(N), N, S))
    end
    return out
end

function choose_candidate(rng::AbstractRNG, cands::Vector{Cand}, measure::String)::Cand
    if measure == "parent_subset_uniform"
        return rand(rng, cands)
    elseif measure == "closure_uniform"
        by_closure = Dict{String,Cand}()
        for c in cands
            if !haskey(by_closure, c.closure_key)
                by_closure[c.closure_key] = c
            end
        end
        keys_vec = collect(keys(by_closure))
        return by_closure[rand(rng, keys_vec)]
    elseif measure == "profile_uniform"
        by_profile = Dict{String,Dict{String,Cand}}()
        for c in cands
            if !haskey(by_profile, c.profile_key)
                by_profile[c.profile_key] = Dict{String,Cand}()
            end
            if !haskey(by_profile[c.profile_key], c.closure_key)
                by_profile[c.profile_key][c.closure_key] = c
            end
        end
        pkeys = collect(keys(by_profile))
        pkey = rand(rng, pkeys)
        cdict = by_profile[pkey]
        ckeys = collect(keys(cdict))
        return cdict[rand(rng, ckeys)]
    else
        error("unknown measure: $measure")
    end
end

function local_mu_v4_from_profile(N::NTuple{4,Int})::Float64
    # Invert V4 = μ + μ²/2 + μ³/6 + μ⁴/24 by bisection.
    V = N[1] + N[2] + N[3] + N[4]
    if V == 0
        return 0.0
    end
    f(mu) = mu + mu^2/2 + mu^3/6 + mu^4/24 - V
    lo = 0.0
    hi = max(1.0, Float64(V))
    while f(hi) < 0
        hi *= 2
    end
    for _ in 1:80
        mid = (lo + hi) / 2
        if f(mid) < 0
            lo = mid
        else
            hi = mid
        end
    end
    return (lo + hi) / 2
end

function run_one(seed_builder, run_seed::Int, measure::String)
    rng = MersenneTwister(run_seed)
    d = seed_builder()
    rows = Vector{NamedTuple}()
    for step_idx in 1:target_extra_n
        cands = admitted_candidates(d; max_parent_size=max_parent_size)
        @assert !isempty(cands)
        c = choose_candidate(rng, cands, measure)
        pset_to_add = measure == "parent_subset_uniform" ? c.orig_pset : c.frontier_pset
        v = addvertex!(d, pset_to_add)
        push!(rows, (
            step_idx=step_idx,
            v=v,
            N1=c.N[1], N2=c.N[2], N3=c.N[3], N4=c.N[4],
            V4=c.N[1]+c.N[2]+c.N[3]+c.N[4],
            S=c.S,
            parent_size=length(pset_to_add),
            orig_parent_size=length(c.orig_pset),
            frontier_parent_size=length(c.frontier_pset),
            n_admitted_parent_subsets=length(cands),
            n_admitted_unique_closures=length(unique([x.closure_key for x in cands])),
            n_admitted_unique_profiles=length(unique([x.profile_key for x in cands])),
            mu_v4=local_mu_v4_from_profile(c.N),
        ))
    end
    return rows
end

per_vertex_path = joinpath(outdir, "measure_comparison_per_vertex.csv")
open(per_vertex_path, "w") do io
    println(io, "measure,seed,run_seed,step_idx,v,N1,N2,N3,N4,V4,S,parent_size,orig_parent_size,frontier_parent_size,n_admitted_parent_subsets,n_admitted_unique_closures,n_admitted_unique_profiles,mu_v4")
    for measure in measures
        @printf("Running measure: %s\n", measure)
        for seed_name in sort(collect(keys(seed_builders)))
            seed_builder = seed_builders[seed_name]
            for run_seed in 1:n_seeds
                rows = run_one(seed_builder, run_seed, measure)
                for r in rows
                    @printf(io, "%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.10f\n",
                        measure, seed_name, run_seed, r.step_idx, r.v,
                        r.N1, r.N2, r.N3, r.N4, r.V4, r.S,
                        r.parent_size, r.orig_parent_size, r.frontier_parent_size,
                        r.n_admitted_parent_subsets, r.n_admitted_unique_closures,
                        r.n_admitted_unique_profiles, r.mu_v4)
                end
            end
            @printf("  seed %s complete\n", seed_name)
        end
    end
end

# Summarize using Julia after writing CSV via simple in-memory re-run-free parse.
# Keep this simple to avoid DataFrames dependency.
function parse_csv(path)
    lines = readlines(path)
    header = split(lines[1], ",")
    rows = Vector{Dict{String,String}}()
    for ln in lines[2:end]
        vals = split(ln, ",")
        push!(rows, Dict(header[i] => vals[i] for i in eachindex(header)))
    end
    return rows
end

rows = parse_csv(per_vertex_path)
summary_path = joinpath(outdir, "measure_comparison_summary.csv")
open(summary_path, "w") do io
    println(io, "measure,seed,n,mean_N1,mean_N2,mean_N3,mean_N4,mean_V4,mean_S,mean_parent_size,mean_orig_parent_size,mean_frontier_parent_size,mean_mu_v4")
    for measure in measures
        for seed_name in sort(collect(keys(seed_builders)))
            rs = [r for r in rows if r["measure"] == measure && r["seed"] == seed_name]
            n = length(rs)
            function mean_col(col)
                return mean(parse(Float64, r[col]) for r in rs)
            end
            @printf(io, "%s,%s,%d,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f\n",
                measure, seed_name, n,
                mean_col("N1"), mean_col("N2"), mean_col("N3"), mean_col("N4"),
                mean_col("V4"), mean_col("S"), mean_col("parent_size"),
                mean_col("orig_parent_size"), mean_col("frontier_parent_size"),
                mean_col("mu_v4"))
        end
    end
end

profile_path = joinpath(outdir, "measure_comparison_profile_frequency.csv")
open(profile_path, "w") do io
    println(io, "measure,seed,profile,count,pct")
    for measure in measures
        for seed_name in sort(collect(keys(seed_builders)))
            rs = [r for r in rows if r["measure"] == measure && r["seed"] == seed_name]
            counts = Dict{String,Int}()
            for r in rs
                pk = string(r["N1"], "|", r["N2"], "|", r["N3"], "|", r["N4"])
                counts[pk] = get(counts, pk, 0) + 1
            end
            total = length(rs)
            for (pk,c) in sort(collect(counts), by=x -> -x[2])
                @printf(io, "%s,%s,%s,%d,%.10f\n", measure, seed_name, pk, c, 100*c/total)
            end
        end
    end
end

println("Wrote outputs to: ", outdir)
