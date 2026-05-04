# Tests for the Ledger module.

@testset "Ledger" begin

    @testset "EdgeLedger construction and constraints" begin
        # Valid edges
        @test EdgeLedger() == EdgeLedger(0, (0, 0, 0))
        @test EdgeLedger(1).qN1 == 1
        @test EdgeLedger(-1, (1, 0, -1)).qN2 == (1, 0, -1)

        # Invalid: qN1 out of range
        @test_throws AssertionError EdgeLedger(2)
        @test_throws AssertionError EdgeLedger(-2, (0, 0, 0))

        # Invalid: qN2 component out of range
        @test_throws AssertionError EdgeLedger(0, (2, 0, 0))
        @test_throws AssertionError EdgeLedger(0, (0, -2, 0))
    end

    @testset "VertexLedger construction" begin
        @test VertexLedger() == VertexLedger(0, (0, 0, 0))
        # No range check on VertexLedger - it can hold sums up to ±3 (or more, briefly)
        v = VertexLedger(3, (3, -3, 1))
        @test v.qN1 == 3
        @test v.qN2 == (3, -3, 1)
    end

    @testset "sum_edge_ledgers" begin
        # Empty sum
        @test sum_edge_ledgers(EdgeLedger[]) == zero_vertex_ledger

        # Single edge
        @test sum_edge_ledgers([EdgeLedger(1, (1, 0, 0))]) == VertexLedger(1, (1, 0, 0))

        # Three edges, max in qN1 channel
        edges = [EdgeLedger(1), EdgeLedger(1), EdgeLedger(1)]
        @test sum_edge_ledgers(edges) == VertexLedger(3, (0, 0, 0))

        # Mixed sum
        edges = [EdgeLedger(1, (1, 0, 0)),
                 EdgeLedger(0, (0, 1, -1)),
                 EdgeLedger(-1, (-1, 0, 1))]
        @test sum_edge_ledgers(edges) == VertexLedger(0, (0, 1, 0))
    end

    @testset "qN1 admissibility (seven-value signature)" begin
        for q in -3:3
            @test qN1_admissible(VertexLedger(q, (0, 0, 0)))
        end
        @test !qN1_admissible(VertexLedger(4, (0, 0, 0)))
        @test !qN1_admissible(VertexLedger(-4, (0, 0, 0)))
    end

    @testset "qN2 admissibility" begin
        @test qN2_admissible(VertexLedger(0, (3, -3, 0)))
        @test !qN2_admissible(VertexLedger(0, (4, 0, 0)))
        @test !qN2_admissible(VertexLedger(0, (0, 0, -4)))
    end

    @testset "all_edge_signs covers 3^4 = 81 distinct edges" begin
        edges = all_edge_signs()
        @test length(edges) == 81
        @test length(Set(edges)) == 81  # no duplicates
        # Includes the zero edge
        @test zero_edge_ledger in edges
    end

    @testset "all_qN1_assignments combinatorics" begin
        @test all_qN1_assignments(0) == [()]
        @test length(all_qN1_assignments(1)) == 3
        @test length(all_qN1_assignments(2)) == 9
        @test length(all_qN1_assignments(3)) == 27
        # Every assignment of size k=2 has values in {-1,0,1}
        for t in all_qN1_assignments(2)
            for v in t
                @test v in (-1, 0, 1)
            end
        end
        # All k=2 sums are in {-2..+2}, all in range
        sums = [sum(t) for t in all_qN1_assignments(2)]
        @test minimum(sums) == -2 && maximum(sums) == 2
    end

    @testset "VertexLedger arithmetic" begin
        a = VertexLedger(1, (1, 0, -1))
        b = VertexLedger(2, (0, 1, 1))
        @test a + b == VertexLedger(3, (1, 1, 0))
        @test a - b == VertexLedger(-1, (1, -1, -2))
        @test a + zero_vertex_ledger == a
    end

    @testset "EdgeLedger and VertexLedger equality use distinct hashing" begin
        # Even with the same numeric content, EdgeLedger(0,(0,0,0)) and
        # VertexLedger(0,(0,0,0)) are different types; their hashes must
        # not collide trivially.
        e = zero_edge_ledger
        v = zero_vertex_ledger
        # They cannot be == (different types)
        @test e != v   # falls back to type-aware comparison
        # Hashes are different (with high probability) because they include
        # the type tag.
        @test hash(e) != hash(v)
    end

end
