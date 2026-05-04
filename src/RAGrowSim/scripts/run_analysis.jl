#!/usr/bin/env julia
# scripts/run_analysis.jl
#
# Multi-seed comparison + μ-conditional BDG profile statistics.
#
# Two questions:
#   (1) Does the growing-DAG dynamics converge to seed-independent
#       <N_k> values? If yes, there is a stationary distribution.
#   (2) Does <N_k> conditioned on local_mu match Poisson(μ): N_k = μ^k/k!?
#       If yes, the closed-form Poisson predictions in the suite are valid
#       coarse-grainings. If no, the suite predictions need re-examination.
#
# Default settings target chain-4 base + ~25 extra vertices, 50 seeds.
# Adjust via command-line args if needed.
#
# Usage:
#   julia --project=. scripts/run_analysis.jl [target_extra_n] [n_seeds]

using Printf
using Statistics

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

target_extra_n = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 25
n_seeds = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 50

println("BDG growth simulator — multi-seed and μ-conditional analysis")
println("=" ^ 70)
@printf("target_extra_n = %d, n_seeds = %d\n", target_extra_n, n_seeds)
@printf("ledger rule: Neutral (BDG dynamics only; no charge bias)\n\n")

# ─────────────────────────────────────────────────────────────────────
# Seed bank
# ─────────────────────────────────────────────────────────────────────

seeds = [
    ("chain2",      () -> seed_chain(2),       2),
    ("chain4",      () -> seed_chain(4),       4),
    ("sym_branch",  () -> seed_sym_branch(),   4),
    ("asym_branch", () -> seed_asym_branch(),  4),
]

cfg = GrowthConfig(ledger_rule=Neutral(), max_parent_size=4)

# ─────────────────────────────────────────────────────────────────────
# Run 1: multi-seed comparison
# ─────────────────────────────────────────────────────────────────────

println("─" ^ 70)
println("PART 1 — Multi-seed comparison: do <N_k> values agree across seeds?")
println("─" ^ 70)
println()

# Each entry: (seed_name, vertex_records)
# Each vertex_record: (vertex_index, local_mu, N_tuple, S, parent_set_size)
all_seed_data = Dict{String, Vector{Tuple{Int,Float64,NTuple{4,Int},Int,Int}}}()

for (name, make_seed, seed_size) in seeds
    records = Tuple{Int,Float64,NTuple{4,Int},Int,Int}[]
    t0 = time()
    for s in 1:n_seeds
        seed_dag = make_seed()
        d_after, h = run_growth(seed_dag, target_extra_n, s; config=cfg)
        # For each new vertex (in step order), record (vertex_index, local_mu, N, S, parent_size).
        # local_mu(d_after, v) gives the right answer because ancestors are
        # immutable once v is added (adding later vertices doesn't change v's
        # ancestor set).
        for step in h.steps
            v = step.v
            mu = local_mu(d_after, v)
            push!(records, (v, mu, step.N, step.S, length(step.parent_set)))
        end
    end
    elapsed = time() - t0
    @printf("Seed %-12s: %d records in %.2f s\n", name, length(records), elapsed)
    all_seed_data[name] = records
end
println()

# Per-seed averages of N_k
@printf("%-15s  %8s  %8s  %8s  %8s  %8s  %8s\n",
        "seed", "<N_1>", "<N_2>", "<N_3>", "<N_4>", "<S>", "<pset|>")
println("-" ^ 80)
for (name, _, _) in seeds
    records = all_seed_data[name]
    ns = [r[3] for r in records]
    Ss = [r[4] for r in records]
    psizes = [r[5] for r in records]
    n1 = mean([n[1] for n in ns])
    n2 = mean([n[2] for n in ns])
    n3 = mean([n[3] for n in ns])
    n4 = mean([n[4] for n in ns])
    s_mean = mean(Ss)
    pmean = mean(psizes)
    @printf("%-15s  %8.4f  %8.4f  %8.4f  %8.4f  %8.2f  %8.2f\n",
            name, n1, n2, n3, n4, s_mean, pmean)
end
println()
@printf("Reference Poisson(μ=1): <N_k> = (%.4f, %.4f, %.4f, %.4f)\n",
        1.0, 0.5, 1/6, 1/24)
println()

# Are the seed-conditional means similar?
# Compute the spread across seeds for each N_k component.
println("Spread across seeds (max - min, per N_k component):")
for k in 1:4
    vals = Float64[]
    for (name, _, _) in seeds
        records = all_seed_data[name]
        push!(vals, mean([r[3][k] for r in records]))
    end
    @printf("  N_%d: spread = %.4f  (min=%.4f, max=%.4f)\n",
            k, maximum(vals) - minimum(vals), minimum(vals), maximum(vals))
end
println()

# ─────────────────────────────────────────────────────────────────────
# Run 2: μ-conditional statistics
# ─────────────────────────────────────────────────────────────────────

println("─" ^ 70)
println("PART 2 — μ-conditional <N_k>: does it match Poisson(μ) = μ^k/k! ?")
println("─" ^ 70)
println()
println("local_mu := |ancestors(v)| / max(1, longest_chain_to(v))")
println("(heuristic; not the formal Poisson sprinkling rate)")
println()

# Pool records from all seeds
all_records = Tuple{Int,Float64,NTuple{4,Int},Int,Int}[]
for (name, _, _) in seeds
    append!(all_records, all_seed_data[name])
end
@printf("Total records pooled across seeds: %d\n\n", length(all_records))

# Bin by local_mu. Choose bins that span the observed range.
mus = [r[2] for r in all_records]
mu_min = minimum(mus)
mu_max = maximum(mus)
@printf("Observed local_mu range: [%.3f, %.3f]\n\n", mu_min, mu_max)

# Use 8 bins evenly across the range
n_bins = 8
bin_edges = range(mu_min, mu_max; length=n_bins+1)

@printf("%-18s  %8s  %8s  %8s  %8s  %8s  %12s\n",
        "mu range", "n_in_bin", "<N_1>", "<N_2>", "<N_3>", "<N_4>", "Poisson <N>")
println("-" ^ 90)

for b in 1:n_bins
    lo = bin_edges[b]
    hi = bin_edges[b+1]
    in_bin = filter(r -> lo <= r[2] < hi || (b == n_bins && r[2] == hi), all_records)
    if isempty(in_bin); continue; end
    mu_center = (lo + hi) / 2
    Ns = [r[3] for r in in_bin]
    n1 = mean([n[1] for n in Ns])
    n2 = mean([n[2] for n in Ns])
    n3 = mean([n[3] for n in Ns])
    n4 = mean([n[4] for n in Ns])
    # Poisson prediction at the bin center
    p1 = mu_center
    p2 = mu_center^2 / 2
    p3 = mu_center^3 / 6
    p4 = mu_center^4 / 24
    @printf("[%.3f, %.3f)  %8d  %8.3f  %8.3f  %8.3f  %8.3f  P(%.2f)=(%.2f,%.2f,%.2f,%.2f)\n",
            lo, hi, length(in_bin), n1, n2, n3, n4,
            mu_center, p1, p2, p3, p4)
end
println()

# ─────────────────────────────────────────────────────────────────────
# Run 3: focused comparison at specific mu values
# ─────────────────────────────────────────────────────────────────────

println("─" ^ 70)
println("PART 3 — Focused comparison at specific μ values")
println("─" ^ 70)
println()
println("For each target μ, find records with local_mu within ±0.1 and report.")
println()

for mu_target in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    in_window = filter(r -> abs(r[2] - mu_target) < 0.1, all_records)
    if isempty(in_window)
        @printf("μ ≈ %.2f: no records in window\n", mu_target)
        continue
    end
    Ns = [r[3] for r in in_window]
    n1 = mean([n[1] for n in Ns])
    n2 = mean([n[2] for n in Ns])
    n3 = mean([n[3] for n in Ns])
    n4 = mean([n[4] for n in Ns])
    p1 = mu_target
    p2 = mu_target^2 / 2
    p3 = mu_target^3 / 6
    p4 = mu_target^4 / 24
    @printf("μ ≈ %.2f (n=%d):\n", mu_target, length(in_window))
    @printf("  sim:     (%6.3f, %6.3f, %6.3f, %6.3f)\n", n1, n2, n3, n4)
    @printf("  Poisson: (%6.3f, %6.3f, %6.3f, %6.3f)\n", p1, p2, p3, p4)
    @printf("  ratio:   (%6.3f, %6.3f, %6.3f, %6.3f)\n",
            n1/p1, n2/p2, n3/p3, n4/p4)
    println()
end

println("Done.")
