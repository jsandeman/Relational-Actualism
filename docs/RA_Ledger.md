# Relational Actualism — Technical Ledger
**April 2026** | *Status of every major claim in the RA programme*
---

## Lean-Verified (Bedrock)
*Machine-checked. Zero sorry tags. Epistemic status: certain.*
| ID | Claim | Evidence | Gap | Downstream |
|---|---|---|---|---|
| L01 | LLC: Σ_out(v)=Σ_in(v) at every DAG vertex | local_ledger_condition in RA_D1_Proofs.lean | — | **5** |
| L02 | GRAPH_CUT: LLC holds independently on each side of causal severance | graph_cut_theorem in RA_D1_Proofs.lean | — | 1 |
| L03 | MARKOV_BLANKET: subgraph shielding from exterior | markov_blanket in RA_D1_Proofs.lean | — | — |
| L04 | FRAME_IND: S(UρU†‖σ₀)=S(ρ‖σ₀) for U s.t. Uσ₀U†=σ₀ | frame_independence in RA_AQFT_Proofs_v10.lean | scope: Poincaré U only; Lean uses σ₀∝I | 2 |
| L05 | RINDLER_STAT: d/dt S(α_t(ρ_β)‖σ₀)=0 under modular flow α_t | rindler_stationarity in RA_AQFT_Proofs_v10.lean | — | 1 |
| L06 | RINDLER_THERMAL: ρ_β is valid density matrix (herm/pos/tr=1) | rindlerThermal in RA_AQFT_Proofs_v10.lean | — | — |
| L07 | CAUSAL_INV_COND: μ_σ(S)=μ_σ'(S) given amplitude_locality | causal_invariance in RA_AQFT_Proofs_v10.lean | conditional on O01 | **3** |
| L08 | ALPHA_EM: 144−7=137 (BDG depth-ratio fixed point) | alpha_inv_137 via norm_num in RA_D1_Proofs.lean | — | — |
| L09 | KOIDE: K=2/3 from BDG integers | koide_formula in RA_D1_Proofs.lean | — | — |
| L10 | CONFINEMENT: L=3 (gluon), L=4 (quark) from BDG topology | confinement_lengths in RA_D1_Proofs.lean | — | — |
| L11 | BDG_CLOSURE: 5 topology types, 124 extensions exhaust SM | universe_closure in RA_D1_Proofs.lean | — | 1 |
| L12 | QUBIT_FRAGILE: electrons/photons at minimum BDG score 1 | structural_fragility in RA_D1_Proofs.lean | — | 1 |

## Computation-Verified
*Public Python scripts. Reproducible by anyone. Status: certain given correct code.*
| ID | Claim | Evidence | Gap | Downstream |
|---|---|---|---|---|
| C01 | ALPHA_S: α_s(m_Z)=1/√72=0.11785 (PDG: 0.118, Δ=0.13%) | d3_alpha_s_proof.py; W=c₂·E[S_virt]·c₄=72 | — | — |
| C02 | P_ACC: P_acc(1)≈0.548 at μ=1 BDG Poisson-CSG | RASM Monte Carlo simulation | — | **3** |
| C03 | DELTA_S_STAR: ΔS*=−log P_acc(1)≈0.601 nats | direct computation from C02 | — | **4** |
| C04 | T_STAR: t*=(1/g)√(ΔS*/2)≈0.274/g (parameter-free) | spin-bath model + C03 | — | 1 |
| C05 | ERIDANUS: H(KBC void)≈75.9 km/s/Mpc from ρ_b proxy | void geometry + RAGC field equations | — | 1 |
| C06 | PROTON_MASS: m_p=√c₄·Λ_QCD to 0.08% | D1 analytic bridge; BDG Regge structure | — | — |
| C07 | ROPER: 290 MeV gap = two-pion loop (Kind 2 virtual process) | bare BDG 1150 MeV vs physical 1440 MeV | — | — |
| C08 | F_ZERO: W_other/W_baryon=17.32×α_s(m_p)=f₀=5.42 (Planck:5.416) | baryon-to-dark ratio from BDG path weights | — | — |
| N01 | α_EM⁻¹ = 137 (integer; Wyler gives fractional correction) | — | — | — |
| N02 | α_s(m_Z) = 1/√72 ≈ 0.11785 | — | — | — |
| N03 | ΔS* ≈ 0.601 nats | — | — | — |
| N04 | t* ≈ 0.274/g | — | — | — |
| N05 | ξ ≈ 0.601 l_P⁻² (provisional — O06) | — | — | — |
| N06 | H(Eridanus) ≈ 75.9 km/s/Mpc | — | — | — |
| N07 | m_p = √c₄ · Λ_QCD (0.08% accuracy) | — | — | — |
| N08 | f₀ = 5.42 (baryon-to-dark ratio; Planck: 5.416) | — | — | — |
| P02 | HUBBLE_GRADIENT: H₀ correlates linearly with ρ_b(LOS) | C05 for specific Eridanus case | NEAR-TERM: DESI data available | — |
| P04 | SPIN_BATH: t*≈0.274/g, ΔS*≈0.601 nats (parameter-free) | C03,C04 fully derived | TESTABLE: superconducting circuits | — |

## Derived
*All steps explicit in RA papers. Argument is complete but not machine-checked.*
| ID | Claim | Evidence | Gap | Downstream |
|---|---|---|---|---|
| D01 | LORENTZ_COV: actualization criterion is Lorentz-covariant | L04 for Poincaré U; σ₀ invariant under boosts | — | 1 |
| D02 | UNRUH_RES: Rindler obs detects no actualization in Mink vac | L05: per-step ΔS_n=0; threshold never crossed | detector coupling story (see O05) | 1 |
| D03 | VACUUM_SUPP: P_act projects out vacuum from metric source | on-shell condition → off-shell ΔS=0 → no sourcing | — | 2 |
| D04 | BIANCHI_FLAT: LLC → ∇_μG^μν≡0 in flat/weak-field limit | RACL proof sketch + Lovelock | — | 2 |
| D05 | FIVE_SCALE: μ=1 unifies QCD/galactic/fault-tol/ΔS*/Firewall | structural: same Erdős-Rényi transition each case | — | 1 |
| D06 | SM_SPECTRUM: 5 BDG types map to SM particle classes | L11 + topology matching | — | — |
| D07 | WEP_APPROX: | ρ_A−ρ_matter | /ρ_matter ~ τ_eq/t_cosm ≲ 10⁻⁴ | 2 |
| D08 | XI_EST: ξ≈0.601 l_P⁻² (provisional) | ξ∝⟨ΔS_vertex⟩/l_RA² with ⟨ΔS_vertex⟩=C03 | what is l_RA exactly? (see O06) | 1 |

## Argued
*Physically motivated. Key steps identified but not all explicit. Upgradeable to DR or LV.*
| ID | Claim | Evidence | Gap | Downstream |
|---|---|---|---|---|
| A01 | GR_UNIQUE: G_μν=8πG P_act[T_μν],Λ=0 unique by Lovelock | RACL; d=4 from L11; Bianchi from D04 | D04 needs curved-background extension (O03) | 2 |
| A02 | WIMP_PROHIB: WIMPs have A_RA≈0, no gravitational coupling | no EM/strong interactions → no actualization flux | O04 for formal WEP bound | 1 |
| A03 | BMV_NULL_MECH: superposed mass sources zero metric | unactualized → ρ_A=0 → ∇²Φ=0 → no phase difference | O07 for timescale criterion; O01 for full proof | 2 |
| A04 | CAUSAL_SEVER: event horizons are topological DAG disconnections | LLC undefined across severance, not violated | — | — |
| A05 | BORN_CONSIST: quantum measure consistent with Born rule | a(x)∝ψ(x) is constraint, not derivation | not claimable as derivation | — |
| A06 | CAUSAL_FIREWALL: μ=1 percolation as origin-of-life threshold | Erdős-Rényi transition at μ=1 | decoherence timescale τ_d (O08) | 2 |
| P01 | BMV_NULL: null gravity-mediated entanglement m~10⁻¹⁴kg τ~1s | A03 mechanism; O01 needed for full logical proof | NEAR-TERM: multiple groups pursuing | — |
| P03 | WIMP_FLOOR: no DM signal below neutrino floor (categorical) | A02; current XENONnT data consistent | ONGOING: LZ/XENONnT | — |
| P05 | KCB: N_max=η·p_th for fault-tolerant quantum arrays | Kinematic Coherence Bound from L12 | TESTABLE: near-future QEC experiments | — |
| P06 | CAUSAL_FIREWALL: biosignature universality | substrate-independence from μ=1 criterion | LONG-TERM: SETI observational | — |

## Open Problems (Hard Walls)
*Precisely scoped gaps. Each has a stated path to closure.*
| ID | Claim | Evidence | Gap | Downstream |
|---|---|---|---|---|
| O01 | AMP_LOC: a(v | S) depends only on S∩past(v) — intrinsic discrete | QFT justification (Pauli-Jordan) exists | 2 |
| O02 | CAUSAL_INV_FULL: L07 without amplitude_locality axiom | L07 is conditional version | close O01 first | — |
| O03 | BIANCHI_CURVED: LLC → Bianchi on curved background | type III₁ algebra; Tomita-Takesaki needed | modular theory collaborator (Dowker/Loll) | — |
| O04 | WEP_FORMAL: ρ_A→ρ_matter with explicit bounds vs. equilibrium | D07 gives order estimate only | equilibration dynamics derivation | — |
| O05 | UNRUH_DETECTOR: explicit coupling/measurement update story | D02 covers stationarity but not detector clicks | open quantum systems model | — |
| O06 | XI_DERIV: ξ from first principles (what is l_RA?) | D08 is estimate; need RA area element definition | connects to O03 | — |
| O07 | BMV_TIMESCALE: when is macroscopic COM "actualized"? | decoherence argument sketched | quantitative criterion consistent with interferometry | — |
| O08 | FIREWALL_TAU: decoherence timescale τ_d in Causal Firewall | μ=λτ_d ℓ³≥1 but τ_d not derived | — | — |
| O09 | COV_STEP4: stochastic update commutes for spacelike candidates | TS analogue for stochastic update | algebraic QFT collaborator | — |

## Predictions
*Falsifiable consequences. Sorted by experimental proximity.*

---

## Priority Closure Map
*Open problems sorted by downstream impact. Close these first.*

**O01** (2 downstream): AMP_LOC: a(v
  → Gap: QFT justification (Pauli-Jordan) exists

**O02** (0 downstream): CAUSAL_INV_FULL: L07 without amplitude_locality axiom
  → Gap: close O01 first

**O03** (0 downstream): BIANCHI_CURVED: LLC → Bianchi on curved background
  → Gap: modular theory collaborator (Dowker/Loll)

**O04** (0 downstream): WEP_FORMAL: ρ_A→ρ_matter with explicit bounds vs. equilibrium
  → Gap: equilibration dynamics derivation

**O05** (0 downstream): UNRUH_DETECTOR: explicit coupling/measurement update story
  → Gap: open quantum systems model

**O06** (0 downstream): XI_DERIV: ξ from first principles (what is l_RA?)
  → Gap: connects to O03

**O07** (0 downstream): BMV_TIMESCALE: when is macroscopic COM "actualized"?
  → Gap: quantitative criterion consistent with interferometry

**O08** (0 downstream): FIREWALL_TAU: decoherence timescale τ_d in Causal Firewall
  → Gap: —

**O09** (0 downstream): COV_STEP4: stochastic update commutes for spacelike candidates
  → Gap: algebraic QFT collaborator


## Integrity Checks
*Known scope caveats and issues to watch.*

- **IC01**: L04 scope: theorem uses σ₀∝I in finite-dim truncation; physical claim needs Poincaré invariance of Minkowski vacuum (documented in RAEB v3+)
- **IC02**: D02 gap: modular flow stationarity ≠ no detector clicks unless detector coupling is incorporated (O05)
- **IC03**: D08 provisional: l_RA undefined; ξ estimate assumes l_RA=l_P (not derived)
- **IC04**: A01 uses d=4 from L11 (imported from RATM/RASM, not proved in RAGC/RAEB)
- **IC05**: A03 uses "unactualized → ρ_A=0" which requires O07 for macroscopic COM case
- **IC06**: C01 (α_s result): UV fixed point; IR fixed point α_s=1/3 also proved (confinement)
- **IC07**: L07 conditional: causal invariance in RAEB abstract must not be stated as unconditional
