"""
    RAGrowSim

Top-level module for the BDG growth simulator with ledger and seeded
initial conditions (April 28 2026 architecture).

Submodules (in dependency order):
  - BDGGrow:     core engine (DAG, profile, bdgscore)
  - Ledger:      EdgeLedger, VertexLedger, admissibility predicates
  - LedgerRules: pluggable strategies for assigning edge ledgers
  - Antichains:  antichain enumeration (kept for completeness; not used
                 by Dynamics in this version)
  - Dynamics:    the growth rule with all-subsets enumeration + ledger
  - Seeds:       vacuum_nucleation, severance_daughter, canonical D1 seeds
  - Observables: statistics from a GrowthHistory

Each submodule is re-exported so that `using RAGrowSim` brings the
public API into scope.

See README.md for usage and methodological notes.
"""
module RAGrowSim

include("BDGGrow.jl")
include("Ledger.jl")
include("LedgerRules.jl")
include("Antichains.jl")
include("Dynamics.jl")
include("Seeds.jl")
include("Observables.jl")

using .BDGGrow
using .Ledger
using .LedgerRules
using .Antichains
using .Dynamics
using .Seeds
using .Observables

# Re-export the public API
export DAG, addvertex!, ancestorsof, profile, bdgscore, BDG_C
export EdgeLedger, VertexLedger, zero_edge_ledger, zero_vertex_ledger,
       qN1_admissible, qN2_admissible, sum_edge_ledgers,
       all_edge_signs, all_qN1_assignments
export all_antichains
export grow!, run_growth, GrowthStep, GrowthHistory, GrowthConfig
export running_profile_means, acceptance_ratios, max_antichain_widths,
       step_S_distribution, parent_count_distribution
export LedgerRule, Neutral, EnumerateLLC, OrientationRuleV0,
       enumerate_ledger_assignments
export vacuum_nucleation, severance_daughter,
       seed_chain, seed_sym_branch, seed_asym_branch,
       seed_dense_random, local_mu

end # module
