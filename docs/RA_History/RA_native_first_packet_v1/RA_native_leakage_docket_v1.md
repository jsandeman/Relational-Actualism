# RA-Native Leakage Docket v1

Static text-pattern scan over the extracted core proofs/scripts bundle. This is a triage tool, not a final verdict; false positives are possible.

## Highest-risk files

| file                           |   total_hits |   forbidden_hits |   bridge_hits |   legacy_hits | triage_action           | triage_note                                                                          |
|:-------------------------------|-------------:|-----------------:|--------------:|--------------:|:------------------------|:-------------------------------------------------------------------------------------|
| RA_D1_Proofs.lean              |           21 |               14 |             5 |             2 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| d1_BDG_string_tension.py       |           14 |               14 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| D1_BDG_MCMC_simulation.py      |           13 |               13 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| d3i_complete.py                |           12 |               12 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| daughter_universe.py           |           12 |               12 |             0 |             0 | manual-audit            | Nature-facing target, but current script shows bridge/theory leakage.                |
| sigma_analysis.py              |           21 |                9 |             0 |            12 | manual-audit            | Potential native content, but labels/categories appear imported.                     |
| bdg_multicoupling.py           |            8 |                8 |             0 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| d3_alpha_s_proof.py            |            8 |                8 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| qcd_running_proof.py           |            7 |                7 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| d2_two_phases.py               |           14 |                6 |             8 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| hard_wall_4_summary.py         |            6 |                6 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| pathwise_exit.py               |            9 |                5 |             0 |             4 | manual-audit            | Potential native content, but labels/categories appear imported.                     |
| mu_derivation.py               |            5 |                5 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| sigma_table.py                 |            6 |                4 |             0 |             2 | manual-audit            | Potential native content, but labels/categories appear imported.                     |
| vwyler_proof.py                |            3 |                3 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| RA_Proofs_Lean4.lean           |            6 |                2 |             4 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| rho_native.py                  |            4 |                2 |             2 |             0 | promising-after-cleanup | Promising native direction; remove external-theory inputs and imported labels first. |
| RA_RASM_Verification.py        |            2 |                2 |             0 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| d3_alpha_s_BDG.py              |            2 |                2 |             0 |             0 | quarantine              | Explicit forbidden theory-object dependence.                                         |
| mu_int_derive.py               |            2 |                2 |             0 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| RA_Session_Log_Apr10.md        |            5 |                1 |             4 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| branching_volume.py            |            3 |                1 |             1 |             1 | manual-audit            | Potential native content, but labels/categories appear imported.                     |
| RA_BDG_Simulation.py           |            2 |                1 |             0 |             1 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| f0_enumeration.py              |            1 |                1 |             0 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| n_eff_alternative.py           |            1 |                1 |             0 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| rindler_relative_entropy.py    |           97 |                0 |            97 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| casimir_benchmark.py           |           32 |                0 |            32 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| ra_calibration.py              |           25 |                0 |            25 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| RA_AQFT_Proofs_v10.lean        |           21 |                0 |            21 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| born_rule_derivation.py        |           11 |                0 |            11 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| berry_bridge.py                |           10 |                0 |            10 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| RA_PACT_conservation_lean.lean |            6 |                0 |             6 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| bullet_cluster.py              |            6 |                0 |             6 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| RA_AQFT_Proofs.lean            |            5 |                0 |             5 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| RA_CFC_Port.lean               |            4 |                0 |             4 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| berry_transfer.py              |            3 |                0 |             3 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| cross_dimensional_exclusion.py |            3 |                0 |             3 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| RA_AQFT_CFC_Patch.lean         |            2 |                0 |             2 |             0 | archive-bridge          | Bridge-only material, not on native critical path.                                   |
| RA_AmpLocality.lean            |            2 |                0 |             2 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |
| lakefile.lean                  |            2 |                0 |             2 |             0 | manual-audit            | Inspect provenance and targets before reuse.                                         |

## Representative flagged snippets

| file                           |   line | group                    | snippet                                                                                  |
|:-------------------------------|-------:|:-------------------------|:-----------------------------------------------------------------------------------------|
| RA_AQFT_CFC_Patch.lean         |     25 | bridge_gr_qft            | -- Unitary conjugation Ad_U : M ↦ UMU† is a *-automorphism.                              |
| RA_AQFT_CFC_Patch.lean         |     27 | bridge_gr_qft            | -- unitary matrices are a special case (isometry with equal dimensions).                 |
| RA_AQFT_Proofs.lean            |      5 | bridge_gr_qft            | ## Relational Actualism — AQFT Stage 2                                                   |
| RA_AQFT_Proofs.lean            |     73 | bridge_gr_qft            | -- 3. RINDLER THERMAL STATE                                                              |
| RA_AQFT_Proofs.lean            |    112 | bridge_gr_qft            | -- 4. UNITARY MATRICES                                                                   |
| RA_AQFT_Proofs_v10.lean        |      4 | bridge_gr_qft            | # RA_AQFT_Proofs.lean  (v10.0 — sorry-free modulo QFT axiom)                             |
| RA_AQFT_Proofs_v10.lean        |      5 | bridge_gr_qft            | ## Relational Actualism — AQFT Stage 2                                                   |
| RA_AQFT_Proofs_v10.lean        |     26 | bridge_gr_qft            | AXIOM (1 — QFT input, not a Lean gap):                                                   |
| RA_AmpLocality.lean            |    126 | bridge_gr_qft            | action increment, with no appeal to the QFT continuum limit. -/                          |
| RA_AmpLocality.lean            |    199 | bridge_gr_qft            | No appeal to QFT continuum limit is required.                                            |
| RA_CFC_Port.lean               |     82 | bridge_gr_qft            | /-- An isometry is a matrix `A` such that `AᴴA = 1`. Compare with a unitary,             |
| RA_CFC_Port.lean               |     85 | bridge_gr_qft            | therefore unitary; this does not work out so well here, since a `Matrix m n R`           |
| RA_CFC_Port.lean               |     86 | bridge_gr_qft            | can be a two-sided isometry but cannot be a `unitary` since the rows and columns         |
| RA_D1_Proofs.lean              |   1092 | bridge_gr_qft            | ### Connection to Lovelock uniqueness                                                    |
| RA_D1_Proofs.lean              |   1094 | bridge_gr_qft            | With ∇_μ(P_act T^μν) = 0 proved, Lovelock's theorem (1971) applies:                      |
| RA_D1_Proofs.lean              |   1105 | bridge_gr_qft            | — Lovelock uniqueness (1971)                                                             |
| RA_PACT_conservation_lean.lean |    126 | bridge_gr_qft            | -- This is the key condition Lovelock's theorem requires.                                |
| RA_PACT_conservation_lean.lean |    148 | bridge_gr_qft            | COROLLARY (Lovelock + P_act conservation → unique field equation):                       |
| RA_PACT_conservation_lean.lean |    153 | bridge_gr_qft            | (3) Lovelock: unique divergence-free symmetric rank-2 local tensor                       |
| RA_Proofs_Lean4.lean           |    398 | bridge_gr_qft            | -- the light cone; QFT microcausality: [φ(x),φ(y)]=0 for spacelike                       |
| RA_Proofs_Lean4.lean           |    495 | bridge_gr_qft            | --   Physical justification: QFT microcausality (Haag 1996),                             |
| RA_Proofs_Lean4.lean           |    520 | bridge_gr_qft            | -- Vacuum Energy Suppression          | AXIOM (requires QFT library)                     |
| RA_Session_Log_Apr10.md        |    130 | bridge_gr_qft            | 4. **GR bridge** — RACL §5 + §5.1                                                        |
| RA_Session_Log_Apr10.md        |    211 | bridge_gr_qft            | ### Note 5: GR Bridge (PP6)                                                              |
| RA_Session_Log_Apr10.md        |    214 | bridge_gr_qft            | - §2: Route 1 (Lovelock chain) — 7 steps, each with explicit status                      |
| berry_bridge.py                |     17 | bridge_gr_qft            | (This is forced by having 2 sectors with unitary transfer.)                              |
| berry_bridge.py                |     20 | bridge_gr_qft            | (This is a property of 2×2 unitary matrices with det=1.)                                 |
| berry_bridge.py                |    122 | bridge_gr_qft            | 3. THE KEY THEOREM (pure algebra, no QFT)                                                |
| berry_final.py                 |    350 | bridge_gr_qft            | Both are RA-native. Both are discrete. Neither imports QFT.                              |
| berry_theorems.py              |    110 | bridge_gr_qft            | F_inv = np.conj(F.T)  # Unitary DFT                                                      |
| berry_transfer.py              |     75 | bridge_gr_qft            | The transfer matrices are UNITARY ROTATIONS in the 3D sector                             |
| berry_transfer.py              |    107 | bridge_gr_qft            | Unitary transfer matrix: fraction f of amplitude from sector                             |
| berry_transfer.py              |    170 | bridge_gr_qft            | print(f"  |det(W)| = {abs(det_W):.6f} (should = 1 for unitary)")                         |
| born_rule_derivation.py        |     44 | bridge_gr_qft            | In QFT, the interaction Hamiltonian is local:                                            |
| born_rule_derivation.py        |     85 | bridge_gr_qft            | (i)  Locality of the QFT interaction Hamiltonian                                         |
| born_rule_derivation.py        |    212 | bridge_gr_qft            | (i)  They evolve unitarily under the Schrödinger equation — no                           |
| branching_volume.py            |    335 | bridge_gr_qft            | This is not imported from QFT. It is computed from:                                      |
| bullet_cluster.py              |    239 | bridge_gr_qft            | → this is what standard GR mass-energy is tracking!                                      |
| bullet_cluster.py              |    240 | bridge_gr_qft            | → recovers GR in the limit of uniformly interacting matter                               |
| bullet_cluster.py              |    244 | bridge_gr_qft            | → zero when λ is uniform (standard GR regime)                                            |
| casimir_benchmark.py           |      3 | bridge_gr_qft            | Relational Actualism — D3 Bianchi Compatibility and D2 Unruh Benchmark                   |
| casimir_benchmark.py           |     13 | bridge_gr_qft            | 5. The modified Einstein equation source is well-defined and consistent.                 |
| casimir_benchmark.py           |     14 | bridge_gr_qft            | 6. The Unruh frame-dependence objection is resolved by the stationarity                  |
| cross_dimensional_exclusion.py |    191 | bridge_gr_qft            | to □ in the continuum limit. No valid Einstein equation emerges.                         |
| cross_dimensional_exclusion.py |    221 | bridge_gr_qft            | C3 rules out d=2,3,5,6,7,8 (Σc_k ≠ 0 → no valid Einstein equation)                       |
| cross_dimensional_exclusion.py |    235 | bridge_gr_qft            | - produces a valid Einstein equation (C3)                                                |
| d2_two_phases.py               |      3 | bridge_gr_qft            | Confirms the GR/particle phase transition at mu=1 and                                    |
| d2_two_phases.py               |     54 | bridge_gr_qft            | print("Other = field/composite regime: GR description appropriate.")                     |
| d2_two_phases.py               |     57 | bridge_gr_qft            | f"{'Frac elem':>10}  {'Frac GR':>10}  {'Phase'}")                                        |
| lakefile.lean                  |     22 | bridge_gr_qft            | -- AQFT: frame independence, Rindler, CPTP (L04–L07)                                     |
| lakefile.lean                  |     22 | bridge_gr_qft            | -- AQFT: frame independence, Rindler, CPTP (L04–L07)                                     |
| ra_calibration.py              |    145 | bridge_gr_qft            | GRAVITY (the Einstein equations derived from BDG),                                       |
| ra_calibration.py              |    150 | bridge_gr_qft            | GR dynamics (BDG uniqueness → Einstein-Hilbert).                                         |
| ra_calibration.py              |    150 | bridge_gr_qft            | GR dynamics (BDG uniqueness → Einstein-Hilbert).                                         |
| ra_early_bh.py                 |    261 | bridge_gr_qft            | # Standard spherical collapse: δ_c = 1.686 (derived from GR)                             |
| rho_native.py                  |    211 | bridge_gr_qft            | print("   NOTHING is imported from QFT coupling constants.")                             |
| rho_native.py                  |    464 | bridge_gr_qft            | IF μ IS FITTED, it replaces the multiple QFT parameters                                  |
| rindler_relative_entropy.py    |      3 | bridge_gr_qft            | Relational Actualism — AQFT Proof Stage 1                                                |
| rindler_relative_entropy.py    |      5 | bridge_gr_qft            | Computes the relative entropy S(ρ || σ₀) for states in the Rindler wedge                 |
| rindler_relative_entropy.py    |     10 | bridge_gr_qft            | 3. Off-shell regime: virtual exchanges do not constitute QFT states                      |
| t1_forecast_deliverables.py    |    129 | bridge_gr_qft            | print("curvature treatment. The true answer requires inhomogeneous-GR distance")         |
| t1_forecast_deliverables.py    |    258 | bridge_gr_qft            | yet provide and which requires either the Wiltshire/timescape machinery                  |
| D1_BDG_MCMC_simulation.py      |     13 | forbidden_theory_objects | - G_F (tree level): G_F/√2 = 1.163e-5 GeV⁻² (PDG: 1.166e-5, 0.3% error)                  |
| D1_BDG_MCMC_simulation.py      |     14 | forbidden_theory_objects | - Remaining open: absolute Λ_QCD from BDG without external QCD input                     |
| D1_BDG_MCMC_simulation.py      |     29 | forbidden_theory_objects | Lambda_QCD = 0.332       # GeV (PDG Λ_QCD^{MS-bar}, n_f=3)                               |
| RA_BDG_Simulation.py           |    149 | forbidden_theory_objects | print("  Q_N3 ∈ {0,1,2,...} ↔  weak isospin related")                                    |
| RA_RASM_Verification.py        |     54 | forbidden_theory_objects | print("  [alpha_EM and alpha_s are external inputs, not BDG-derived]")                   |
| RA_RASM_Verification.py        |    155 | forbidden_theory_objects | print("  HYBRID conjectures: verified numerically against PDG 2022.")                    |
| bdg_multicoupling.py           |     57 | forbidden_theory_objects | alpha_s = 0.118                                                                          |
| bdg_multicoupling.py           |     61 | forbidden_theory_objects | Lambda_QCD = 200  # MeV                                                                  |
| bdg_multicoupling.py           |     68 | forbidden_theory_objects | lam2 = alpha_em * (mass_MeV / Lambda_QCD) / 2  # EM rate                                 |
| branching_volume.py            |     72 | forbidden_theory_objects | # G-parity (for non-strange mesons)                                                      |
| d1_BDG_string_tension.py       |      5 | forbidden_theory_objects | - sigma_BDG = Lambda_QCD^2  (BDG string tension, one Λ² per gluon mode)                  |
| d1_BDG_string_tension.py       |      6 | forbidden_theory_objects | - m_p = sqrt(c4) * Lambda_QCD = sqrt(8) * Lambda_QCD  [0.08% from PDG]                   |
| d1_BDG_string_tension.py       |      6 | forbidden_theory_objects | - m_p = sqrt(c4) * Lambda_QCD = sqrt(8) * Lambda_QCD  [0.08% from PDG]                   |
| d3_alpha_s_BDG.py              |     15 | forbidden_theory_objects | print(f"α_EM (Wyler): 1/{1/alpha_EM_Wyler:.3f}  PDG: 1/137.036  (0.0001%)")              |
| d3_alpha_s_BDG.py              |     16 | forbidden_theory_objects | print(f"α_s (BDG):    {alpha_s_BDG:.6f}  PDG: 0.11800    (0.13%)")                       |
| d3_alpha_s_proof.py            |      2 | forbidden_theory_objects | COMPLETE PROOF: alpha_s(m_Z) = 1/sqrt(c2*c4) = 1/sqrt(72)                                |
| d3_alpha_s_proof.py            |      5 | forbidden_theory_objects | alpha_s(m_Z) = 1/sqrt(c2 * c4) = 1/sqrt(9*8) = 1/sqrt(72)                                |
| d3_alpha_s_proof.py            |     13 | forbidden_theory_objects | Step 3:  alpha_s = 1/K = 1/sqrt(72). QED.                                                |
| d3i_complete.py                |      6 | forbidden_theory_objects | 2. UV fixed point: alpha_s(mu->inf) = 1/sqrt(72) = 0.11785  [proved]                     |
| d3i_complete.py                |      7 | forbidden_theory_objects | 3. IR fixed point: alpha_s(mu->0)   = 1/3         = 0.33333  [proved]                    |
| d3i_complete.py                |      8 | forbidden_theory_objects | 4. Q_eff = L * W_baryon * Lambda_QCD = 4 * (3/2) * Lambda_QCD  [derived]                 |
| daughter_universe.py           |    131 | forbidden_theory_objects | # At condensation, the physical density is the QCD scale:                                |
| daughter_universe.py           |    134 | forbidden_theory_objects | Lambda_QCD = 0.2e9 * 1.602e-19 / c  # 0.2 GeV in kg⋅m/s...                               |
| daughter_universe.py           |    150 | forbidden_theory_objects | # From initial (Planck density) to condensation (QCD density):                           |
| f0_enumeration.py              |    208 | forbidden_theory_objects | print("parameters). The α_s(2 m_p) = 0.312 uses standard SM QCD RG")                     |
| hard_wall_4_summary.py         |     37 | forbidden_theory_objects | (the "thermal QCD excess" above the rest-mass contribution)                              |
| hard_wall_4_summary.py         |     39 | forbidden_theory_objects | Whether the QGP phase deposits exactly this ratio is a QCD physics                       |
| hard_wall_4_summary.py         |     40 | forbidden_theory_objects | question that connects RA to lattice QCD.                                                |
| mu_derivation.py               |     12 | forbidden_theory_objects | individual motif — it's a property of the QCD-scale graph.                               |
| mu_derivation.py               |     46 | forbidden_theory_objects | QCD-scale graph.                                                                         |
| mu_derivation.py               |    167 | forbidden_theory_objects | Physical meaning: the internal graph density at the QCD                                  |
| mu_int_derive.py               |     32 | forbidden_theory_objects | Lambda_QCD = 200  # MeV                                                                  |
| mu_int_derive.py               |    155 | forbidden_theory_objects | log_ratio.append(np.log(m / Lambda_QCD))                                                 |
| n_eff_alternative.py           |     16 | forbidden_theory_objects | scale, consistent with string-like confinement pictures in QCD.                          |
| pathwise_exit.py               |     14 | forbidden_theory_objects | - σ labels: {isospin I, G-parity G, strangeness S, flavor content}                       |
| pathwise_exit.py               |     14 | forbidden_theory_objects | - σ labels: {isospin I, G-parity G, strangeness S, flavor content}                       |
| pathwise_exit.py               |     80 | forbidden_theory_objects | - Isospin: must be accessible (|I_parent - I_daughter| ≤ ΔI ≤ I_parent + I_daughter)     |
| qcd_running_proof.py           |      2 | forbidden_theory_objects | QCD running proof for the f0 = 17.32 × alpha_s(2m_p) = 5.42 derivation.                  |
| qcd_running_proof.py           |      2 | forbidden_theory_objects | QCD running proof for the f0 = 17.32 × alpha_s(2m_p) = 5.42 derivation.                  |
| qcd_running_proof.py           |      4 | forbidden_theory_objects | Key result: alpha_s(2m_p = 1877 MeV) = 0.312 +/- 0.004                                   |
| rho_native.py                  |    308 | forbidden_theory_objects | # ρ_graph ~ Λ_QCD^4 (the QCD vacuum density)                                             |
| sigma_analysis.py              |     62 | forbidden_theory_objects | # ── Type III: G-parity forces 3-body ──                                                 |
| sigma_analysis.py              |     71 | forbidden_theory_objects | ('η\'(958)',[2,1,0,0],3, 958, 3.3e-21, 'ηππ/ργ',3,'V',  'SU(3) anomaly, U(1)_A mixing'), |
| sigma_analysis.py              |    176 | forbidden_theory_objects | TYPE III (G-parity multi-step):                                                          |
| sigma_table.py                 |     87 | forbidden_theory_objects | # G-parity conservation (only for non-strange, I-definite states)                        |
| sigma_table.py                 |     93 | forbidden_theory_objects | # Isospin compatibility (daughter I must be reachable)                                   |
| sigma_table.py                 |    344 | forbidden_theory_objects | TYPE III (G-parity multi-step):                                                          |
| vwyler_proof.py                |     11 | forbidden_theory_objects | print(f"alpha_s    = 1/sqrt({T}) = {alpha_s_mZ:.6f}")                                    |
| vwyler_proof.py                |     12 | forbidden_theory_objects | print(f"PDG alpha_s = 0.118000  (error {abs(alpha_s_mZ-0.118)/0.118*100:.2f}%)")         |
| vwyler_proof.py                |     12 | forbidden_theory_objects | print(f"PDG alpha_s = 0.118000  (error {abs(alpha_s_mZ-0.118)/0.118*100:.2f}%)")         |
| RA_BDG_Simulation.py           |    149 | legacy_labels            | print("  Q_N3 ∈ {0,1,2,...} ↔  weak isospin related")                                    |
| branching_volume.py            |     68 | legacy_labels            | # Strangeness (strong decays)                                                            |