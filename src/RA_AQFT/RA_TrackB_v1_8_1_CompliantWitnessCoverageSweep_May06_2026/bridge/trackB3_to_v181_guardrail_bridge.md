# Track B.3 to v1.8.1 Guardrail Bridge

Track B.3 implements the v1.8.1 rule that fixed bins remain fixed across confound controls. The audit reports non-estimability rather than locally re-binning when joint `support_width × family_size` strata lack low/high contrasts.
