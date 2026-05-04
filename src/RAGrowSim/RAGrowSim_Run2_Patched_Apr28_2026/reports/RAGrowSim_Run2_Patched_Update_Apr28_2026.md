# RAGrowSim Run-2 patched update — Apr 28 2026

Claude's audit of the Run-2 methodology packet was correct.

## Blocking bug fixed

The original conditional-Poisson script used:

```julia
loggamma(n + 1)
```

without importing `SpecialFunctions`. This would fail at runtime.

The patched default script avoids the dependency by replacing pointwise log-PMF evaluation with a recurrence-generated Poisson probability vector:

```julia
p[1] = exp(-lambda)
for n in 1:maxn
    p[n+1] = p[n] * lambda / n
end
```

This is sufficient for the diagnostic μ ranges currently being explored and avoids modifying `Project.toml`.

## Methodology retained

The corrected script still compares simulator records to:

```text
raw Poisson:                 E[N_k | μ]
accepted-conditional Poisson: E[N_k | μ, S>0]
```

This remains the proper next test because the simulator records realized vertices that have passed the BDG acceptance condition.

## Recommendation

Do not update RAKB claims from the prior multi-seed output yet. Run the patched conditional-Poisson script and candidate-measure diagnostic first. The key question is whether the simulator differs from accepted-conditional Poisson once candidate-measure effects are understood.
