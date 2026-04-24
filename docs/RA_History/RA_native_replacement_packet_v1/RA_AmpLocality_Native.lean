import RA_AmpLocality

/-!
# RA_AmpLocality_Native

Strict native wrapper for the active amplitude-locality bedrock.

This transitional file preserves the existing proofs while removing the
last imported quantum-facing labels from the active root. The final step
should be to move these names into the underlying source file itself.
-/

noncomputable section

abbrev extension_order_measure := quantum_measure

theorem extension_order_invariance := bdg_causal_invariance
