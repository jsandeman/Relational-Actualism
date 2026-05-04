#!/usr/bin/env julia
# Multi-seed BDG growth analysis with multiple local-μ estimators.
#
# Usage from RAGrowSim root:
#   julia --project=. scripts/run_analysis_v2_mu_estimators.jl [target_extra_n] [n_seeds] [outdir]
#
# This script is intentionally conservative. It distinguishes:
#   mu_depth  = existing heuristic |ancestors| / longest_chain
#   mu_v4     = μ fitted to V4=N1+N2+N3+N4 under truncated Poisson volume
#   mu_mle    = one-parameter Poisson profile MLE fitted to (N1..N4)
#
# mu_v4 and mu_mle are fitted from the profile itself. Use them to study
# profile-composition residuals, not as independent density measurements.

using Printf
using Statistics

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

target_extra_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 25
n_seeds        = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 50
outdir         = length(ARGS) >= 3 ? ARGS[3] : "outputs/mu_estimators"
mkpath(outdir)

seeds = [
    ("chain2",      () -> seed_chain(2)),
    ("chain4",      () -> seed_chain(4)),
    ("sym_branch",  () -> seed_sym_branch()),
    ("asym_branch", () -> seed_asym_branch()),
]

cfg = GrowthConfig(ledger_rule=Neutral(), max_parent_size=4)

fact(k::Int) = k <= 1 ? 1.0 : prod(1.0:k)

function trunc_volume(mu::Float64; K::Int=4)
    s = 0.0
    for k in 1:K
        s += mu^k / fact(k)
    end
    return s
end

function invert_trunc_volume(V::Float64; K::Int=4)
    if V <= 0
        return 0.0
    end
    lo = 0.0
    hi = max(1.0, V)
    while trunc_volume(hi; K=K) < V
        hi *= 2
        hi > 1e6 && error("failed to bracket μ for V=$V")
    end
    for _ in 1:80
        mid = (lo + hi) / 2
        if trunc_volume(mid; K=K) < V
            lo = mid
        else
            hi = mid
        end
    end
    return (lo + hi) / 2
end

# MLE for independent Poisson profile with λ_k = μ^k/k!, k=1..4.
# Solves: sum_k k*N_k / μ = sum_k μ^(k-1)/(k-1)!.
function mu_mle_profile(N::NTuple{4,Int})
    A = 0.0
    for k in 1:4
        A += k * N[k]
    end
    if A == 0
        return 0.0
    end
    f(mu) = A / mu - sum(mu^(k-1) / fact(k-1) for k in 1:4)
    lo = 1e-9
    hi = max(1.0, sum(N) + 1.0)
    while f(hi) > 0
        hi *= 2
        hi > 1e6 && error("failed to bracket MLE μ for N=$N")
    end
    for _ in 1:100
        mid = (lo + hi) / 2
        if f(mid) > 0
            lo = mid
        else
            hi = mid
        end
    end
    return (lo + hi) / 2
end

poisson_means(mu::Float64) = (mu, mu^2/2, mu^3/6, mu^4/24)

records = NamedTuple[]

println("BDG growth simulator — μ-estimator comparison")
println("=" ^ 72)
@printf("target_extra_n=%d, n_seeds=%d, ledger=Neutral, max_parent_size=4\n", target_extra_n, n_seeds)

for (seed_name, make_seed) in seeds
    t0 = time()
    for run_seed in 1:n_seeds
        d0 = make_seed()
        d_after, h = run_growth(d0, target_extra_n, run_seed; config=cfg)
        for (step_idx, step) in enumerate(h.steps)
            N = step.N
            V4 = sum(N)
            mu_depth = local_mu(d_after, step.v)
            mu_v4 = invert_trunc_volume(float(V4))
            mu_mle = mu_mle_profile(N)
            push!(records, (
                seed=seed_name, run_seed=run_seed, step_idx=step_idx,
                v=step.v, N1=N[1], N2=N[2], N3=N[3], N4=N[4], V4=V4,
                S=step.S, parent_size=length(step.parent_set),
                mu_depth=mu_depth, mu_v4=mu_v4, mu_mle=mu_mle
            ))
        end
    end
    @printf("Seed %-12s done in %.2f s\n", seed_name, time() - t0)
end

# Write per-vertex records
open(joinpath(outdir, "per_vertex_records_v2.csv"), "w") do io
    println(io, "seed,run_seed,step_idx,v,N1,N2,N3,N4,V4,S,parent_size,mu_depth,mu_v4,mu_mle")
    for r in records
        @printf(io, "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.10f,%.10f,%.10f\n",
            r.seed, r.run_seed, r.step_idx, r.v, r.N1, r.N2, r.N3, r.N4,
            r.V4, r.S, r.parent_size, r.mu_depth, r.mu_v4, r.mu_mle)
    end
end

function summarize_by_bins(records, field::Symbol, outpath::String; n_bins::Int=12)
    vals = [getfield(r, field) for r in records]
    lo = minimum(vals); hi = maximum(vals)
    if hi == lo
        hi = lo + 1
    end
    edges = collect(range(lo, hi; length=n_bins+1))
    open(outpath, "w") do io
        println(io, "estimator,bin_lo,bin_hi,n,mean_mu,mean_N1,mean_N2,mean_N3,mean_N4,mean_S,pois_N1,pois_N2,pois_N3,pois_N4,resid_N1,resid_N2,resid_N3,resid_N4")
        for b in 1:n_bins
            blo = edges[b]; bhi = edges[b+1]
            bin = [r for r in records if (getfield(r, field) >= blo && getfield(r, field) < bhi) || (b == n_bins && getfield(r, field) == bhi)]
            isempty(bin) && continue
            mean_mu = mean([getfield(r, field) for r in bin])
            mn = (mean([r.N1 for r in bin]), mean([r.N2 for r in bin]), mean([r.N3 for r in bin]), mean([r.N4 for r in bin]))
            mS = mean([r.S for r in bin])
            pm = poisson_means(mean_mu)
            resid = (mn[1]-pm[1], mn[2]-pm[2], mn[3]-pm[3], mn[4]-pm[4])
            @printf(io, "%s,%.10f,%.10f,%d,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f\n",
                String(field), blo, bhi, length(bin), mean_mu, mn[1], mn[2], mn[3], mn[4], mS,
                pm[1], pm[2], pm[3], pm[4], resid[1], resid[2], resid[3], resid[4])
        end
    end
end

summarize_by_bins(records, :mu_depth, joinpath(outdir, "bin_summary_mu_depth.csv"))
summarize_by_bins(records, :mu_v4,    joinpath(outdir, "bin_summary_mu_v4.csv"))
summarize_by_bins(records, :mu_mle,   joinpath(outdir, "bin_summary_mu_mle.csv"))

# Seed summary
open(joinpath(outdir, "seed_summary_v2.csv"), "w") do io
    println(io, "seed,n,mean_N1,mean_N2,mean_N3,mean_N4,mean_V4,mean_S,mean_parent_size,mean_mu_depth,mean_mu_v4,mean_mu_mle")
    for (seed_name, _) in seeds
        bin = [r for r in records if r.seed == seed_name]
        @printf(io, "%s,%d,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f,%.10f\n",
            seed_name, length(bin), mean([r.N1 for r in bin]), mean([r.N2 for r in bin]),
            mean([r.N3 for r in bin]), mean([r.N4 for r in bin]), mean([r.V4 for r in bin]),
            mean([r.S for r in bin]), mean([r.parent_size for r in bin]),
            mean([r.mu_depth for r in bin]), mean([r.mu_v4 for r in bin]), mean([r.mu_mle for r in bin]))
    end
end

println("Wrote outputs to: $outdir")
