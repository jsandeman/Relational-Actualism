# RA Casimir Benchmark Note v1

## Purpose

This note reframes the Casimir effect as a **Nature-facing benchmark** for Relational Actualism rather than as a translation exercise. The target is a measurable pressure between conducting plates, not the recovery of any particular legacy formalism for its own sake.

## Benchmark question

Can RA compute a configuration-dependent vacuum effect while suppressing the absolute vacuum term?

That is the right test because it bears simultaneously on:

1. calculational usefulness,
2. the vacuum-energy issue,
3. the AQFT / semiclassical-gravity bridge,
4. the claim that RA preserves physically real boundary-induced effects while projecting out non-actualized vacuum support.

## Observable

Two perfectly conducting parallel plates separated by distance
\[
  d = 1\,\mu\text{m}
\]
with measured Casimir pressure of order
\[
  p_z \approx -1.3\times 10^{-3}\,\text{Pa}.
\]

## Current computational artifact

- Script: `casimir_benchmark.py`
- Current role: benchmark witness / bridge note
- Status in the current audit: **strong runnable witness, but not yet the final suite-primary formal closure**

## Core calculation used in the script

For the standard renormalized Casimir configuration between plates,
\[
  u = -\frac{\pi^2 \hbar c}{720 d^4},
  \qquad
  p_z = -\frac{\pi^2 \hbar c}{240 d^4},
  \qquad
  p_\perp = +\frac{\pi^2 \hbar c}{720 d^4}.
\]

The script verifies:

- tracelessness of the massless stress tensor,
- local bulk conservation,
- numerical evaluation at \(d=1\,\mu\text{m}\),
- RA vacuum subtraction,
- consistency of the modified source with the Bianchi identity.

The RA prescription in the script is
\[
  \langle T^{\mu\nu}_{\mathrm{RA}} \rangle
  :=
  \langle T^{\mu\nu}_{\mathrm{ren}}[g,\Phi] \rangle
  -
  \langle T^{\mu\nu}_{\mathrm{ren}}[g,|0\rangle] \rangle.
\]

For the plate geometry, this yields
\[
  \langle T^{\mu\nu}_{\mathrm{RA}} \rangle
  =
  \langle T^{\mu\nu}_{\mathrm{Casimir}} \rangle,
\]
so the configuration-dependent effect is preserved while the absolute Minkowski vacuum term self-subtracts.

## Numerical result from the current script run

At plate separation \(d=1\,\mu\text{m}\):

- energy density:
  \[
    \langle T^{tt}_{\mathrm{RA}} \rangle = -4.3340\times 10^{-4}\,\text{J/m}^3,
  \]
- normal pressure:
  \[
    \langle T^{zz}_{\mathrm{RA}} \rangle = -1.3002\times 10^{-3}\,\text{Pa},
  \]
- transverse pressure:
  \[
    \langle T^{xx}_{\mathrm{RA}} \rangle = \langle T^{yy}_{\mathrm{RA}} \rangle = +4.3340\times 10^{-4}\,\text{Pa}.
  \]

These values are numerically consistent with the usual measured Casimir-pressure scale at this separation.

## What this benchmark currently supports

### Strong support

- RA can be presented as a calculational tool for a concrete observable.
- The configuration-dependent force is preserved exactly in the current benchmark prescription.
- The vacuum-subtraction move is compatible with local conservation in the plate geometry.
- The benchmark is simple enough to serve as a flagship “first calculational note.”

### What it does **not** yet settle

- full AQFT modular-flow closure,
- the remaining formal commutativity target in the Unruh / stationarity layer,
- strong-coupling / non-perturbative regimes,
- full curved-spacetime backreaction beyond the benchmark setting.

## Why this benchmark should be first in the public programme

Among the current candidate benchmarks, Casimir is the cleanest because:

- the observable is precise,
- the calculation is compact,
- the physical interpretation is load-bearing for RA,
- the current script already gives a reproducible witness,
- it connects directly to the “useful calculational tool” thesis.

By contrast, Mercury and weak-field lensing are probably even more persuasive in the long run for the GR-domain claim, but they still need a cleaner suite-primary sourcing derivation.

## Recommended next deliverable

A short benchmark note with exactly five parts:

1. Nature-facing statement of the observable,
2. RA prescription for the source,
3. closed-form stress-tensor evaluation,
4. one numerical benchmark at \(d=1\,\mu\text{m}\),
5. explicit open-scope paragraph on the remaining AQFT formal target.

## Recommended epistemic label

**CV/DR hybrid**

- CV for the numerical benchmark,
- DR for the conservation argument in the benchmark geometry,
- still conditional / open at the full AQFT modular-flow closure layer.

## Bottom line

Casimir is ready to serve as the first suite-primary benchmark note for the thesis that RA is not only conceptually viable, but computationally usable.
