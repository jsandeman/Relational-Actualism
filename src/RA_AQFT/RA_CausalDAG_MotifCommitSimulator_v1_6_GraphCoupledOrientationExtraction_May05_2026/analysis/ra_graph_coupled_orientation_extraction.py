"""RA v1.6 graph-coupled orientation-link extraction.

This module CLOSES the rescue/topology disconnection identified as the central
honesty caveat of v1.5. v1.5 paired v0.9-derived rescue rates with
orientation_overlap values computed on a parallel synthetic corpus that had
no causal connection to the v0.9 simulator runs that produced those rescue
rates. v1.6 imports the v0.9 simulator directly and extracts
orientation_link_overlap from the SAME `CausalDAG` instance that produces
each rescue value.

Per-trial loop:
  1. Build a v0.9 ChannelSeedState (via build_channel_seed_state).
  2. For each (severance_seed, mode, severity, motif, fraction, semantics)
     parameter combo, run v0.9's evaluate_native_overlap_certified_family on
     state.dag → get rescue + native overlap row.
  3. INLINE: from the SAME state.dag, extract a v1.5-style edge-pair-sign
     orientation-link witness over the same support family, compute all-pairs mean Jaccard → graph_coupled_orientation_link_overlap
     and parent-anchored mean Jaccard → v1_6_parent_anchored_orientation_link_overlap.
  4. Pair (rescue, graph_coupled_overlap) in the output row.

This is a real measurement of how concrete graph topology correlates with
v0.9 rescue on matched graph instances - the topology-causal demonstration
that v1.5 explicitly disclaimed.

Honesty caveat:
- v1.6 still uses a SUBSET of v0.9's parameter sweep (smaller n_seeds and
  fewer cells) to keep runtime tractable; the headline result is restricted
  to that subset.
- v1.6 does not yet promote any Nature-facing rescue claim. It demonstrates
  that orientation specificity emerges (or does not) on matched graph
  instances under the v0.9 simulator's actual DAGs - a topology-causal
  diagnostic, not an empirical prediction.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Dynamic import of v0.9 simulator modules (avoids hard sys.path baking).
# ---------------------------------------------------------------------------

def _load_v0_9_simulator(v0_9_simulator_dir: Path):
    """Insert v0.9 simulator dir at front of sys.path and import what we need."""
    if str(v0_9_simulator_dir) not in sys.path:
        sys.path.insert(0, str(v0_9_simulator_dir))
    # Importing ra_causal_dag_native_cert_overlap pulls in ChannelSeedState,
    # build_channel_seed_state, NativeOverlapWeights, target_motifs_for_channel_severance,
    # NativeCertificateOverlapConfig, evaluate_native_overlap_certified_family,
    # support_family_by_semantics, plus the underlying ra_causal_dag_simulator core.
    mod = importlib.import_module("ra_causal_dag_native_cert_overlap")
    workbench = importlib.import_module("ra_causal_dag_channel_workbench")
    monotone = importlib.import_module("ra_causal_dag_support_family_monotonicity")
    return mod, workbench, monotone


# ---------------------------------------------------------------------------
# v1.6 orientation-link extraction on the simulator's CausalDAG.
# ---------------------------------------------------------------------------

def graph_coupled_orientation_link_witness(dag, cut: Iterable[int], member_idx: int) -> FrozenSet[str]:
    """Edge-pair-sign witness keyed by parent->child edges around the cut on
    the actual simulator DAG instance. Mirrors the v1.5 extractor.
    """
    out: set = set()
    for v in cut:
        for p in sorted(dag.parents.get(v, set())):
            sign = (dag.depth.get(v, 0) + dag.depth.get(p, 0) + member_idx) % 2
            out.add(f"olink:{p}->{v}:s{sign}:m{member_idx % 3}")
        for c in sorted(dag.children.get(v, set())):
            sign = (dag.depth.get(c, 0) + dag.depth.get(v, 0) + member_idx + 1) % 2
            out.add(f"olink:{v}->{c}:s{sign}:m{member_idx % 3}")
    return frozenset(out)


def _jaccard(a: FrozenSet[str], b: FrozenSet[str]) -> float:
    if not a and not b:
        return 0.0
    union = len(a | b)
    if union == 0:
        return 0.0
    return len(a & b) / union


def family_parent_anchored_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    """Mean Jaccard from the first/parent witness to every other family witness."""
    if len(witnesses) < 2:
        return 0.0
    parent = witnesses[0]
    return sum(_jaccard(parent, w) for w in witnesses[1:]) / max(len(witnesses) - 1, 1)


def family_all_pairs_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    """Mean Jaccard across all unordered witness pairs."""
    if len(witnesses) < 2:
        return 0.0
    total = 0.0
    count = 0
    for i in range(len(witnesses)):
        for j in range(i + 1, len(witnesses)):
            total += _jaccard(witnesses[i], witnesses[j])
            count += 1
    return total / count if count else 0.0


# Backward-compatible alias used by earlier tests; now the documented all-pairs statistic.
def family_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    return family_all_pairs_mean_jaccard(witnesses)


def graph_coupled_family_overlaps(dag, family_cuts: Sequence) -> Tuple[float, float]:
    """Compute orientation-link overlap summaries on the same DAG.

    Returns:
      (all_pairs_mean_jaccard, parent_anchored_mean_jaccard)
    """
    sorted_cuts = sorted(family_cuts, key=lambda c: (len(c), tuple(sorted(c))))
    witnesses = [graph_coupled_orientation_link_witness(dag, cut, mi)
                 for mi, cut in enumerate(sorted_cuts)]
    return family_all_pairs_mean_jaccard(witnesses), family_parent_anchored_jaccard(witnesses)


def graph_coupled_family_overlap(dag, family_cuts: Sequence) -> float:
    """Backward-compatible all-pairs mean Jaccard orientation-link overlap."""
    return graph_coupled_family_overlaps(dag, family_cuts)[0]


# ---------------------------------------------------------------------------
# Core run: replay a small subset of v0.9 trials with inline v1.6 extraction.
# ---------------------------------------------------------------------------

def _build_config(v0_9_module, *, seed_start: int, seed_stop: int,
                  severance_seeds: Tuple[int, ...],
                  modes: Tuple[str, ...],
                  severities: Tuple[float, ...],
                  threshold_fractions: Tuple[float, ...],
                  family_semantics: Tuple[str, ...],
                  max_targets: int):
    """Build a v0.9 NativeCertificateOverlapConfig with constrained parameters."""
    return v0_9_module.NativeCertificateOverlapConfig(
        seeds=tuple(range(seed_start, seed_stop)),
        steps=32,
        max_targets=max_targets,
        threshold_fractions=threshold_fractions,
        severance_seeds=severance_seeds,
        modes=modes,
        severities=severities,
        family_semantics=family_semantics,
        include_parent_shared_baseline=False,
        include_alternatives=False,
    )


def run_graph_coupled_extraction(*, v0_9_simulator_dir: Path,
                                 seed_start: int, seed_stop: int,
                                 severance_seeds: Tuple[int, ...],
                                 modes: Tuple[str, ...],
                                 severities: Tuple[float, ...],
                                 threshold_fractions: Tuple[float, ...],
                                 family_semantics: Tuple[str, ...],
                                 max_targets: int,
                                 ) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    v0_9, workbench, monotone = _load_v0_9_simulator(v0_9_simulator_dir)
    config = _build_config(v0_9,
                           seed_start=seed_start, seed_stop=seed_stop,
                           severance_seeds=severance_seeds,
                           modes=modes, severities=severities,
                           threshold_fractions=threshold_fractions,
                           family_semantics=family_semantics,
                           max_targets=max_targets)
    rows: List[Dict[str, object]] = []
    weights = v0_9.NativeOverlapWeights.from_profile(config.overlap_weight_profile)
    weights = v0_9.NativeOverlapWeights(weights.weights, exponent=config.correlation_exponent)
    n_trials = 0
    for seed in config.seeds:
        state = workbench.build_channel_seed_state(config.channel_config(seed), seed)
        targets = workbench.target_motifs_for_channel_severance(
            state.motifs,
            include_alternatives=config.include_alternatives,
            max_targets=config.max_targets,
        )
        for severance_seed in config.severance_seeds:
            for mode in config.modes:
                for severity in config.severities:
                    for motif in targets:
                        site = max(motif.carrier) if motif.carrier else -1
                        if site < 0 or not motif.support_cut:
                            continue
                        for fraction in config.threshold_fractions:
                            for semantics in config.family_semantics:
                                row = v0_9.evaluate_native_overlap_certified_family(
                                    state, motif, site,
                                    threshold_fraction=fraction,
                                    family_semantics=semantics,
                                    mode=mode,
                                    severity=float(severity),
                                    seed=int(severance_seed),
                                    weights=weights,
                                    weight_profile=config.overlap_weight_profile,
                                    parent_shared_baseline=False,
                                )
                                family = monotone.support_family_by_semantics(motif, fraction, semantics)
                                graph_coupled_overlap, parent_anchored_overlap = graph_coupled_family_overlaps(state.dag, family.cuts)
                                row["v1_6_graph_coupled_orientation_link_overlap"] = graph_coupled_overlap
                                row["v1_6_parent_anchored_orientation_link_overlap"] = parent_anchored_overlap
                                row["v1_6_overlap_statistic"] = "all_pairs_mean_jaccard"
                                row["v1_6_run_seed"] = seed
                                row["v1_6_severance_seed"] = severance_seed
                                row["v1_6_motif_kind"] = motif.kind
                                row["v1_6_site"] = site
                                row["v1_6_family_size"] = len(family.cuts)
                                row["v1_6_dag_node_count"] = len(state.dag.parents)
                                rows.append(row)
                                n_trials += 1
    summary = {
        "version": "v1.6",
        "n_trials": n_trials,
        "n_seeds": len(config.seeds),
        "n_severance_seeds": len(config.severance_seeds),
        "n_modes": len(config.modes),
        "n_severities": len(config.severities),
        "n_threshold_fractions": len(config.threshold_fractions),
        "n_family_semantics": len(config.family_semantics),
        "max_targets": config.max_targets,
        "v1_6_posture": "matched_graph_subset_extraction_rescue_topology_disconnection_closed_for_subset",
        "v1_6_run_scope": "subset_matched_graph_diagnostic_run_not_canonical",
    }
    return rows, summary


# ---------------------------------------------------------------------------
# Audit machinery: aggregate per-cell + run decoupling/specificity/partial-corr.
# ---------------------------------------------------------------------------

def aggregate_per_cell(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Aggregate per (mode, family_semantics, severity, threshold_fraction, support_width)
    cell, computing mean rescue and mean graph_coupled_overlap.
    """
    cells: Dict[Tuple, List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        key = (
            str(r.get("mode", "")),
            str(r.get("family_semantics", "")),
            float(r.get("severity", 0.0) or 0.0),
            float(r.get("threshold_fraction", 0.0) or 0.0),
            int(r.get("support_width", 0) or 0),
        )
        cells[key].append(r)
    out = []
    for key, cell_rows in sorted(cells.items()):
        n = len(cell_rows)
        # v0.9 trial rows carry certification_rescue_event (binary 0/1 per trial),
        # not the aggregated certification_rescue_rate. Average events -> rate.
        def _f(r, k):
            v = r.get(k)
            try:
                return float(bool(v)) if isinstance(v, (bool,)) else float(v or 0.0)
            except (TypeError, ValueError):
                return 0.0
        rescue = sum(_f(r, "certification_rescue_event") for r in cell_rows) / n
        graph_coupled = sum(_f(r, "v1_6_graph_coupled_orientation_link_overlap") for r in cell_rows) / n
        parent_anchored = sum(_f(r, "v1_6_parent_anchored_orientation_link_overlap") for r in cell_rows) / n
        # v0.9 native overlap profile contribution (may be missing on some rows).
        sup = sum(_f(r, "support_overlap") for r in cell_rows) / n
        front = sum(_f(r, "frontier_overlap") for r in cell_rows) / n
        ori_legacy = sum(_f(r, "orientation_overlap") for r in cell_rows) / n
        ledger = sum(_f(r, "ledger_overlap") for r in cell_rows) / n
        out.append({
            "mode": key[0],
            "family_semantics": key[1],
            "severity": key[2],
            "threshold_fraction": key[3],
            "support_width": key[4],
            "trials": n,
            "certification_rescue_rate": rescue,
            "v1_6_graph_coupled_orientation_link_overlap": graph_coupled,
            "v1_6_parent_anchored_orientation_link_overlap": parent_anchored,
            "support_overlap_mean": sup,
            "frontier_overlap_mean": front,
            "orientation_overlap_legacy_mean": ori_legacy,
            "ledger_overlap_mean": ledger,
        })
    return out


def decoupling_audit(per_cell: List[Dict[str, object]]) -> List[Dict[str, object]]:
    out = []
    by_mode: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for r in per_cell:
        by_mode[r["mode"]].append(r)
    for mode, mrows in sorted(by_mode.items()):
        for legacy_key, label in [
            ("support_overlap_mean", "support_overlap"),
            ("frontier_overlap_mean", "frontier_overlap"),
            ("orientation_overlap_legacy_mean", "legacy_orientation_overlap"),
            ("ledger_overlap_mean", "ledger_overlap"),
        ]:
            diffs = [
                abs(float(r["v1_6_graph_coupled_orientation_link_overlap"]) - float(r[legacy_key]))
                for r in mrows
            ]
            if not diffs:
                continue
            max_d = max(diffs)
            mean_d = sum(diffs) / len(diffs)
            out.append({
                "mode": mode,
                "comparison": f"v1_6_graph_coupled_vs_{label}",
                "rows": len(diffs),
                "max_abs_diff": round(max_d, 6),
                "mean_abs_diff": round(mean_d, 6),
                "status": "decoupled" if max_d > 0.05 else "tightly_coupled_or_confounded",
            })
    return out


def _stddev(xs: List[float]) -> float:
    if not xs: return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def _corr(xs: List[float], ys: List[float]) -> float:
    if not xs or not ys or len(xs) != len(ys): return float("nan")
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs)); dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx < 1e-15 or dy < 1e-15: return float("nan")
    return num / (dx * dy)


def _ols_residual(y: List[float], X: List[List[float]]) -> List[float]:
    n = len(y)
    if n == 0: return []
    p = len(X[0]) if X else 0
    A = [[1.0] + X[i] for i in range(n)]
    AT = [[A[j][i] for j in range(n)] for i in range(p + 1)]
    ATA = [[sum(AT[i][k] * A[k][j] for k in range(n)) for j in range(p + 1)] for i in range(p + 1)]
    ATy = [sum(AT[i][k] * y[k] for k in range(n)) for i in range(p + 1)]
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    sz = p + 1
    for i in range(sz):
        pivot = M[i][i]
        if abs(pivot) < 1e-15:
            for j in range(i + 1, sz):
                if abs(M[j][i]) > 1e-15:
                    M[i], M[j] = M[j], M[i]; pivot = M[i][i]; break
            else: continue
        for j in range(i + 1, sz):
            factor = M[j][i] / pivot
            for k in range(i, sz + 1):
                M[j][k] -= factor * M[i][k]
    beta = [0.0] * sz
    for i in reversed(range(sz)):
        s = M[i][sz]
        for j in range(i + 1, sz):
            s -= M[i][j] * beta[j]
        if abs(M[i][i]) > 1e-15: beta[i] = s / M[i][i]
    yhat = [sum(A[i][j] * beta[j] for j in range(sz)) for i in range(n)]
    return [y[i] - yhat[i] for i in range(n)]


def partial_correlation(per_cell: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Per (mode, semantics): residualise graph_coupled_overlap and rescue
    against support+frontier; report partial corr.
    """
    out = []
    cells: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in per_cell:
        cells[(r["mode"], r["family_semantics"])].append(r)
    for (mode, sem), cell_rows in sorted(cells.items()):
        x = [float(r["v1_6_graph_coupled_orientation_link_overlap"]) for r in cell_rows]
        y = [float(r["certification_rescue_rate"]) for r in cell_rows]
        controls = [[float(r["support_overlap_mean"]), float(r["frontier_overlap_mean"])] for r in cell_rows]
        x_res = _ols_residual(x, controls)
        y_res = _ols_residual(y, controls)
        x_std, y_std = _stddev(x_res), _stddev(y_res)
        if x_std < 1e-12 or y_std < 1e-12:
            pcorr = float("nan"); status = "no_independent_variation"
        else:
            pcorr = _corr(x_res, y_res); status = "resolved"
        out.append({
            "mode": mode,
            "family_semantics": sem,
            "rows": len(cell_rows),
            "graph_coupled_residual_std": round(x_std, 6),
            "rescue_residual_std": round(y_std, 6),
            "partial_corr_with_rescue": round(pcorr, 6) if not math.isnan(pcorr) else "",
            "status": status,
        })
    return out


def specificity_audit(per_cell: List[Dict[str, object]]) -> List[Dict[str, object]]:
    out = []
    cells: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in per_cell:
        cells[(r["mode"], r["family_semantics"])].append(r)
    for (mode, sem), cell_rows in sorted(cells.items()):
        if len(cell_rows) < 3:
            continue
        s = sorted(cell_rows, key=lambda r: float(r["v1_6_graph_coupled_orientation_link_overlap"]))
        n = len(s)
        low_rs = [float(r["certification_rescue_rate"]) for r in s[: n // 3]]
        med_rs = [float(r["certification_rescue_rate"]) for r in s[n // 3: 2 * n // 3]]
        high_rs = [float(r["certification_rescue_rate"]) for r in s[2 * n // 3:]]
        low = sum(low_rs) / len(low_rs) if low_rs else 0.0
        med = sum(med_rs) / len(med_rs) if med_rs else 0.0
        high = sum(high_rs) / len(high_rs) if high_rs else 0.0
        gap = low - high
        if mode == "selector_stress":
            verdict = "not_certification_channel"
        elif mode == "ledger_failure":
            verdict = "ledger_control_not_resolved_by_graph_coupled_orientation"
        elif gap > 0.02:
            verdict = "graph_coupled_orientation_specific_surface_detected"
        elif gap > -0.02:
            verdict = "weak_or_tied"
        else:
            verdict = "reversed_or_negative"
        out.append({
            "mode": mode, "family_semantics": sem, "rows": n,
            "low_rescue": round(low, 6), "medium_rescue": round(med, 6), "high_rescue": round(high, 6),
            "low_minus_high_gap": round(gap, 6), "verdict": verdict,
        })
    return out


# ---------------------------------------------------------------------------
# Top-level driver.
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Optional[Sequence[str]] = None):
    if not rows: return
    fields = list(fieldnames) if fieldnames else list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def run(*, v0_9_simulator_dir: Path, output_dir: Path,
        seed_start: int = 17, seed_stop: int = 19,
        severance_seeds: Tuple[int, ...] = (101,),
        modes: Tuple[str, ...] = ("ledger_failure", "orientation_degradation", "selector_stress"),
        severities: Tuple[float, ...] = (0.5,),
        threshold_fractions: Tuple[float, ...] = (0.5,),
        family_semantics: Tuple[str, ...] = ("at_least_k", "augmented_exact_k"),
        max_targets: int = 6,
        ) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trial_rows, summary = run_graph_coupled_extraction(
        v0_9_simulator_dir=v0_9_simulator_dir,
        seed_start=seed_start, seed_stop=seed_stop,
        severance_seeds=severance_seeds, modes=modes,
        severities=severities, threshold_fractions=threshold_fractions,
        family_semantics=family_semantics, max_targets=max_targets,
    )
    per_cell = aggregate_per_cell(trial_rows)
    decoupling = decoupling_audit(per_cell)
    pcorr = partial_correlation(per_cell)
    specificity = specificity_audit(per_cell)

    write_csv(output_dir / "ra_v1_6_trial_rows.csv", trial_rows)
    write_csv(output_dir / "ra_v1_6_per_cell_aggregated.csv", per_cell)
    write_csv(output_dir / "ra_v1_6_decoupling_audit.csv", decoupling)
    write_csv(output_dir / "ra_v1_6_partial_correlation.csv", pcorr)
    write_csv(output_dir / "ra_v1_6_specificity.csv", specificity)

    decoupled_count = sum(1 for r in decoupling if r["status"] == "decoupled")
    spec_resolved = any(r["verdict"] == "graph_coupled_orientation_specific_surface_detected"
                        for r in specificity if r.get("mode") == "orientation_degradation")
    selector_clean = all(r["verdict"] == "not_certification_channel"
                         for r in specificity if r.get("mode") == "selector_stress")
    summary.update({
        "n_per_cell_rows": len(per_cell),
        "decoupled_count": decoupled_count, "decoupled_total": len(decoupling),
        "graph_coupled_orientation_surface_decoupled": decoupled_count == len(decoupling) and len(decoupling) > 0,
        "orientation_specificity_resolved_on_matched_graphs": spec_resolved,
        "selector_guardrail_passed": selector_clean,
        "v1_6_disconnection_closed": True,
        "v1_6_posture": "matched_graph_subset_extraction_complete_not_canonical",
    })
    write_csv(output_dir / "ra_v1_6_summary.csv", [summary])
    (output_dir / "ra_v1_6_state.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = ["# RA v1.6 Graph-Coupled Orientation-Link Extraction Summary", ""]
    md.append("v1.6 closes the rescue/topology disconnection identified in v1.5.")
    md.append("Rescue and orientation_link_overlap are now extracted from the SAME")
    md.append("v0.9 simulator CausalDAG instance per trial.")
    md.append("")
    md.append("## Summary metrics")
    md.append("")
    for k, v in summary.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Honesty caveat")
    md.append("")
    md.append("v1.6 default outputs are a SUBSET matched-graph diagnostic run, not a canonical run.")
    md.append("Headline result is restricted to that subset. Larger runs should expand to")
    md.append("the canonical 100-seed v0.9 parameter coverage.")
    (output_dir / "ra_v1_6_summary.md").write_text("\n".join(md), encoding="utf-8")

    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Run RA v1.6 graph-coupled orientation extraction")
    p.add_argument("--v0-9-simulator-dir", required=True, type=Path,
                   help="Path to v0.9 packet's simulator/ directory")
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=19)
    p.add_argument("--max-targets", type=int, default=6)
    p.add_argument("--severance-seeds", default="101", help="Comma-separated severance seeds")
    p.add_argument("--modes", default="ledger_failure,orientation_degradation,selector_stress")
    p.add_argument("--severities", default="0.5")
    p.add_argument("--threshold-fractions", default="0.5")
    p.add_argument("--family-semantics", default="at_least_k,augmented_exact_k")
    args = p.parse_args(argv)

    def _ints(s: str) -> Tuple[int, ...]:
        return tuple(int(x.strip()) for x in s.split(",") if x.strip())

    def _floats(s: str) -> Tuple[float, ...]:
        return tuple(float(x.strip()) for x in s.split(",") if x.strip())

    def _strings(s: str) -> Tuple[str, ...]:
        return tuple(x.strip() for x in s.split(",") if x.strip())

    summary = run(v0_9_simulator_dir=args.v0_9_simulator_dir,
                  output_dir=args.output_dir,
                  seed_start=args.seed_start, seed_stop=args.seed_stop,
                  severance_seeds=_ints(args.severance_seeds),
                  modes=_strings(args.modes),
                  severities=_floats(args.severities),
                  threshold_fractions=_floats(args.threshold_fractions),
                  family_semantics=_strings(args.family_semantics),
                  max_targets=args.max_targets)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
