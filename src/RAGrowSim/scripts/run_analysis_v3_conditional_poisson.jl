#!/usr/bin/env julia
# Multi-seed BDG growth analysis with accepted-conditional Poisson baselines.
#
# Usage from RAGrowSim root:
#   julia --project=. scripts/run_analysis_v3_conditional_poisson.jl [target_extra_n] [n_seeds] [outdir]
#
# This version fixes the most important comparison issue:
# realized simulator vertices have passed S>0, so the corresponding
# Poisson-CSG baseline is E[N_k | S>0, μ], not raw E[N_k]=μ^k/k!.

using Printf
using Statistics

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

target_extra_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 25
n_seeds        = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 50
outdir         = length(ARGS) >= 3 ? ARGS[3] : "outputs/conditional_poisson"
mkpath(outdir)

seeds = [
    ("chain2",      () -> seed_chain(2)),
    ("chain4",      () -> seed_chain(4)),
    ("sym_branch",  () -> seed_sym_branch()),
    ("asym_branch", () -> seed_asym_branch()),
]

cfg = GrowthConfig(ledger_rule=Neutral(), max_parent_size=4)

fact(k::Int) = k <= 1 ? 1.0 : prod(1.0:k)
poisson_means(mu::Float64) = (mu, mu^2/2, mu^3/6, mu^4/24)

function poisson_pmf(n::Int, lambda::Float64)
    if lambda == 0
        return n == 0 ? 1.0 : 0.0
    end
    return exp(-lambda + n * log(lambda) - loggamma(n + 1))
end

function trunc_max(lambda::Float64)
    # Conservative for μ up to ~4. Good enough for diagnostic use.
    return max(12, Int(ceil(lambda + 10 * sqrt(max(lambda, 1e-9)) + 10)))
end

function conditional_poisson_stats(mu::Float64)
    lambdas = poisson_means(mu)
    maxs = ntuple(i -> trunc_max(lambdas[i]), 4)
    total_mass = 0.0
    acc_mass = 0.0
    sN = [0.0, 0.0, 0.0, 0.0]
    sS = 0.0
    for n1 in 0:maxs[1]
        p1 = poisson_pmf(n1, lambdas[1])
        for n2 in 0:maxs[2]
            p12 = p1 * poisson_pmf(n2, lambdas[2])
            for n3 in 0:maxs[3]
                p123 = p12 * poisson_pmf(n3, lambdas[3])
                for n4 in 0:maxs[4]
                    p = p123 * poisson_pmf(n4, lambdas[4])
                    total_mass += p
                    N = (n1,n2,n3,n4)
                    S = bdgscore(N)
                    if S > 0
                        acc_mass += p
                        sN[1] += p*n1; sN[2] += p*n2; sN[3] += p*n3; sN[4] += p*n4
                        sS += p*S
                    end
                end
            end
        end
    end
    if acc_mass == 0
        return (p_acc=0.0, included_mass=total_mass, mean_N=(NaN,NaN,NaN,NaN), mean_S=NaN)
    end
    return (
        p_acc = acc_mass / total_mass,
        included_mass = total_mass,
        mean_N = (sN[1]/acc_mass, sN[2]/acc_mass, sN[3]/acc_mass, sN[4]/acc_mass),
        mean_S = sS/acc_mass
    )
end

function trunc_volume(mu::Float64; K::Int=4)
    s = 0.0
    for k in 1:K
        s += mu^k / fact(k)
    end
    return s
end

function invert_trunc_volume(V::Float64; K::Int=4)
    V <= 0 && return 0.0
    lo = 0.0; hi = max(1.0, V)
    while trunc_volume(hi; K=K) < V
        hi *= 2
    end
    for _ in 1:80
        mid = (lo+hi)/2
        if trunc_volume(mid; K=K) < V
            lo = mid
        else
            hi = mid
        end
    end
    return (lo+hi)/2
end

records = NamedTuple[]
println("BDG growth simulator — accepted-conditional Poisson comparison")
println("=" ^ 78)

for (seed_name, make_seed) in seeds
    for run_seed in 1:n_seeds
        d0 = make_seed()
        d_after, h = run_growth(d0, target_extra_n, run_seed; config=cfg)
        for (step_idx, step) in enumerate(h.steps)
            N = step.N
            V4 = sum(N)
            push!(records, (
                seed=seed_name, run_seed=run_seed, step_idx=step_idx, v=step.v,
                N1=N[1], N2=N[2], N3=N[3], N4=N[4], V4=V4,
                S=step.S, parent_size=length(step.parent_set),
                mu_depth=local_mu(d_after, step.v),
                mu_v4=invert_trunc_volume(float(V4))
            ))
        end
    end
    @printf("Seed %-12s complete\n", seed_name)
end

open(joinpath(outdir, "per_vertex_records_conditional.csv"), "w") do io
    println(io, "seed,run_seed,step_idx,v,N1,N2,N3,N4,V4,S,parent_size,mu_depth,mu_v4")
    for r in records
        @printf(io, "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.10f,%.10f\n",
            r.seed, r.run_seed, r.step_idx, r.v, r.N1, r.N2, r.N3, r.N4,
            r.V4, r.S, r.parent_size, r.mu_depth, r.mu_v4)
    end
end

function summarize(records, field::Symbol, outpath::String; n_bins::Int=10)
    vals = [getfield(r, field) for r in records]
    lo = minimum(vals); hi = maximum(vals)
    hi == lo && (hi += 1.0)
    edges = collect(range(lo, hi; length=n_bins+1))
    open(outpath, "w") do io
        println(io, "estimator,bin_lo,bin_hi,n,mean_mu,sim_N1,sim_N2,sim_N3,sim_N4,sim_S,raw_N1,raw_N2,raw_N3,raw_N4,raw_S,cond_Pacc,cond_N1,cond_N2,cond_N3,cond_N4,cond_S,cond_included_mass")
        for b in 1:n_bins
            blo = edges[b]; bhi = edges[b+1]
            bin = [r for r in records if (getfield(r, field) >= blo && getfield(r, field) < bhi) || (b==n_bins && getfield(r, field)==bhi)]
            isempty(bin) && continue
            mean_mu = mean([getfield(r, field) for r in bin])
            simN = (mean([r.N1 for r in bin]), mean([r.N2 for r in bin]), mean([r.N3 for r in bin]), mean([r.N4 for r in bin]))
            simS = mean([r.S for r in bin])
            rawN = poisson_means(mean_mu)
            rawS = bdgscore((0,0,0,0)) - rawN[1] + 9*rawN[2] - 16*rawN[3] + 8*rawN[4]
            cond = conditional_poisson_stats(mean_mu)
            cN = cond.mean_N
            @printf(io, "%s,%.10f,%.10f,%d,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f\n",
                String(field), blo, bhi, length(bin), mean_mu,
                simN[1], simN[2], simN[3], simN[4], simS,
                rawN[1], rawN[2], rawN[3], rawN[4], rawS,
                cond.p_acc, cN[1], cN[2], cN[3], cN[4], cond.mean_S, cond.included_mass)
        end
    end
end

summarize(records, :mu_depth, joinpath(outdir, "conditional_summary_mu_depth.csv"))
summarize(records, :mu_v4, joinpath(outdir, "conditional_summary_mu_v4.csv"))

println("Wrote outputs to: $outdir")
