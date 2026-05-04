"""
    LedgerRules

Pluggable strategies for assigning EdgeLedger values to the immediate-
predecessor edges of a candidate new vertex.

Per RA-OPEN-CHARGE-SIGN-001 (RAKB v0.4 candidate, Apr 28 2026), the
edge-level sign-source for the signed N1 charge is an open formalization
target. This module provides multiple rules for use in simulation, with
explicit epistemic labeling. None of these rules is yet the canonical
RA rule; each is a candidate or a baseline.

Available rules (all subtypes of LedgerRule):

  Neutral:
    All edges carry the zero ledger. Equivalent to the no-charge
    baseline. Useful for isolating BDG dynamics from ledger
    enumeration.

  EnumerateLLC:
    For each candidate parent set of size k, enumerate all 3^k
    assignments of qN1 ∈ {-1, 0, +1} per edge. (qN2 enumeration deferred
    until needed; see strong-sector tracking.) Filters by the seven-
    value signature qN1_admissible at the candidate vertex. Each
    (parent_set, qN1_assignment) is a separate candidate; the dynamics'
    uniform-pick is over the joint space.

    This is NOT a claim about physical measure. It is the conservative
    "no preferred orientation" baseline that doesn't import a sign-source
    rule we don't have.

  OrientationRuleV0 (placeholder):
    A future rule deriving signs from a graph-native orientation
    convention. Not yet implemented; kept here as a stub so the
    interface is visible.
"""
module LedgerRules

using ..BDGGrow
using ..Ledger

export LedgerRule, Neutral, EnumerateLLC, OrientationRuleV0,
       enumerate_ledger_assignments

"""
Abstract supertype for all ledger rules.
"""
abstract type LedgerRule end

"""
    Neutral

Rule: every edge carries the zero ledger. The single ledger
assignment is the all-zero one.
"""
struct Neutral <: LedgerRule end

"""
    EnumerateLLC

Rule: enumerate all qN1 ∈ {-1, 0, +1} assignments to the immediate-
predecessor edges, filter by qN1_admissible at the candidate vertex.
Other channels (qN2) carry zero by default in this rule; a future
extension can enumerate them too.

This is the conservative baseline that respects LLC's signature
constraint without committing to a sign-source.
"""
struct EnumerateLLC <: LedgerRule end

"""
    OrientationRuleV0

Placeholder for an orientation-based sign-source rule. Not yet implemented;
calling enumerate_ledger_assignments with this rule throws NotImplementedError.
"""
struct OrientationRuleV0 <: LedgerRule end

"""
    enumerate_ledger_assignments(rule::LedgerRule, d::DAG, parent_set)
        -> Vector{Vector{EdgeLedger}}

For a candidate new vertex v with given parent set, return the list of
admissible edge-ledger assignments under the active rule. Each element
of the returned list is a Vector{EdgeLedger} with one EdgeLedger per
parent vertex, in the same iteration order as `parent_set`.

For example, if parent_set has size 2 and the rule is EnumerateLLC, the
return is a vector of 9 candidate assignments, one per (qN1_a, qN1_b)
choice in {-1, 0, +1}^2.
"""
function enumerate_ledger_assignments end

# Neutral: a single all-zero assignment, regardless of parent set.
function enumerate_ledger_assignments(::Neutral, d::DAG, parent_set)
    k = length(parent_set)
    [[zero_edge_ledger for _ in 1:k]]
end

# EnumerateLLC: all 3^k qN1 assignments where the qN1-sum at v is admissible.
function enumerate_ledger_assignments(::EnumerateLLC, d::DAG, parent_set)
    k = length(parent_set)
    out = Vector{EdgeLedger}[]
    for q_tuple in all_qN1_assignments(k)
        qN1_sum = sum(q_tuple; init=0)
        if -3 <= qN1_sum <= 3
            edges = [EdgeLedger(q_tuple[i]) for i in 1:k]
            push!(out, edges)
        end
    end
    out
end

# OrientationRuleV0: stub
function enumerate_ledger_assignments(::OrientationRuleV0, d::DAG, parent_set)
    error("OrientationRuleV0 is a placeholder; sign-source rule not yet defined per RA-OPEN-CHARGE-SIGN-001")
end

end # module
