#!/usr/bin/env julia
# Candidate-measure diagnostics for RAGrowSim.
#
# Usage from RAGrowSim root:
#   julia --project=. scripts/run_candidate_measure_diagnostics.jl [target_extra_n] [n_seeds] [outdir] [max_parent_size]
#
# This script asks whether uniform sampling over parent subsets is strongly
# different from sampling over unique causal closures or unique BDG profiles.

using Printf
using Statistics
using Random

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

target_extra_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 25
n_seeds        = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 20
outdir         = length(ARGS) >= 3 ? ARGS[3] : "outputs/candidate_measure"
max_parent_size = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 4
mkpath(outdir)

seeds = [
    ("chain2",      () -> seed_chain(2)),
    ("chain4",      () -> seed_chain(4)),
    ("sym_branch",  () -> seed_sym_branch()),
    ("asym_branch", () -> seed_asym_branch()),
]

cfg = GrowthConfig(ledger_rule=Neutral(), max_parent_size=max_parent_size)

function closure_key(d::DAG, pset)
    anc = RAGrowSim.BDGGrow.proposed_ancestors(d, pset)
    return join(sort(collect(anc)), ";")
end

profile_key(N::NTuple{4,Int}) = @sprintf("%d|%d|%d|%d", N[1], N[2], N[3], N[4])

function candidate_space_summary(d::DAG, cfg::GrowthConfig)
    psets = RAGrowSim.Dynamics.enumerate_parent_sets(d, cfg.max_parent_size)
    total = length(psets)
    admitted = 0
    closure_counts = Dict{String,Int}()
    closure_adm_counts = Dict{String,Int}()
    profile_counts = Dict{String,Int}()
    profile_adm_counts = Dict{String,Int}()
    profile_unique_closures = Dict{String,Set{String}}()
    profile_unique_adm_closures = Dict{String,Set{String}}()

    for pset in psets
        ck = closure_key(d, pset)
        closure_counts[ck] = get(closure_counts, ck, 0) + 1
        N = profile(d, pset)
        pk = profile_key(N)
        profile_counts[pk] = get(profile_counts, pk, 0) + 1
        if !haskey(profile_unique_closures, pk)
            profile_unique_closures[pk] = Set{String}()
        end
        push!(profile_unique_closures[pk], ck)
        if bdgscore(N) > 0
            admitted += 1
            closure_adm_counts[ck] = get(closure_adm_counts, ck, 0) + 1
            profile_adm_counts[pk] = get(profile_adm_counts, pk, 0) + 1
            if !haskey(profile_unique_adm_closures, pk)
                profile_unique_adm_closures[pk] = Set{String}()
            end
            push!(profile_unique_adm_closures[pk], ck)
        end
    end

    mults = collect(values(closure_counts))
    adm_mults = collect(values(closure_adm_counts))
    return (
        total_parent_subsets=total,
        admitted_parent_subsets=admitted,
        unique_closures=length(closure_counts),
        admitted_unique_closures=length(closure_adm_counts),
        unique_profiles=length(profile_counts),
        admitted_unique_profiles=length(profile_adm_counts),
        mean_closure_multiplicity=mean(mults),
        max_closure_multiplicity=maximum(mults),
        mean_adm_closure_multiplicity=isempty(adm_mults) ? 0.0 : mean(adm_mults),
        max_adm_closure_multiplicity=isempty(adm_mults) ? 0 : maximum(adm_mults),
        profile_counts=profile_counts,
        profile_adm_counts=profile_adm_counts,
        profile_unique_closures=profile_unique_closures,
        profile_unique_adm_closures=profile_unique_adm_closures
    )
end

step_rows = NamedTuple[]
profile_totals = Dict{Tuple{String,String}, NamedTuple}()

println("RAGrowSim candidate-measure diagnostic")
println("=" ^ 72)
@printf("target_extra_n=%d, n_seeds=%d, max_parent_size=%d\n", target_extra_n, n_seeds, max_parent_size)

for (seed_name, make_seed) in seeds
    for run_seed in 1:n_seeds
        rng = MersenneTwister(run_seed)
        d = make_seed()
        for step_idx in 1:target_extra_n
            summ = candidate_space_summary(d, cfg)
            push!(step_rows, (
                seed=seed_name, run_seed=run_seed, step_idx=step_idx, n_vertices=d.n,
                total_parent_subsets=summ.total_parent_subsets,
                admitted_parent_subsets=summ.admitted_parent_subsets,
                unique_closures=summ.unique_closures,
                admitted_unique_closures=summ.admitted_unique_closures,
                unique_profiles=summ.unique_profiles,
                admitted_unique_profiles=summ.admitted_unique_profiles,
                mean_closure_multiplicity=summ.mean_closure_multiplicity,
                max_closure_multiplicity=summ.max_closure_multiplicity,
                mean_adm_closure_multiplicity=summ.mean_adm_closure_multiplicity,
                max_adm_closure_multiplicity=summ.max_adm_closure_multiplicity
            ))
            # accumulate profile-level candidate mass
            for (pk, c) in summ.profile_counts
                key = (seed_name, pk)
                old = get(profile_totals, key, (candidate_count=0, admitted_candidate_count=0, unique_closure_count=0, admitted_unique_closure_count=0))
                adm = get(summ.profile_adm_counts, pk, 0)
                ucl = length(get(summ.profile_unique_closures, pk, Set{String}()))
                uadm = length(get(summ.profile_unique_adm_closures, pk, Set{String}()))
                profile_totals[key] = (
                    candidate_count=old.candidate_count + c,
                    admitted_candidate_count=old.admitted_candidate_count + adm,
                    unique_closure_count=old.unique_closure_count + ucl,
                    admitted_unique_closure_count=old.admitted_unique_closure_count + uadm
                )
            end
            # now actually grow one step
            grow!(d, rng, cfg)
        end
    end
end

open(joinpath(outdir, "candidate_measure_step_summary.csv"), "w") do io
    println(io, "seed,run_seed,step_idx,n_vertices,total_parent_subsets,admitted_parent_subsets,unique_closures,admitted_unique_closures,unique_profiles,admitted_unique_profiles,mean_closure_multiplicity,max_closure_multiplicity,mean_adm_closure_multiplicity,max_adm_closure_multiplicity")
    for r in step_rows
        @printf(io, "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.10f,%d,%.10f,%d\n",
            r.seed, r.run_seed, r.step_idx, r.n_vertices,
            r.total_parent_subsets, r.admitted_parent_subsets,
            r.unique_closures, r.admitted_unique_closures,
            r.unique_profiles, r.admitted_unique_profiles,
            r.mean_closure_multiplicity, r.max_closure_multiplicity,
            r.mean_adm_closure_multiplicity, r.max_adm_closure_multiplicity)
    end
end

open(joinpath(outdir, "candidate_measure_profile_summary.csv"), "w") do io
    println(io, "seed,profile,candidate_count,admitted_candidate_count,unique_closure_count,admitted_unique_closure_count")
    for ((seed_name, pk), v) in sort(collect(profile_totals), by=x -> (x[1][1], x[1][2]))
        @printf(io, "%s,%s,%d,%d,%d,%d\n", seed_name, pk, v.candidate_count, v.admitted_candidate_count, v.unique_closure_count, v.admitted_unique_closure_count)
    end
end

println("Wrote outputs to: $outdir")
