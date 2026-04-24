# RA Paper I AQFT Patch Summary v1

This patch makes four targeted AQFT edits.

1. Renames the theorem heading from "Lean-verified in finite-dimensional scope" to "conditional Lean theorem in finite-dimensional scope".

2. Rewrites the explanatory paragraph below the theorem so that:
   - the single live CFC lemma is described accurately,
   - the failed LQI-to-current-Mathlib port is acknowledged,
   - the vacuum-invariance axiom is separated from the library closure issue,
   - the open local-algebra/modular-flow AQFT layer is named explicitly.

3. Adds a scope sentence clarifying that the load-bearing claim is stationarity / no-threshold-crossing, not finiteness of the full continuum relative entropy in every representation.

4. Rewrites the Lean-status footnote and the status-box wording to remove the phrase "trivially closable" and to distinguish the narrow CFC target from the broader AQFT frontier.
