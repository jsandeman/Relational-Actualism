# Run all tests for RAGrowSim.
# Usage:  julia --project=. test/runtests.jl

using Test

# Load the package once.
include("../src/RAGrowSim.jl")
using .RAGrowSim

include("test_BDGGrow.jl")
include("test_Antichains.jl")
include("test_Dynamics.jl")
include("test_Ledger.jl")
include("test_LedgerRules.jl")
include("test_Seeds.jl")
