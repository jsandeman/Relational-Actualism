# RAGrowSim Run-2 Methodological Review — Apr 28 2026

## Executive verdict

The new multi-seed / μ-conditional run is a genuinely useful simulator milestone, but it should **not yet be used to update settled RAKB claims**. It should be treated as exploratory evidence for three open methodological questions:

1. **Growth-measure question**: is RA sequential growth uniform over edgeful parent subsets, causal closures/downsets, BDG profiles, or some action-weighted candidate class?
2. **Local-density question**: what is the RA-native finite-graph estimator corresponding to the Poisson-CSG parameter μ?
3. **Poisson-approximation question**: under which regime, if any, do finite RA growth trajectories reproduce Poisson-CSG shell statistics?

The run is strongest as evidence that the simulator is now nontrivial and that canonical seeds converge into a shared motif region. It is weaker as evidence for or against closed-form paper predictions, because the current `local_mu` and candidate measure are still heuristic.

## What the run establishes

### 1. The simulator is no longer in the empty-DAG pathology

The multi-seed run uses seeded initial conditions and Neutral ledger rule, so it isolates BDG growth without charge-sign multiplicity. The four seeds all produce nontrivial profiles, with mean parent-set size around 3.2–3.4 and mean BDG score around 9–15.

This is real progress: the simulator is exercising the BDG motif landscape rather than repeatedly selecting isolated vertices.

### 2. Seed dependence is moderate but not gone

Reported means:

| seed | <N1> | <N2> | <N3> | <N4> | <S> | <parent size> |
|---|---:|---:|---:|---:|---:|---:|
| chain2 | 1.7024 | 1.8608 | 0.6072 | 0.8344 | 13.00 | 3.21 |
| chain4 | 1.6336 | 1.7416 | 0.8216 | 0.9272 | 9.31 | 3.43 |
| sym_branch | 1.7664 | 1.9880 | 0.5960 | 0.9784 | 15.42 | 3.44 |
| asym_branch | 1.8080 | 2.0216 | 0.7552 | 0.9648 | 13.02 | 3.44 |

The spreads across seeds are roughly 0.14–0.28 per channel. This suggests partial convergence into a common region, not yet a demonstrated stationary distribution.

### 3. The μ≈1 row is not a clean Poisson test

The current script defines:

```julia
local_mu := |ancestors(v)| / max(1, longest_chain_to(v))
```

That is a useful branch-density heuristic, but it is not an independent Poisson sprinkling density. In a chain-tip region, `|ancestors| ≈ longest_chain`, so `local_mu ≈ 1` and `N1 ≈ 1` essentially by construction. Therefore the reported agreement:

```text
μ≈1: sim N1 = 1.009 vs Poisson N1 = 1.000
```

is mostly a binning artifact, not a physical validation of the Poisson approximation.

The deeper-channel deviations in the μ≈1 bin remain informative, but they should be described as conditional on this chain-density heuristic, not on a formal Poisson μ.

## What remains unresolved

### 1. Candidate measure dominates interpretation

The simulator currently samples uniformly among admitted parent subsets up to `max_parent_size=4`.

That is not a neutral modeling choice. There are at least three distinct measures:

- **edgeful parent-subset measure**: every explicit parent-link set counts separately;
- **closure/downset measure**: parent sets with the same transitive past are quotiented;
- **profile measure**: candidates with the same BDG `(N1,N2,N3,N4)` profile are quotiented;
- **action-weighted measure**: admitted candidates are weighted by a function of `S` rather than uniformly.

The current run uses the first, with a size cap. This likely biases toward parent sets near the cap, because the number of subsets grows combinatorially with size. The high parent-size means are therefore not yet interpretable as a physical result.

### 2. Acceptance ratio is not directly comparable to `P_acc(μ=1)`

The reported simulator acceptance ratio is a count over capped candidate subsets. The closed-form `P_acc(μ)` is a probability under a Poisson-CSG profile distribution. These are different sample spaces. They should not be compared as if they were the same observable.

The correct comparison requires aligning the measure first.

### 3. Poisson predictions may survive at the aggregate-action level

Claude's cancellation observation is important. Even when individual channels deviate strongly from Poisson, the BDG score

```text
S = 1 - N1 + 9N2 - 16N3 + 8N4
```

can show much smaller discrepancy because the deviations are correlated and the signed coefficients cancel. Therefore closed-form predictions that depend on aggregate BDG action may be more robust than predictions depending on the full joint profile distribution.

This argues for a case-by-case audit, not a blanket demotion of all Poisson-based derivations.

## Recommended next experiments before any RAKB claim update

### Experiment A — local-μ estimator comparison

Run the revised analysis script that reports multiple μ estimators:

1. `mu_depth = |ancestors| / longest_chain`, the current heuristic.
2. `mu_v4`, obtained by inverting
   `V4 = μ + μ²/2 + μ³/6 + μ⁴/24`, where `V4=N1+N2+N3+N4`.
3. `mu_mle`, the one-parameter Poisson profile fit to the observed `(N1..N4)`.

Important caveat: `mu_v4` and `mu_mle` are fitted from the same profile being tested, so they should be used for **composition residuals**, not as independent density measurements.

### Experiment B — candidate-measure diagnostic

For the same pre-growth DAGs, count:

- number of parent subsets;
- number of unique causal closures;
- number of unique BDG profiles;
- multiplicity of each closure/profile under the parent-subset measure;
- how selected profile probabilities change under subset vs closure quotient.

This directly tests whether the current results are mostly a measure artifact.

### Experiment C — one prediction-specific audit

After A and B, test one closed-form prediction against the simulator's actual empirical joint distribution. The best first target is the `f0` path-weight ratio, because it is explicitly a profile-weight enumeration and likely sensitive to the joint distribution.

## Recommended RAKB status

Do **not** promote the simulation outputs to claim support yet.

Recommended status if/when recorded:

```text
artifact: RAGrowSim
role: exploratory_simulator
status: source_reviewed_not_claim_support
links:
  RA-OPEN-GROWTH-MEASURE-001
  RA-OPEN-LOCAL-MU-001
  RA-OPEN-POISSON-DYNAMICS-001
  RA-OPEN-CHARGE-SIGN-001
```

Suggested new issue:

```text
RA-OPEN-LOCAL-MU-001 — RA-native finite-graph local density estimator
```

This should join the already-proposed growth-measure and Poisson-dynamics issues.

## Bottom line

The new run strengthens the case that finite RA growth has a structured motif ecology, not a simple Poisson shell process. But the next decisive step is not scaling alone. It is to control for candidate measure and define the finite-graph μ observable.

## Addendum: two corrections to Claude's interpretation

### Correction 1 — compare realized vertices to accepted-conditional Poisson, not raw Poisson

The simulator records **selected realized vertices**, and every selected vertex has already passed the BDG filter `S>0`. Therefore the immediate Poisson comparison should not be raw

```text
E[N_k] = μ^k/k!
```

but rather

```text
E[N_k | S(N)>0]
```

under the Poisson-CSG candidate distribution. The raw Poisson shell means are the candidate/potentia baseline; the simulator's selected-vertex means are the post-filter actualization distribution. Comparing selected simulation records to raw Poisson exaggerates or mischaracterizes the discrepancy.

A proper test needs three layers:

```text
raw candidate distribution       P(N | μ)
acceptance probability           P(S>0 | μ)
realized/accepted distribution   P(N | μ, S>0)
```

The current run only reports the realized/accepted side.

### Correction 2 — the aggregate-BDG-score cancellation claim is not supported by the printed numbers

Claude suggested that channel-wise deviations cancel strongly in the BDG score. For the μ≈1 row, the simulator value is:

```text
S_sim ≈ 1 - 1.009 + 9(1.002) - 16(0.707) + 8(0.714) ≈ 3.41
```

The raw Poisson μ=1 expectation is:

```text
S_Pois = 1 - 1 + 9(0.5) - 16(1/6) + 8(1/24) = 2.1667
```

not 3.16. So even at μ≈1 the aggregate action differs by roughly 57% relative to the raw Poisson value. At μ≈1.5 and μ≈2 the discrepancy is much larger because the simulator suppresses N3 and boosts N4 relative to raw Poisson in a way that increases S.

This does **not** yet invalidate the paper calculations, because the relevant baseline may be accepted-conditional Poisson rather than raw Poisson. But it does mean we should not lean on the cancellation argument until the conditional calculation is done.
