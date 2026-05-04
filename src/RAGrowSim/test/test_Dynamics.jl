# Tests for the dynamics module.

using Random

@testset "Dynamics" begin

    @testset "Single grow! step on empty DAG" begin
        d = DAG()
        rng = MersenneTwister(0)
        step = grow!(d, rng)
        # Empty DAG: only subset is the empty set, gives N=(0,0,0,0) S=1.
        @test step.v == 1
        @test step.parent_set == BitSet()
        @test step.N == (0, 0, 0, 0)
        @test step.S == 1
        @test step.n_candidates == 1
        @test step.n_admitted == 1
        @test d.n == 1
        # New fields
        @test isempty(step.edge_ledger)
        @test step.vertex_qN1 == 0
    end

    @testset "Reproducibility: same seed, same trajectory" begin
        d1, h1 = run_growth(8, 42)
        d2, h2 = run_growth(8, 42)
        @test d1.n == d2.n
        for (s1, s2) in zip(h1.steps, h2.steps)
            @test s1.parent_set == s2.parent_set
            @test s1.N == s2.N
            @test s1.S == s2.S
        end
    end

    @testset "All admitted profiles really have S > 0" begin
        d, h = run_growth(10, 7)
        for step in h.steps
            @test step.S > 0
            @test step.S == bdgscore(step.N)
        end
    end

    @testset "Empty parent set is always admitted" begin
        d, h = run_growth(8, 99)
        for step in h.steps
            @test step.n_admitted >= 1
        end
    end

    @testset "Profile is consistent with parent_set chosen" begin
        d, h = run_growth(8, 11)
        d2 = DAG()
        for step in h.steps
            recomputed_N = profile(d2, step.parent_set)
            @test recomputed_N == step.N
            addvertex!(d2, step.parent_set)
        end
    end

    # ───────────────────────────────────────────────────────────────
    # New tests for ledger rules and seeded growth
    # ───────────────────────────────────────────────────────────────

    @testset "Default config uses Neutral ledger rule" begin
        d, h = run_growth(5, 7)
        for step in h.steps
            # Neutral rule: all edge ledgers are zero, vertex_qN1 always 0
            @test step.vertex_qN1 == 0
            for e in step.edge_ledger
                @test e == zero_edge_ledger
            end
        end
    end

    @testset "EnumerateLLC config produces nonzero qN1 sometimes" begin
        cfg = GrowthConfig(ledger_rule=EnumerateLLC())
        # Need a non-trivial seed where parent sets larger than empty are
        # admitted. Use a chain-2 seed - then v_3 with parent {v_2} is admissible.
        seed = seed_chain(2)
        rng = MersenneTwister(0)
        steps_with_nonzero_qN1 = 0
        for _ in 1:30
            step = grow!(seed, rng, cfg)
            if step.vertex_qN1 != 0
                steps_with_nonzero_qN1 += 1
            end
        end
        # With EnumerateLLC, many candidates have non-zero qN1, so some
        # picked steps should too. (Stochastic; might rarely be zero by
        # bad luck. Use a generous threshold.)
        @test steps_with_nonzero_qN1 > 0
    end

    @testset "Seeded growth: chain-2 seed runs without error" begin
        seed = seed_chain(2)   # Returns a DAG with 2 vertices in a chain
        d, h = run_growth(seed, 5, 100)
        @test d.n == 2 + 5  # 2 seed + 5 added
        @test length(h.steps) == 5
    end

    @testset "Seeded growth: sym_branch seed runs without error" begin
        seed = seed_sym_branch()    # 4 vertices
        d, h = run_growth(seed, 3, 200)
        @test d.n == 4 + 3
        @test length(h.steps) == 3
    end

    @testset "max_parent_size cap is enforced" begin
        cfg = GrowthConfig(max_parent_size=2)
        seed = seed_chain(3)   # 3 vertices
        d, h = run_growth(seed, 5, 0; config=cfg)
        # Every selected parent set has size ≤ 2
        for step in h.steps
            @test length(step.parent_set) <= 2
        end
    end

    @testset "GrowthConfig fields are populated correctly" begin
        cfg = GrowthConfig(ledger_rule=EnumerateLLC(), max_parent_size=3)
        @test cfg.ledger_rule isa EnumerateLLC
        @test cfg.max_parent_size == 3
        @test cfg.enforce_llc_signature == true   # default
    end

end

