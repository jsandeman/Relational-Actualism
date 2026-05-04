# Tests for the BDGGrow core engine.
# Assumes runtests.jl has already loaded RAGrowSim.

@testset "BDGGrow core engine" begin

    @testset "Empty DAG: first vertex" begin
        d = DAG()
        @test d.n == 0
        N = profile(d, Int[])
        @test N == (0, 0, 0, 0)
        @test bdgscore(N) == 1
        v = addvertex!(d, Int[])
        @test v == 1
        @test d.n == 1
        @test ancestorsof(d, 1) == BitSet()
    end

    @testset "Length-4 chain: v_5 with parent {v_4} has N=(1,1,1,1) S=1" begin
        d = DAG()
        addvertex!(d, Int[])             # v_1
        addvertex!(d, [1])               # v_2
        addvertex!(d, [2])               # v_3
        addvertex!(d, [3])               # v_4
        @test ancestorsof(d, 1) == BitSet()
        @test ancestorsof(d, 2) == BitSet([1])
        @test ancestorsof(d, 3) == BitSet([1, 2])
        @test ancestorsof(d, 4) == BitSet([1, 2, 3])
        N = profile(d, [4])
        @test N == (1, 1, 1, 1)
        @test bdgscore(N) == 1
    end

    @testset "Diamond: v_1 < {v_2, v_3}, propose v_4 with parents {v_2,v_3}" begin
        d = DAG()
        addvertex!(d, Int[])             # v_1
        addvertex!(d, [1])               # v_2
        addvertex!(d, [1])               # v_3
        N = profile(d, [2, 3])
        @test N == (2, 0, 1, 0)
        @test bdgscore(N) == -17
    end

    @testset "Profile is independent of parent_set type" begin
        d = DAG()
        addvertex!(d, Int[])
        addvertex!(d, [1])
        addvertex!(d, [1])
        addvertex!(d, [2, 3])
        N1 = profile(d, [4])
        N2 = profile(d, BitSet([4]))
        @test N1 == N2
    end

    @testset "BDG identities (Lean-verified, O14)" begin
        @test BDG_C[2] + BDG_C[3] + BDG_C[4] + BDG_C[5] == 0     # Σ c_k for k=1..4
        @test BDG_C[1] + BDG_C[2] == 0                            # c_0 + c_1
        @test BDG_C[1] + 2*BDG_C[2] + BDG_C[3] == BDG_C[5]        # c_0+2c_1+c_2 = c_4
        @test BDG_C[5] == 8
        @test bdgscore((1,1,1,1)) == 1
    end

    @testset "Spawn-vertex (no parents) always has N=(0,0,0,0) S=1" begin
        d = DAG()
        for _ in 1:10
            addvertex!(d, Int[])
        end
        N = profile(d, Int[])
        @test N == (0, 0, 0, 0)
        @test bdgscore(N) == 1
    end

end
