#!/usr/bin/env julia
# scripts/run_small.jl
#
# Run multiple independent growth simulations to a small target n,
# accumulate observables, print a summary.
#
# Usage:  julia --project=. scripts/run_small.jl [target_n] [n_seeds]
#
# Defaults: target_n = 20, n_seeds = 50.

using Printf
using Statistics

# Make the package available (load by direct include)
include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

# ----- parse arguments
target_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 20
n_seeds  = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 50

println("BDG growth simulator — small run")
println("=" ^ 64)
@printf("target_n = %d, n_seeds = %d\n\n", target_n, n_seeds)

# ----- run all seeds
histories = GrowthHistory[]
t0 = time()
for seed in 1:n_seeds
    _, h = run_growth(target_n, seed)
    push!(histories, h)
end
elapsed = time() - t0
@printf("Completed %d runs in %.2f s (%.3f s/run, %.3f ms/vertex)\n\n",
        n_seeds, elapsed, elapsed / n_seeds, 1000 * elapsed / (n_seeds * target_n))

# ----- per-step running means: average over seeds at each step
println("Running profile means (averaged across seeds at each step n):")
println("-" ^ 64)
@printf("%5s  %10s  %10s  %10s  %10s\n",
        "n", "<N_1>", "<N_2>", "<N_3>", "<N_4>")
all_means = [running_profile_means(h) for h in histories]
for n in 1:target_n
    n1 = mean([all_means[s][n][1] for s in 1:n_seeds])
    n2 = mean([all_means[s][n][2] for s in 1:n_seeds])
    n3 = mean([all_means[s][n][3] for s in 1:n_seeds])
    n4 = mean([all_means[s][n][4] for s in 1:n_seeds])
    @printf("%5d  %10.4f  %10.4f  %10.4f  %10.4f\n", n, n1, n2, n3, n4)
end
println()
println("Reference Poisson(μ=1) means: (1.0000, 0.5000, 0.1667, 0.0417)")
println()

# ----- acceptance ratios
println("Acceptance ratio P_acc(n) = n_admitted / n_candidates per step:")
println("-" ^ 64)
@printf("%5s  %10s  %10s  %10s\n", "n", "min", "mean", "max")
all_ratios = [acceptance_ratios(h) for h in histories]
for n in 1:target_n
    vs = [all_ratios[s][n] for s in 1:n_seeds]
    @printf("%5d  %10.4f  %10.4f  %10.4f\n", n, minimum(vs), mean(vs), maximum(vs))
end
println()

# ----- per-vertex profile distribution (across all steps, all seeds)
println("Top 12 (N_1, N_2, N_3, N_4) profiles selected (across all steps × seeds):")
println("-" ^ 64)
prof_counts = Dict{NTuple{4,Int},Int}()
for h in histories, step in h.steps
    prof_counts[step.N] = get(prof_counts, step.N, 0) + 1
end
sorted = sort(collect(prof_counts), by = kv -> -kv[2])
n_total = sum(v for (_, v) in prof_counts)
@printf("%6s  %22s  %8s  %8s\n", "rank", "(N_1,N_2,N_3,N_4)", "S", "count (%)")
for (i, (N, c)) in enumerate(sorted[1:min(12, end)])
    S = bdgscore(N)
    @printf("%6d  %22s  %8d  %5d (%5.1f%%)\n",
            i, string(N), S, c, 100*c/n_total)
end
println()

# ----- parent-set size distribution
println("Parent-set size distribution (= |selected antichain|):")
println("-" ^ 64)
pcounts = parent_count_distribution(histories)
total = sum(values(pcounts))
@printf("%5s  %10s  %10s\n", "size", "count", "fraction")
for k in sort(collect(keys(pcounts)))
    @printf("%5d  %10d  %10.4f\n", k, pcounts[k], pcounts[k]/total)
end
println()

# ----- antichain width (final DAG only, expensive)
if target_n <= 18
    println("Maximum antichain width over time (averaged across seeds):")
    println("-" ^ 64)
    @printf("%5s  %15s\n", "n", "<max width>")
    all_widths = [max_antichain_widths(h) for h in histories]
    for n in 1:target_n
        w = mean([all_widths[s][n] for s in 1:n_seeds])
        @printf("%5d  %15.3f\n", n, w)
    end
else
    println("Antichain width tracking skipped (target_n > 18).")
end

println()
println("Done.")
