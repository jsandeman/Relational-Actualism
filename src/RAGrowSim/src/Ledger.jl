"""
    Ledger

Signed ledger increments carried by edges in the actualization DAG, and
their sums at vertices.

Per RA-MATTER-CHARGE-001 (RAKB v0.4 candidate, Apr 28 2026):
  - N1 channel: signed integer in {-1, 0, +1} per edge.
    A vertex's net Q_N1 = Σ N1-channel over incoming edges, constrained
    to the seven-value signature {-3, -2, -1, 0, +1, +2, +3}.
    Electric translation: Q_e = (e/3) Q_N1.
  - N2 channel: spatial winding/branching ledger, three components
    (analog of color charge). LLC requires component-wise balance.

Per RA-OPEN-CHARGE-SIGN-001: the edge-level sign-source function is an
open formalization target. This module provides the data types and
constraints; the rule for assigning signs to edges lives in LedgerRules.

Per ChatGPT's note (April 28 2026): per-vertex LLC is enforced over the
eventual neighborhood, not at the instant of birth. At birth, we only
check that the incoming ledger lies in the admissible signature range.
Outgoing ports are virtual obligations to be settled by later
actualizations.

Type design:
  - `EdgeLedger`: per-edge ledger increment, qN1 ∈ {-1, 0, +1}.
  - `VertexLedger`: vertex-level sum, qN1 ∈ {-3..+3}; can also represent
    accumulated unbalanced ports.
  Sums of EdgeLedgers produce VertexLedgers.
"""
module Ledger

export EdgeLedger, VertexLedger, zero_edge_ledger, zero_vertex_ledger,
       qN1_admissible, qN2_admissible, sum_edge_ledgers,
       all_edge_signs, all_qN1_assignments

"""
    EdgeLedger

Per-edge signed ledger increment.

Fields:
  qN1::Int — signed integer in {-1, 0, +1}, electric-translation channel.
  qN2::NTuple{3,Int} — three components, each in {-1, 0, +1}, spatial
                       winding / strong-sector channel.
"""
struct EdgeLedger
    qN1::Int
    qN2::NTuple{3,Int}

    function EdgeLedger(qN1::Int, qN2::NTuple{3,Int})
        @assert qN1 in (-1, 0, 1) "EdgeLedger qN1 must be in {-1, 0, +1}, got $qN1"
        for (i, c) in enumerate(qN2)
            @assert c in (-1, 0, 1) "EdgeLedger qN2[$i] must be in {-1, 0, +1}, got $c"
        end
        new(qN1, qN2)
    end
end

# Convenience constructors
EdgeLedger() = EdgeLedger(0, (0, 0, 0))
EdgeLedger(qN1::Int) = EdgeLedger(qN1, (0, 0, 0))

const zero_edge_ledger = EdgeLedger()

"""
    VertexLedger

Sum of edge ledgers at a vertex. Wider integer ranges than EdgeLedger,
since sums of three signed inputs can reach ±3 in each component.
"""
struct VertexLedger
    qN1::Int
    qN2::NTuple{3,Int}
end

VertexLedger() = VertexLedger(0, (0, 0, 0))
const zero_vertex_ledger = VertexLedger()

# Conversion: sum of EdgeLedgers gives a VertexLedger
function sum_edge_ledgers(edges)::VertexLedger
    qN1 = 0
    a = 0; b = 0; c = 0
    for e in edges
        qN1 += e.qN1
        a += e.qN2[1]; b += e.qN2[2]; c += e.qN2[3]
    end
    VertexLedger(qN1, (a, b, c))
end

# Equality, hashing, display
import Base: ==, hash, show, +, -

==(a::EdgeLedger, b::EdgeLedger) = (a.qN1 == b.qN1 && a.qN2 == b.qN2)
==(a::VertexLedger, b::VertexLedger) = (a.qN1 == b.qN1 && a.qN2 == b.qN2)
hash(a::EdgeLedger, h::UInt) = hash(a.qN2, hash(a.qN1, hash(:edge, h)))
hash(a::VertexLedger, h::UInt) = hash(a.qN2, hash(a.qN1, hash(:vertex, h)))
show(io::IO, a::EdgeLedger) = print(io, "EdgeLedger(qN1=$(a.qN1), qN2=$(a.qN2))")
show(io::IO, a::VertexLedger) = print(io, "VertexLedger(qN1=$(a.qN1), qN2=$(a.qN2))")

# Arithmetic on VertexLedger (used for accumulating port balances over neighborhoods)
+(a::VertexLedger, b::VertexLedger) = VertexLedger(
    a.qN1 + b.qN1,
    (a.qN2[1] + b.qN2[1], a.qN2[2] + b.qN2[2], a.qN2[3] + b.qN2[3])
)
-(a::VertexLedger, b::VertexLedger) = VertexLedger(
    a.qN1 - b.qN1,
    (a.qN2[1] - b.qN2[1], a.qN2[2] - b.qN2[2], a.qN2[3] - b.qN2[3])
)

# Admissibility predicates

"""
    qN1_admissible(v::VertexLedger) :: Bool

Per Paper II §9.2: signed N1 sum at a vertex constrained to {-3..+3}
in 3+1D (at most three independent spatial directions).
"""
qN1_admissible(v::VertexLedger) = -3 <= v.qN1 <= 3

"""
    qN2_admissible(v::VertexLedger) :: Bool

Heuristic admissibility on the strong-sector channel. Each component
constrained to {-3..+3}. Stricter constraints (LLC over neighborhood,
component-wise color balance) are enforced over time, not at birth.
"""
qN2_admissible(v::VertexLedger) =
    all(abs(c) <= 3 for c in v.qN2)

# Enumeration helpers used by ledger rules

"""
    all_edge_signs() :: Vector{EdgeLedger}

The set of all syntactically-valid EdgeLedger values:
qN1 ∈ {-1,0,1}, qN2 each ∈ {-1,0,1}. Total 3⁴ = 81 distinct edges.
"""
function all_edge_signs()
    out = EdgeLedger[]
    for q in (-1, 0, 1)
        for a in (-1, 0, 1), b in (-1, 0, 1), c in (-1, 0, 1)
            push!(out, EdgeLedger(q, (a, b, c)))
        end
    end
    out
end

"""
    all_qN1_assignments(k::Int) :: Vector{NTuple{k,Int}}

All assignments of qN1 ∈ {-1,0,+1} to k edges, restricted to those whose
sum lies in the admissible signature {-3..+3}. Since k ≤ 3 in 3+1D
(at most three independent spatial directions), and -k ≤ sum ≤ k always
holds, all 3^k assignments are admissible for k ≤ 3.

For k > 3, this returns 3^k tuples without filtering — the caller is
responsible for applying qN1_admissible to each.
"""
function all_qN1_assignments(k::Int)
    @assert k >= 0
    if k == 0
        return [()]
    end
    rest = all_qN1_assignments(k - 1)
    out = NTuple{k,Int}[]
    for r in rest, q in (-1, 0, 1)
        push!(out, (q, r...))
    end
    out
end

end # module
