# RA-Native Bedrock Internal Split Docket v2

Some declarations inside otherwise bedrock files appear to belong to later interpretive, numerical, or bridge-facing layers. Split these declaration clusters during the line-by-line audit rather than treating the whole file as uniform.

## Suspect declarations inside bedrock files

| file                   | kind    | name                       |   line |
|:-----------------------|:--------|:---------------------------|-------:|
| RA_D1_Proofs.lean      | theorem | D1h_clebsch_gordan         |    998 |
| RA_D1_Proofs.lean      | theorem | D1h_hypercharge_ratio      |   1014 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_electron           |   1018 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_up_quark           |   1025 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_down_quark         |   1030 |
| RA_D1_Proofs.lean      | theorem | D1h_isospin_master         |   1038 |
| RA_D1_Proofs.lean      | theorem | relative_entropy_self_zero |   1123 |
| RA_D1_Proofs.lean      | theorem | vacuum_stress_energy_zero  |   1127 |
| RA_D1_Proofs.lean      | theorem | P_act_linear_zero          |   1136 |
| RA_D1_Proofs.lean      | theorem | P_act_conservation         |   1149 |
| RA_D1_Proofs.lean      | theorem | RA_field_equation_unique   |   1157 |
| RA_O14_Uniqueness.lean | theorem | alpha_inv_137              |    166 |
| RA_O14_Uniqueness.lean | theorem | alpha_s_weight             |    179 |

## Why this matters

Keeping the truly native statements at the front of the file stack makes the core proof story cleaner, and it stops later observational/cartographic declarations from contaminating the native frontier.
