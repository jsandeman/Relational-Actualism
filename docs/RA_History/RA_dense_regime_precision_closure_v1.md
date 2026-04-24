# RA Dense-Regime Precision Closure Note v1

## Core problem

Paper III currently does two things in the same WEP subsection:

1. it states a headline tracking estimate at the `10^-4` level;
2. it then immediately notes that modern WEP tests are at `10^-14` precision and that compatibility requires much faster equilibration.

Those two moves are not strictly contradictory, but they are rhetorically unstable when placed back-to-back.

## Better interpretation

The underlying structural claim appears to be:

\[
\frac{|\rho_A - \rho_{\mathrm{matter}}|}{\rho_{\mathrm{matter}}}
\sim \frac{\tau_{\mathrm{eq}}}{t_{\mathrm{cosm}}}.
\]

That is the real RA statement.

The fixed number `10^-4` is best read as a coarse, provisional scale estimate, **not** as the intended final accuracy for ordinary baryonic matter.

## Why this matters

If the paper leaves `10^-4` in the proposition line, a skeptical reader will reasonably conclude:

- RA weak-field recovery is much too weak for present Solar-system / laboratory precision;
- the suite is asking the reader to infer an unstated stronger bound later in the same paragraph.

That is avoidable.

## Safer proposition wording

A cleaner proposition is:

> For baryonic matter with local equilibration timescale \(\tau_{\mathrm{eq}}\), the actualization density tracks the matter density with relative error of order \(\tau_{\mathrm{eq}}/t_{\mathrm{hist}}\), where \(t_{\mathrm{hist}}\) is the relevant accumulation timescale. In ordinary dense baryonic environments this error is expected to be extremely small; a quantitative derivation of the bound remains an open target.

This does three things correctly:

1. keeps the **structural mechanism**;
2. avoids pinning the headline to a weak provisional number;
3. preserves the open-closure honesty.

## Practical audit recommendation

### Keep as present benchmark support
- Solar-system benchmarks remain valid as **conditional domain-recovery consequences** of the dense-regime GR bridge.

### Do not yet claim
- a directly derived RA bound at the `10^-14` level,
- or a theorem-level WEP closure across all ordinary matter.

## Closure docket

### P1. Define the relevant history timescale
Clarify whether the denominator should be:

- cosmic age,
- local assembly time,
- local relaxation time,
- or a source-dependent causal-depth age.

### P2. Derive baryonic equilibration timescales
The bridge needs a real RA estimate for how fast ordinary matter drives \(\rho_A \to \rho_{\mathrm{matter}}\).

### P3. Convert to precision observables
Once \(\tau_{\mathrm{eq}}\) is controlled, the same chain should bound:

- WEP violations,
- dense-regime metric-source mismatch,
- post-Newtonian parameter drift.

## Paper-facing patch recommendation

The cleanest immediate fix is editorial, not mathematical:

- remove `10^-4` from the proposition headline;
- keep the scaling law;
- move the numerical bound to a discussion sentence labeled provisional;
- explicitly mark precision closure as open.

## Bottom line

The dense-regime precision problem is not “RA fails WEP.”

It is:

> **the current paper states the right scaling idea but the wrong headline number.**

That is a fixable presentation issue now, and a genuine derivation target later.
