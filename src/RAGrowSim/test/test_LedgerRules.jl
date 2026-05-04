# Tests for the LedgerRules module.

@testset "LedgerRules" begin

    @testset "Neutral rule: single all-zero assignment per parent set" begin
        d = DAG()
        addvertex!(d, Int[])

        # Empty parent set: single empty edge list
        assignments = enumerate_ledger_assignments(Neutral(), d, Int[])
        @test length(assignments) == 1
        @test isempty(assignments[1])

        # Single parent: single one-element list of zero ledger
        assignments = enumerate_ledger_assignments(Neutral(), d, [1])
        @test length(assignments) == 1
        @test assignments[1] == [zero_edge_ledger]

        # Three parents (after building more vertices)
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        assignments = enumerate_ledger_assignments(Neutral(), d, [1, 2, 3])
        @test length(assignments) == 1
        @test length(assignments[1]) == 3
        @test all(e == zero_edge_ledger for e in assignments[1])
    end

    @testset "EnumerateLLC: 3^k assignments for k parents (k <= 3)" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        addvertex!(d, Int[])

        # 1 parent: 3 assignments (qN1 in {-1, 0, 1})
        a1 = enumerate_ledger_assignments(EnumerateLLC(), d, [1])
        @test length(a1) == 3
        # All are 1-element lists of EdgeLedger with qN1 in {-1, 0, 1}
        for assign in a1
            @test length(assign) == 1
            @test assign[1].qN1 in (-1, 0, 1)
        end

        # 2 parents: 9 assignments
        a2 = enumerate_ledger_assignments(EnumerateLLC(), d, [1, 2])
        @test length(a2) == 9

        # 3 parents: 27 assignments (all admissible since qN1_sum in {-3..+3})
        a3 = enumerate_ledger_assignments(EnumerateLLC(), d, [1, 2, 3])
        @test length(a3) == 27
    end

    @testset "EnumerateLLC: empty parent set gives one empty assignment" begin
        d = DAG()
        a = enumerate_ledger_assignments(EnumerateLLC(), d, Int[])
        @test length(a) == 1
        @test isempty(a[1])
    end

    @testset "OrientationRuleV0: throws on use" begin
        d = DAG()
        addvertex!(d, Int[])
        @test_throws ErrorException enumerate_ledger_assignments(
            OrientationRuleV0(), d, [1])
    end

    @testset "EnumerateLLC produces all valid qN1 sums" begin
        # For 2 parents, the qN1-sums seen across all 9 assignments
        # should be {-2, -1, 0, 1, 2}, with multiplicity.
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        a = enumerate_ledger_assignments(EnumerateLLC(), d, [1, 2])
        sums = [sum(e.qN1 for e in assign) for assign in a]
        @test Set(sums) == Set([-2, -1, 0, 1, 2])
        # Multiplicities: -2: 1 (-1,-1), -1: 2 (-1,0)+(0,-1), 0: 3 (0,0)+(1,-1)+(-1,1),
        # 1: 2, 2: 1. Total 9 ✓
        @test count(s -> s == 0, sums) == 3
        @test count(s -> s == 1, sums) == 2
        @test count(s -> s == -1, sums) == 2
    end

    @testset "EnumerateLLC: every returned assignment has admissible qN1 sum" begin
        d = DAG()
        for _ in 1:5
            addvertex!(d, Int[])
        end
        # 4 parents: 3^4 = 81, but qN1 sums could be -4..+4, only -3..+3 admitted.
        # The assignment with all 4 edges at +1 sums to +4: NOT admissible.
        # Similarly all -1: -4. So we expect 81 - 2 = 79 admissible assignments.
        a = enumerate_ledger_assignments(EnumerateLLC(), d, [1, 2, 3, 4])
        @test length(a) == 79
        for assign in a
            s = sum(e.qN1 for e in assign)
            @test -3 <= s <= 3
        end
    end

end
