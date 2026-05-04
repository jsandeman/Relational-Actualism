#!/usr/bin/env julia
# scripts/run_seeded.jl
#
# Run growth simulations from a seeded (non-empty) DAG, comparing
# ledger rules. This is the script that exercises the post-Apr-28
# architecture — saturated initial conditions per RA's nucleation-at-
# saturation principle, and pluggable ledger rules per RA-OPEN-CHARGE-SIGN-001.
#
# Usage:
#   julia --project=. scripts/run_seeded.jl [seed_kind] [target_extra_n] [n_seeds]
#
# seed_kind: one of "chain4", "sym_branch", "asym_branch", "chain2"
# target_extra_n: how many vertices to grow beyond the seed
# n_seeds: number of independent runs

using Printf
using Statistics

include(joinpath(@__DIR__, "..", "src", "RAGrowSim.jl"))
using .RAGrowSim

# Parse arguments
seed_kind = length(ARGS) >= 1 ? ARGS[1] : "chain4"
target_extra_n = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 12
n_seeds = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 30

# Construct the seed
make_seed = if seed_kind == "chain4"
    () -> seed_chain(4)
elseif seed_kind == "chain2"
    () -> seed_chain(2)
elseif seed_kind == "sym_branch"
    () -> seed_sym_branch()
elseif seed_kind == "asym_branch"
    () -> seed_asym_branch()
else
    error("unknown seed_kind: $seed_kind. Try chain4, chain2, sym_branch, asym_branch.")
end

println("BDG growth simulator — seeded run")
println("=" ^ 70)
@printf("seed_kind = %s, target_extra_n = %d, n_seeds = %d\n\n",
        seed_kind, target_extra_n, n_seeds)

# Show the seed DAG
seed_demo = make_seed()
@printf("Seed DAG: %d vertices\n", seed_demo.n)
for v in 1:seed_demo.n
    parents = collect(seed_demo.parents[v])
    @printf("  v_%d: parents = %s\n", v, isempty(parents) ? "{}" : string(parents))
end
println()

# Run with both ledger rules and compare
for (rule_name, rule) in [("Neutral", Neutral()),
                          ("EnumerateLLC", EnumerateLLC())]

    println("─" ^ 70)
    @printf("LEDGER RULE: %s\n", rule_name)
    println("─" ^ 70)

    cfg = GrowthConfig(ledger_rule=rule, max_parent_size=4)
    histories = GrowthHistory[]
    t0 = time()
    for s in 1:n_seeds
        seed_dag = make_seed()
        _, h = run_growth(seed_dag, target_extra_n, s; config=cfg)
        push!(histories, h)
    end
    elapsed = time() - t0
    @printf("Completed %d runs in %.2f s (%.2f ms/vertex)\n\n",
            n_seeds, elapsed, 1000 * elapsed / (n_seeds * target_extra_n))

    # Per-step profile statistics
    println("Average BDG profile across all steps × seeds:")
    s1 = 0.0; s2 = 0.0; s3 = 0.0; s4 = 0.0
    n_steps_total = 0
    for h in histories, step in h.steps
        s1 += step.N[1]; s2 += step.N[2]
        s3 += step.N[3]; s4 += step.N[4]
        n_steps_total += 1
    end
    @printf("  <N_1> = %.4f\n", s1 / n_steps_total)
    @printf("  <N_2> = %.4f\n", s2 / n_steps_total)
    @printf("  <N_3> = %.4f\n", s3 / n_steps_total)
    @printf("  <N_4> = %.4f\n", s4 / n_steps_total)
    @printf("  total steps: %d\n\n", n_steps_total)

    # Acceptance ratio
    all_ratios = vcat([acceptance_ratios(h) for h in histories]...)
    @printf("Acceptance ratio (admitted/total candidates):\n")
    @printf("  mean = %.4f, min = %.4f, max = %.4f\n\n",
            mean(all_ratios), minimum(all_ratios), maximum(all_ratios))

    # Top profiles selected
    prof_counts = Dict{NTuple{4,Int}, Int}()
    for h in histories, step in h.steps
        prof_counts[step.N] = get(prof_counts, step.N, 0) + 1
    end
    sorted = sort(collect(prof_counts), by = kv -> -kv[2])
    println("Top 8 selected profiles (N_1, N_2, N_3, N_4):")
    @printf("  %20s  %4s  %s\n", "(N_1,N_2,N_3,N_4)", "S", "count")
    for (N, c) in sorted[1:min(8, end)]
        S = bdgscore(N)
        @printf("  %20s  %4d  %d (%.1f%%)\n",
                string(N), S, c, 100*c/n_steps_total)
    end
    println()

    # Parent-set sizes
    psize_counts = parent_count_distribution(histories)
    total = sum(values(psize_counts))
    println("Parent-set size distribution:")
    for k in sort(collect(keys(psize_counts)))
        @printf("  size %d: %d (%.1f%%)\n", k, psize_counts[k],
                100 * psize_counts[k] / total)
    end
    println()

    # qN1 distribution (only meaningful for non-Neutral rules)
    if rule_name != "Neutral"
        qN1_counts = Dict{Int, Int}()
        for h in histories, step in h.steps
            q = step.vertex_qN1
            qN1_counts[q] = get(qN1_counts, q, 0) + 1
        end
        total = sum(values(qN1_counts))
        println("Vertex qN1 distribution (signed N1 charge):")
        for q in sort(collect(keys(qN1_counts)))
            @printf("  Q_N1 = %+d: %d (%.1f%%)\n", q, qN1_counts[q],
                    100 * qN1_counts[q] / total)
        end
        println()
    end
end

println("Done.")
