# RA Weak-Field and Lensing Audit Memo v2

## What changed in this pass

This pass moved beyond “more benchmark numbers” and instead tightened the *architecture* of the gravitational benchmark story.

The key outcome is that the benchmark ladder is now much clearer:

- **safe now**: dense-regime weak-field consequences of the Paper III Einstein-sector bridge;
- **open hard wall**: canonical source-law closure for halo / cluster lensing.

## Main conclusions

### 1. The next technical bottleneck is not another benchmark script
It is the missing canonical weak-field source law connecting

- `P_act[T_{μν}]`
- the Paper III modified-Poisson form
- the script-level `ρ_A + ρ_λ` / `T00^(A)+Θ00^(λ)` split.

Until that is canonicalized, Solar-system and generic thin-lens benchmarks are solidly useful, while cluster-lensing claims should remain explicitly downstream.

### 2. The bridge-support Lean layer is weaker than its theorem names suggest
Direct inspection of the bridge-support files shows that the current `P_act`-conservation chain is still scaffold-level, not an end-to-end typed closure.

That means the suite should keep describing the gravitational bridge as a **derived translation chain with explicit assumptions**, not as a fully Lean-closed result.

### 3. The WEP subsection needs editorial repair now
The present Paper III wording places a provisional `10^-4` estimate in the proposition line and then immediately appeals to much smaller effective errors for ordinary matter.

The underlying scaling idea is good; the headline number should be moved out of the theorem-style statement.

### 4. The lensing programme now has a better order
The correct benchmark order is:

1. Casimir
2. Solar light deflection
3. Mercury perihelion
4. Generic thin-lens benchmark
5. Canonical source-law closure
6. Rotation-curve coefficient closure
7. Cluster lensing
8. Bullet Cluster

That ordering is both honest and strategically persuasive.

## Deliverables in this pass

- weak-field source-law docket
- dense-regime precision closure note
- lensing bridge note
- bridge-support supplement
- issue register update
- benchmark matrix update
- Paper III patch packet
- lensing benchmark script and output

## Recommendation

The best next move is now very specific:

> write the suite-primary source-law note, then rethread Paper III and the benchmark scripts through it.

That one move will do more for the viability case than adding three more phenomenology scripts.
