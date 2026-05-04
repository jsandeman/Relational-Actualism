# Python Audit Taxonomy for RAKB v0.5

## Artifact roles

| role | meaning | RAKB implication |
|---|---|---|
| `computational_derivation_candidate` | Script appears to derive/enumerate/check a theoretical expression. | Candidate `computes` edge after execution is reproduced. |
| `computational_experiment_or_benchmark` | Script runs a numerical test, simulation, benchmark, or forecast. | Candidate `supports` or `benchmark_support` edge. |
| `report_generator` | Script builds tables, plots, or deliverables. | Usually `generates_report`, not claim support by itself. |
| `kb_tool` | Script operates on the KB itself. | Infrastructure artifact, not scientific evidence. |
| `legacy_or_provenance` | Older source retained for restoration/history. | Do not promote without review. |

## Evidence relations

| relation | when to use |
|---|---|
| `computes` | Script deterministically computes a quantity used by a claim; command and outputs recorded. |
| `enumerates` | Script exhaustively enumerates a finite class or motif family. |
| `simulates` | Script samples or evolves a model; stochastic details recorded. |
| `benchmarks` | Script compares RA observable against measured data or benchmark. |
| `generates_report` | Script makes plots/tables but does not by itself support a claim. |
| `candidate_support` | Static evidence suggests relevance, but execution/content review is incomplete. |
| `mentions` | The file mentions a claim/term without supporting it. |
| `legacy_provenance` | Useful for recovery/history but not active support. |

## Promotion gates

A Python artifact can move from `candidate_support` to `computes`/`enumerates`/`benchmarks` only when all are true:

1. The file parses under the intended Python version.
2. Required packages and input data are recorded.
3. The exact command and working directory are recorded.
4. Outputs are saved or summarized with hashes where possible.
5. Randomness is absent or seed-controlled.
6. The claim statement matches the computed quantity.
7. Use of non-RA theoretical objects is classified as measurement input, benchmark, bridge comparison, or contamination.

## Contamination versus legitimate benchmark

A script that imports `PDG`, `QCD`, `ΛCDM`, `H0`, `DESI`, or other standard-theory vocabulary is not automatically invalid. It needs classification:

- `measurement_input`: empirical numerical datum only.
- `benchmark_comparison`: RA output compared to external measurement/model.
- `bridge_translation`: used to express an RA result in legacy notation.
- `mechanism_import`: legacy theory is functioning as the mechanism. This requires warning/demotion.

## Recommended Python claim-status vocabulary

```text
CE-static      computational evidence, static audit only
CE-reproduced  computational evidence, command/output reproduced
BENCH          benchmark/empirical comparison
ENUM           exhaustive enumeration
SIM            stochastic or numerical simulation
BRIDGE         bridge/cartography support only
LEGACY         provenance/restoration source
```
