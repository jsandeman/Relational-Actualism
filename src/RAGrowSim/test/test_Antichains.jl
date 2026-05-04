# Tests for antichain enumeration.

@testset "Antichain enumeration" begin

    @testset "Empty DAG" begin
        d = DAG()
        acs = all_antichains(d)
        @test acs == [BitSet()]
    end

    @testset "Single isolated vertex" begin
        d = DAG()
        addvertex!(d, Int[])
        acs = all_antichains(d)
        @test Set(acs) == Set([BitSet(), BitSet([1])])
    end

    @testset "Two isolated vertices" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        acs = all_antichains(d)
        @test Set(acs) == Set([BitSet(), BitSet([1]), BitSet([2]), BitSet([1,2])])
        @test length(acs) == 4
    end

    @testset "Three vertices: 1, 2 isolated, 3 has parent 1" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        addvertex!(d, [1])
        acs = all_antichains(d)
        # 1 < 3.  Antichains: {}, {1}, {2}, {3}, {1,2}, {2,3}.
        # NOT antichains: {1,3} (1 ancestor of 3), {1,2,3}.
        expected = Set([
            BitSet(),
            BitSet([1]), BitSet([2]), BitSet([3]),
            BitSet([1,2]), BitSet([2,3])
        ])
        @test Set(acs) == expected
        @test length(acs) == 6
    end

    @testset "Length-3 chain: 1<2<3" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, [1])
        addvertex!(d, [2])
        acs = all_antichains(d)
        @test Set(acs) == Set([BitSet(), BitSet([1]), BitSet([2]), BitSet([3])])
    end

    @testset "Diamond: 1 -> 2,3 -> 4" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, [1])
        addvertex!(d, [1])
        addvertex!(d, [2, 3])
        acs = all_antichains(d)
        # 2,3 NOT comparable to each other.
        # Antichains: {}, {1}, {2}, {3}, {4}, {2,3}.  Total 6.
        expected = Set([
            BitSet(), BitSet([1]), BitSet([2]),
            BitSet([3]), BitSet([4]), BitSet([2,3])
        ])
        @test Set(acs) == expected
        @test length(acs) == 6
    end

    @testset "No duplicates ever" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, Int[])
        addvertex!(d, [1])
        addvertex!(d, [2])
        addvertex!(d, [1, 2])
        addvertex!(d, [3, 4])
        acs = all_antichains(d)
        @test length(acs) == length(Set(acs))
    end

end
