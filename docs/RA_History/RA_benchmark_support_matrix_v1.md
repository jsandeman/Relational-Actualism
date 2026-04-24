# RA Benchmark Support Matrix v1

This matrix reorders the benchmark agenda around your stated target: not only conceptual viability, but practical calculational usefulness.


| benchmark | current_support | paper_anchor | current_epistemic_state | main_gap | priority |
| --- | --- | --- | --- | --- | --- |
| Casimir effect | casimir_benchmark.py (runs) | Not a suite-primary paper benchmark yet; related to Paper I/III AQFT-vacuum bridge | promising runnable witness | RA-specific modular-flow commutativity / AQFT closure still open | 1 |
| Weak-field light deflection / lensing | Bullet Cluster discussion + bullet_cluster.py (runs) | Paper III §4.4 | qualitative/open | Need clean weak-field derivation before cluster-scale lensing can carry evidential weight | 2 |
| Mercury perihelion | No artifact found in current core bundle | None in current core snapshot | absent | No benchmark derivation or script yet | 3 |
| Galactic rotation curves | Paper III claim + ra_flat_rotation_curve.py (runs) | Paper III §4 | illustrative AR/CV mix | xi presently calibrated from target velocity rather than derived | 4 |
| Bullet Cluster | Paper III claim + bullet_cluster.py (runs) | Paper III §4.4 | framework-consistent, open proof | Need formal ρ_A derivation from P_act[T_{μν}] | 5 |
| DESI / apparent dark energy | Paper III phenomenology + ra_desi_verify.py (runs) | Paper III §§8–9 | useful phenomenology | t_trans and void-fraction evolution still underived | 6 |
| KCB / quantum-array hard wall | Paper I prediction row + Paper IV §7 | Paper I §11 / Paper IV §7 | unstable due to cross-paper mismatch | Formula mismatch and suite-primary provenance problem | 7 |
| Spin-bath collapse | Paper I prediction row + Paper IV §7 | Paper I §11 / Paper IV §7 | interesting but provenance-blurred | Current suite does not yet carry a clean self-contained derivation | 8 |


Recommended immediate order: Casimir → weak-field light deflection/lensing → Mercury perihelion → rotation curves/Bullet Cluster → KCB/spin-bath.