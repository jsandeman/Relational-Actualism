# Relational Actualism (RA): Formal Verification Repository

**Relational Actualism** is a foundational physics framework built on a single ontological commitment: that on-shell actualization events — irreversible physical interactions that write permanent vertices into a growing causal graph — are the primitive reality from which spacetime, conservation laws, and complexity emerge.

From this foundation, a coherent predictive framework cascades across quantum mechanics, gravity and cosmology, biological complexity, quantum information theory, and the thermodynamics of cognition. The suite makes specific, falsifiable predictions — including a strict null result for gravity-mediated entanglement experiments (Bose-Marletto-Vedral protocol), a kinematic scaling limit for fault-tolerant quantum arrays, and a categorical prohibition on causally silent dark matter candidates.

The discrete-mathematical core has been formally verified in Lean 4/Mathlib. The foundational paper (RAQM) is under review at _Foundations of Physics_.

---

## 📄 Companion Papers (Zenodo)

| Paper | Title                                                               | DOI                                                                |
| ----- | ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| RAQM  | Relational Actualism and Quantum Mechanics                          | [10.5281/zenodo.19174380](https://doi.org/10.5281/zenodo.19174380) |
| RAGC  | Relational Actualism: Gravity and Cosmology                         | [10.5281/zenodo.19197999](https://doi.org/10.5281/zenodo.19197999) |
| EB    | The Engine of Becoming                                              | [10.5281/zenodo.19198120](https://doi.org/10.5281/zenodo.19198120) |
| RAHC  | Algorithmic Causal Dynamics                                         | [10.5281/zenodo.19198171](https://doi.org/10.5281/zenodo.19198171) |
| RACI  | Relational Actualism: Complexity and Intelligence                   | [10.5281/zenodo.19198224](https://doi.org/10.5281/zenodo.19198224) |
| RAQI  | Relational Actualism: Implications for Quantum Information          | [10.5281/zenodo.19198285](https://doi.org/10.5281/zenodo.19198285) |
| RADM  | Relational Actualism: Dark Matter as Actualization-Density Topology | [10.5281/zenodo.19198513](https://doi.org/10.5281/zenodo.19198513) |

All papers are also available in the `docs/` folder.

---

## 🗂️ Repository Structure

```
src/
  RA_AQFT/
    RA_AQFT_Proofs_v10.lean   — Density matrices, relative entropy, frame independence,
                                 Rindler stationarity (Unruh paradox resolution)
    RA_AQFT_Proofs_v2.lean    — Causal DAG, Graph Cut Theorem, Markov Blanket shielding,
                                 causal invariance of the quantum measure
  RA_Complexity/
    [Graph-theoretic proofs for biological emergence and agency]
data/
  DFT_Survey/
    thermo_batch_b3lyp.py     — B3LYP/6-311+G* thermochemistry pipeline
    assembly_mapper.py        — Assembly index computation
    [Raw DFT output files]
docs/
  [Companion paper PDFs and supplementary mathematical notes]
```

---

## ✅ Formal Verification Status

| Result                                  | File                      | Status                                                                                                                                                            |
| --------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local Ledger Condition                  | `RA_AQFT_Proofs_v2.lean`  | **Proved**                                                                                                                                                        |
| Graph Cut Theorem (RAGC Thm 2)          | `RA_AQFT_Proofs_v2.lean`  | **Proved** (no `sorry`)                                                                                                                                           |
| Markov Blanket Shielding                | `RA_AQFT_Proofs_v2.lean`  | **Proved**                                                                                                                                                        |
| Causal Invariance of Quantum Measure    | `RA_AQFT_Proofs_v2.lean`  | **Proved** (given `amplitude_locality` axiom)                                                                                                                     |
| Frame Independence (AQFT)               | `RA_AQFT_Proofs_v10.lean` | **Proved** (compiled theorem)                                                                                                                                     |
| Rindler Stationarity / Unruh Resolution | `RA_AQFT_Proofs_v10.lean` | **Proved** (compiled theorem)                                                                                                                                     |
| Amplitude Locality                      | `RA_AQFT_Proofs_v2.lean`  | **Axiom** — physically justified by QFT microcausality (Haag 1996) and Rideout-Sorkin Bell causality (2000); intrinsic discrete proof is the primary open problem |

Both Lean files compile with **zero errors and zero warnings** against Lean 4/Mathlib.

---

## 🔭 Key Predictions

- **BMV null result** — no gravity-mediated entanglement between superposed masses (EB)
- **WIMP prohibition** — no dark matter signal below the neutrino floor (RAGC/RADM)
- **Kinematic Coherence Bound** — N_max = η · p_th scaling limit for fault-tolerant quantum arrays (RAQI)
- **Actualization propagation velocity** — bounded by Lieb-Robinson speed (RAQM)
- **Causal depth selection pressure** — thermodynamic cost of cognition (RAHC)

---

## 🤝 Contributing and Open Problems

We actively welcome collaboration from experts in the following areas:

| Open Problem                                         | Target Expertise                                          |
| ---------------------------------------------------- | --------------------------------------------------------- |
| Intrinsic discrete proof of amplitude locality       | Algebraic QFT, causal set theory (Dowker, Sorkin, Henson) |
| Covariant RA field equations / Bianchi compatibility | Algebraic QFT, Hadamard renormalization                   |
| Continuum limit: type III₁ AQFT extension            | Tomita-Takesaki modular theory                            |
| Generative measure c_k derivation                    | QFT on causal set backgrounds                             |
| ξ coupling constant from first principles            | Modified gravity, causal set theory                       |
| Tully-Fisher scaling from covariant field equation   | Modified gravity                                          |

Please see `CONTRIBUTING.md` and the Issue Templates for how to engage. Pull requests are welcome.

---

## 📬 Contact

Joshua F. Sandeman — Independent Researcher, Salem, Oregon  
sansuikyo@gmail.com
