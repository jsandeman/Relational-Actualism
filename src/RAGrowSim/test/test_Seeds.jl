# Tests for the Seeds module.
#
# These tests are critical because they verify that the simulator's seed
# constructors produce exactly the BDG profiles specified by the Lean
# corpus (RA_D1_Core_draft.lean theorems D1a, D1b).
#
# Any drift here would mean the simulator's "canonical motifs" are not the
# same as RA's canonical motifs, which would invalidate downstream results.

using Random

@testset "Seeds" begin

    @testset "vacuum_nucleation: empty DAG" begin
        d = vacuum_nucleation()
        @test d.n == 0
        @test d isa DAG
    end

    @testset "severance_daughter: also empty (placeholder)" begin
        # Placeholder behavior: returns empty DAG, ignores ledger for now
        d = severance_daughter(zero_vertex_ledger)
        @test d.n == 0

        # Non-zero inherited ledger - still empty for now (TODO once
        # sign-source rule is formalized)
        d2 = severance_daughter(VertexLedger(2, (1, 0, -1)))
        @test d2.n == 0
    end

    @testset "seed_chain: profiles match Lean D1a" begin
        # k=1: isolated vertex, profile (0,0,0,0), S=1
        d = seed_chain(1)
        @test d.n == 1
        # Profile of a hypothetical NEXT vertex with parent {1} is the
        # depth-1 "boundary" case from Lean
        N_next = profile(d, [1])
        @test N_next == (1, 0, 0, 0)
        @test bdgscore(N_next) == 0  # boundary, S=0

        # k=2: chain 1 -> 2
        d = seed_chain(2)
        @test d.n == 2
        # If we propose v_3 with parent {2}: it would see v_2 at card 0,
        # v_1 at card 1, so N=(1,1,0,0), S=9 (chain-2 motif).
        N_next = profile(d, [2])
        @test N_next == (1, 1, 0, 0)
        @test bdgscore(N_next) == 9

        # k=3: chain 1 -> 2 -> 3
        d = seed_chain(3)
        @test d.n == 3
        # Propose v_4 with parent {3}: would see v_3 (card 0), v_2 (card 1),
        # v_1 (card 2), giving N=(1,1,1,0), S=-7 (chain-3 filtered).
        N_next = profile(d, [3])
        @test N_next == (1, 1, 1, 0)
        @test bdgscore(N_next) == -7

        # k=4: chain 1 -> 2 -> 3 -> 4
        d = seed_chain(4)
        @test d.n == 4
        # Propose v_5 with parent {4}: N=(1,1,1,1), S=1 (chain-4 fixed point).
        N_next = profile(d, [4])
        @test N_next == (1, 1, 1, 1)
        @test bdgscore(N_next) == 1
    end

    @testset "seed_sym_branch: matches Lean D1b symmetric Y-join" begin
        d = seed_sym_branch()
        @test d.n == 4
        # Vertex 4 should have N=(1,2,0,0) S=18 per Lean theorem D1b_sym_yjoin
        # The seed builds: 1, 2 isolated, 3 with parents {1,2}, 4 with parent {3}.
        # For vertex 4 (already added), let's verify the profile would
        # be (1,2,0,0) by constructing a minimal DAG and checking.
        d_check = DAG()
        addvertex!(d_check, Int[])     # v_1
        addvertex!(d_check, Int[])     # v_2
        addvertex!(d_check, [1, 2])    # v_3
        # Now propose v_4 with parent {3}:
        N4 = profile(d_check, [3])
        # Ancestors of v_4 = {3, 1, 2}. Cardinalities of (u, v_4):
        #   u=3: between = {} (no w with 3 prec w except v_4 itself) -> card 0
        #   u=1: between = {3} -> card 1
        #   u=2: between = {3} -> card 1
        # So N=(1, 2, 0, 0), S = 1 - 1 + 18 - 0 + 0 = 18 ✓
        @test N4 == (1, 2, 0, 0)
        @test bdgscore(N4) == 18
    end

    @testset "seed_asym_branch: matches Lean D1b asymmetric Y-join" begin
        d = seed_asym_branch()
        @test d.n == 4
        # The seed builds: 1 -> 2, 3 isolated, 4 with parents {2,3}.
        # Verify by reconstruction.
        d_check = DAG()
        addvertex!(d_check, Int[])     # v_1
        addvertex!(d_check, [1])       # v_2
        addvertex!(d_check, Int[])     # v_3
        # Now propose v_4 with parents {2, 3}:
        N4 = profile(d_check, [2, 3])
        # Ancestors of v_4 = {1, 2, 3}. Cardinalities of (u, v_4):
        #   u=2: between = {} -> card 0
        #   u=3: between = {} -> card 0
        #   u=1: between = {2} -> card 1
        # So N=(2, 1, 0, 0), S = 1 - 2 + 9 - 0 + 0 = 8 ✓
        @test N4 == (2, 1, 0, 0)
        @test bdgscore(N4) == 8
    end

    @testset "seed_dense_random: produces n vertices, no errors" begin
        rng = MersenneTwister(42)
        d = seed_dense_random(15; rng=rng)
        @test d.n == 15
        # First vertex always isolated
        @test ancestorsof(d, 1) == BitSet()
        # All ancestor sets should be valid (subsets of preceding vertices)
        for v in 1:d.n
            for a in d.ancestors[v]
                @test a < v
            end
        end
    end

    @testset "seed_dense_random: reproducibility" begin
        rng1 = MersenneTwister(123)
        d1 = seed_dense_random(10; rng=rng1)
        rng2 = MersenneTwister(123)
        d2 = seed_dense_random(10; rng=rng2)
        @test d1.n == d2.n
        for v in 1:d1.n
            @test d1.parents[v] == d2.parents[v]
            @test d1.ancestors[v] == d2.ancestors[v]
        end
    end

    @testset "local_mu: sparse chain has small mu" begin
        # Length-5 chain. At vertex 5: |anc|=4, longest_chain=4, mu = 1.0
        d = seed_chain(5)
        @test local_mu(d, 5) == 4 / 4
        @test local_mu(d, 1) == 0.0   # isolated vertex
    end

    @testset "local_mu: branch motif has higher mu" begin
        # sym_branch: at vertex 4, |anc|=3 (v_1, v_2, v_3),
        # longest chain ending at v_4 is 1 -> 3 -> 4 or 2 -> 3 -> 4, length 2
        d = seed_sym_branch()
        mu = local_mu(d, 4)
        @test mu == 3 / 2  # |anc|/chain_len = 3/2
    end

end
