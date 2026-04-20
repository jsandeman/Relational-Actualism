# RA-Native Severance Entropy Observable

*Joshua F. Sandeman — Independent Researcher, Salem, Oregon*
*Formal note, April 2026 — supersedes earlier ambiguous formulations*

---

## 1. The observable

**Definition 1 (Cross-severance link set).** Let $G=(V,\prec)$ be a causal graph with irreducible relation ("link") set $L(G)\subseteq V\times V$. A *severance* $\Sigma$ is a partition $V=V_A\sqcup V_B$. The cross-severance link set is
$$L_\Sigma=\{(u,v)\in L(G):\ u\in V_A,\ v\in V_B\}.$$

**Definition 2 (RA-native severance entropy).**
$$\boxed{S_{\mathrm{RA}}(\Sigma)=|L_\Sigma|=N_{\mathrm{sev}}(\Sigma).}$$

The entropy counts *irreducible future-directed causal links blocked by the severance* — minimal causal channels removed, not boundary vertex counts and not order relations that factor through intermediate vertices.

**Definition 3 (Severance out-degree).** For a boundary vertex $u\in\partial V_A$,
$$d^{\Sigma}_{\mathrm{out}}(u)=|\{v\in V_B:(u,v)\in L_\Sigma\}|.$$

Then
$$S_{\mathrm{RA}}(\Sigma)=\sum_{u\in\partial V_A}d^{\Sigma}_{\mathrm{out}}(u)=\langle d^{\Sigma}_{\mathrm{out}}\rangle\cdot N_\partial,$$
where $N_\partial=|\partial V_A|$ and $\langle d^{\Sigma}_{\mathrm{out}}\rangle$ is the mean severed out-degree across the boundary.

---

## 2. Why this observable (three propositions)

These three propositions were contributed by ChatGPT (GPT-4o), 2026-04-12, and justify the choice of $|L_\Sigma|$ over competing candidates (boundary-vertex count, total cross-severance order relations, or a metric-import from Bekenstein–Hawking).

**Proposition 1 (Additivity).** If $\Sigma_1$ and $\Sigma_2$ are disjoint severances of $G$ (no shared vertices in the boundary, no shared severed links), then
$$S_{\mathrm{RA}}(\Sigma_1\sqcup\Sigma_2)=S_{\mathrm{RA}}(\Sigma_1)+S_{\mathrm{RA}}(\Sigma_2).$$
*Proof sketch.* The severed link set is a union over disjoint index sets; $|A\sqcup B|=|A|+|B|$. $\square$

This is the correct behavior for an extensive entropy count. Any non-additive candidate (e.g., a log-like quantity applied to link count) would fail this basic requirement.

**Proposition 2 (Sensitivity).** There exist severances $\Sigma_1,\Sigma_2$ of distinct causal graphs with $N_\partial(\Sigma_1)=N_\partial(\Sigma_2)$ but $S_{\mathrm{RA}}(\Sigma_1)\neq S_{\mathrm{RA}}(\Sigma_2)$.

*Proof sketch.* Boundary-vertex count is too coarse: two graphs with the same boundary $V$-set can have different link structures between $V_A$-boundary and $V_B$-boundary. A boundary vertex may have 1 severed out-link in one configuration and 10 in another. $\square$

This is why $N_\partial$ alone is the wrong observable — it loses information. $N_\partial$ is a *proxy* for $S_{\mathrm{RA}}$ in the sense of the decomposition above, valid only when $\langle d^{\Sigma}_{\mathrm{out}}\rangle$ is approximately constant across the severance class.

**Proposition 3 (Transitive-overcount avoidance).** Let $R_\Sigma\supseteq L_\Sigma$ be the full set of cross-severance order relations (not just irreducible links). Then $|R_\Sigma|$ overcounts the independent causal channels blocked by $\Sigma$, because any non-link relation $(u,w)\in R_\Sigma\setminus L_\Sigma$ factors as $u\prec v\prec w$ through some intermediate $v$ and is therefore not independent of the links $(u,v)$ and $(v,w)$ already in $L_\Sigma$.

*Proof sketch.* If $u\prec w$ is a relation but not a link, there exists $v\in V$ with $u\prec v\prec w$. If both $(u,v)$ and $(v,w)$ are in $L_\Sigma$ (i.e., $v$ is in the "wrong side" of the severance), then $(u,w)$ is a derived relation, not an additional channel. Counting it would double-count the information flow already accounted for by the two links. $\square$

The irreducible-link observable is therefore the unique additivity-compatible, sensitivity-correct, non-overcounting choice.

---

## 3. Finiteness and refinement invariance

**Open target 1A** (stated by ChatGPT 2026-04-12, currently open): Prove that for any severance $\Sigma$ of a locally finite causal graph,

(a) $S_{\mathrm{RA}}(\Sigma)<\infty$, and
(b) $S_{\mathrm{RA}}(\Sigma)$ is invariant under internal refinement of $V_A$ or $V_B$ that leaves $L_\Sigma$ unchanged.

Part (a) holds trivially for finite severances and almost-trivially for locally finite graphs with finite boundary; the honest content is the locally-finite-with-infinite-components case. Part (b) is the more interesting result: it says $S_{\mathrm{RA}}$ is a property of the severance *surface*, not of the bulk description on either side, which is the right behavior for a horizon entropy.

**Status:** open. Formal proof has not been written.

---

## 4. Boundary-law structure

The locality of $\langle d^{\Sigma}_{\mathrm{out}}\rangle$ — i.e., the statement that the mean severed out-degree converges to a graph-dimension-dependent constant as the severance grows — is what makes $S_{\mathrm{RA}}\propto N_\partial$ a boundary law rather than a volume law.

**Numerical evidence (`severed_outdegree.py`):** In Poisson-CSG simulations in $d=2$, $\langle d^{\Sigma}_{\mathrm{out}}\rangle$ converges toward a constant $\sim 2.5$–$2.75$ as graph size $N$ grows (with decreasing sample variance). The same pattern is observed for $d=3$ at accessible sample sizes. This is CV-level evidence for the locality claim; a formal proof in general $d$ would complete the boundary law.

The statement then is:
$$S_{\mathrm{RA}}(\Sigma) = \langle d^{\Sigma}_{\mathrm{out}}\rangle_{d}\cdot N_\partial(\Sigma),$$
with $\langle d^{\Sigma}_{\mathrm{out}}\rangle_d$ a dimension-dependent local constant of the Poisson-CSG.

---

## 5. Relation to Bekenstein–Hawking (open bridge)

The conjectured continuum translation is
$$S_{\mathrm{RA}}(\Sigma)\approx\kappa_{\mathrm{BDG}}\cdot A(\Sigma),$$
where $A(\Sigma)$ is the continuum area of the severance surface and $\kappa_{\mathrm{BDG}}$ is a normalization constant from the BDG-to-metric dictionary. Matching the Bekenstein–Hawking formula $S_{\mathrm{BH}}=A/(4\ell_P^2)$ would require $\kappa_{\mathrm{BDG}}=1/(4\ell_P^2)$.

**Status:** this is a *conjecture*, not an established result. Two honest caveats:

**Caveat 1.** The naive identification "one severed link per Planck-area patch of the horizon, each contributing $\Delta S^*$ nats of entropy" gives
$$S = N_\partial\cdot\Delta S^* = (A/\ell_P^2)\cdot\Delta S^*,$$
which matches $S_{\mathrm{BH}}=A/(4\ell_P^2)$ only if $\Delta S^*=1/4$. But the canonical D4U02 value is $\Delta S^*=0.600685$ (Paper I), **not** $1/4$. The ratio is $0.600685/0.25=2.40$, so the naive identification is wrong by a factor of $\sim 2.4$. The $1/4$ coefficient cannot be the per-link entropy $\Delta S^*$.

**Caveat 2.** The correct route uses the decomposition of Section 4. If $\langle d^{\Sigma}_{\mathrm{out}}\rangle_{d=4}\cdot(\text{boundary vertices per Planck area})=1/4$ in units where the dictionary is normalized, the continuum area law recovers Bekenstein–Hawking. The $1/4$ is then the product of a dimension-dependent local constant and a tiling density — the Dou–Sorkin–style geometric constant, not any primitive discrete quantity.

The full identification of $\langle d^{\Sigma}_{\mathrm{out}}\rangle_{d=4}$ with the causal-set literature's geometric constants is open work.

---

## 6. Use in Paper III

Paper III §5 ("Black Hole Entropy: The Discrete Boundary Law") builds on this observable. Specifically:

- §5.1: The entropy observable — cites Definition 2 above.
- §5.2: Finiteness and invariance — cites Open target 1A.
- §5.3: The decomposition $S_{\mathrm{RA}}=\langle d^{\Sigma}_{\mathrm{out}}\rangle\cdot N_\partial$ — cites Section 1.
- §5.4: The discrete boundary law — cites Section 4.
- §5.5: Locality of severed out-degree — cites `severed_outdegree.py` and Section 4.
- §5.6: Boundary regularity — technical development of the $\langle d^{\Sigma}_{\mathrm{out}}\rangle$ convergence.
- §5.7: Translation to Bekenstein–Hawking — cites Section 5 above, including both caveats.

The paper's overall epistemic tier for the boundary law is **DR** (derived, all steps explicit within RA) at the discrete level; the continuum translation to Bekenstein–Hawking is explicitly **CN** (conjecture, path to closure stated).

---

## 7. Summary

| Item | Status |
|------|--------|
| Definition of $S_{\mathrm{RA}}=\|L_\Sigma\|$ | Adopted (Definition 2) |
| Additivity | DR (Proposition 1) |
| Sensitivity | DR (Proposition 2) |
| Transitive-overcount avoidance | DR (Proposition 3) |
| Decomposition $S_{\mathrm{RA}}=\langle d^{\Sigma}_{\mathrm{out}}\rangle\cdot N_\partial$ | DR |
| Finiteness + internal refinement invariance (1A) | Open |
| Locality $\langle d^{\Sigma}_{\mathrm{out}}\rangle\to$ const in $d$ | CV in $d=2,3$ (`severed_outdegree.py`); open formally |
| Boundary law $S_{\mathrm{RA}}\propto N_\partial$ | DR (given locality) |
| Bekenstein–Hawking match $S_{\mathrm{RA}}\sim A/(4\ell_P^2)$ | CN (normalization $\kappa_{\mathrm{BDG}}$ open) |

---

## Acknowledgments

Propositions 1–3 and Definitions 1–3 in the form given here were contributed by ChatGPT (GPT-4o) on 2026-04-12 as part of an externally-reviewed resolution of the entropy-observable ambiguity in the RA programme. The present note organizes that contribution as a standalone formal artifact for Paper III citations.
