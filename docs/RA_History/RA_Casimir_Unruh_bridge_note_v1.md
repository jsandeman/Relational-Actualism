# RA Casimir and Unruh Bridge Note v1

## Summary

This note consolidates the current benchmark status of the AQFT side of the suite.

## 1. Casimir benchmark

### What is already strong

`casimir_benchmark.py` reproduces the standard Casimir stress tensor for parallel conducting plates and verifies the standard numerical pressure at `d = 1 μm`:

- energy density: `u = -4.3340e-04 J/m^3`
- normal pressure: `p_z = -1.3002e-03 Pa`

The script also checks the static bulk-conservation story and presents the RA subtraction prescription

`<T^μν_RA> = <T^μν_ren>[g,Φ] - <T^μν_ren>[g,|0⟩]`

as the reason the absolute vacuum term is removed while the boundary-condition-dependent Casimir difference remains.

### Correct status label

This should be presented as:

- **CV / bridge benchmark**
- strong evidence that the RA vacuum-suppression prescription preserves a known observable
- not yet a discrete derivation of Casimir from BDG graph growth

The script is therefore best used to support the claim:

> RA does not erase Casimir physics when suppressing absolute vacuum energy.

not the stronger claim:

> RA has already derived Casimir from discrete first principles.

## 2. Unruh / Rindler stationarity

### What is already strong

In `RA_AQFT_Proofs_v10.lean`, the chain

- `relEnt_unitary_invariant`
- `frame_independence`
- `rindler_stationarity`

is compact and meaningful.

The support script `rindler_relative_entropy.py` also verifies unitary invariance numerically to machine precision and is very clear about what is still open.

### Correct status label

This should be presented as:

- **LV finite-dimensional (conditional)**
- one CFC lemma still open
- vacuum Lorentz/Poincaré invariance still imported as a QFT axiom
- full modular/local-algebra closure still open

### The key interpretive point

The current theorem supports the claim:

> the Rindler bath is stationary and therefore non-actualizing in the finite-dimensional translated setting

It does **not** yet support the stronger claim:

> the entire local-algebra AQFT actualization programme is formally closed.

## 3. The clean benchmark wording

### Safe wording

- Casimir: **RA preserves the measured Casimir difference while suppressing the absolute vacuum reference.**
- Unruh: **RA has a conditional finite-dimensional stationarity theorem supporting the claim that the Rindler bath is not itself an actualization event.**
- AQFT frontier: **full local-algebra `P_act` / modular-flow closure remains open.**

### Unsafe wording to avoid

- "Casimir is fully derived from RA"
- "AQFT is closed"
- "the CFC gap is trivial"
- "Rindler stationarity is an unconditional full-AQFT theorem"

## 4. Best next move

The next benchmark/publication move on the AQFT side should be a short suite-primary note with exactly two claims:

1. the Casimir benchmark preserves the observed force under the RA subtraction prescription;
2. the Unruh theorem is finite-dimensional and conditional, with the open local-algebra layer stated separately.

That would make the AQFT side look much more coherent and much less overstated.
