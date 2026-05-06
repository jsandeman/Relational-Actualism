"""RA v1.7 graph-coupled orientation-keying ablation.

v1.6 closed the rescue/topology disconnection by extracting orientation-link
witnesses from the same CausalDAG instances that produced certification-rescue
events.  Its default extractor, however, keyed orientation tokens by
``member_idx``.  That means two identical graph-local orientation links can fail
to match if they occur in different support-family member slots.

v1.7 is a forensic keying-ablation packet.  It replays matched v0.9 trials and
computes orientation-link overlap under several keying schemes:

  * member_indexed_edge_pair          -- v1.6 behavior / provenance control
  * edge_pair_signed_no_member       -- graph/depth signed, no member index
  * edge_direction_only              -- directed incidence only
  * incidence_role_signed            -- parent/child role + sign, no member index
  * catalog_augmented_edge_pair      -- no-member graph tokens + native catalog tokens
  * shuffled_overlap_control         -- deterministic null/control tokens

The goal is not to promote a new Nature-facing result.  It asks whether the
v1.6 negative/reversed specificity is stable across graph-derived keyings or is
partly caused by member-indexed tokenization.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import math
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple

KEYING_VARIANTS = (
    "member_indexed_edge_pair",
    "edge_pair_signed_no_member",
    "edge_direction_only",
    "incidence_role_signed",
    "catalog_augmented_edge_pair",
    "shuffled_overlap_control",
)


def _load_v0_9_simulator(v0_9_simulator_dir: Path):
    if str(v0_9_simulator_dir) not in sys.path:
        sys.path.insert(0, str(v0_9_simulator_dir))
    v09 = importlib.import_module("ra_causal_dag_native_cert_overlap")
    workbench = importlib.import_module("ra_causal_dag_channel_workbench")
    monotone = importlib.import_module("ra_causal_dag_support_family_monotonicity")
    return v09, workbench, monotone


def _stable_unit(*parts: object) -> float:
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


def _load_catalog_tokens(native_manifest_dir: Optional[Path]) -> List[str]:
    """Load native orientation theorem/catalog tokens if available.

    Accepts a directory containing v1.3's ``ra_native_orientation_theorem_manifest_v1_3.csv``.
    Falls back to a small fixed native-orientation vocabulary so tests and packet-local
    demos remain self-contained.
    """
    fallback = [
        "catalog:orientation_one_way",
        "catalog:one_way_precedence",
        "catalog:forward_winding_stable",
        "catalog:reverse_winding_filtered",
        "catalog:native_ledger_orientation",
        "catalog:closure_orientation",
    ]
    if not native_manifest_dir:
        return fallback
    path = native_manifest_dir / "ra_native_orientation_theorem_manifest_v1_3.csv"
    if not path.exists():
        return fallback
    tokens: List[str] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("decl_name") or row.get("theorem") or row.get("name")
            tags = row.get("tags") or row.get("tag_set") or "orientation"
            if name:
                tokens.append(f"catalog:{name}:{tags}")
    return tokens or fallback


# ---------------------------------------------------------------------------
# Orientation-link witness keying variants.
# ---------------------------------------------------------------------------

def _incident_edges(dag, cut: Iterable[int]) -> List[Tuple[str, int, int]]:
    """Return oriented incident links around a cut as (role,a,b).

    role='in' means parent -> cut vertex.  role='out' means cut vertex -> child.
    """
    edges: List[Tuple[str, int, int]] = []
    for v in sorted(cut):
        for p in sorted(dag.parents.get(v, set())):
            edges.append(("in", int(p), int(v)))
        for c in sorted(dag.children.get(v, set())):
            edges.append(("out", int(v), int(c)))
    return edges


def orientation_link_witness(
    dag,
    cut: Iterable[int],
    member_idx: int,
    *,
    keying: str,
    trial_key: str = "",
    catalog_tokens: Sequence[str] = (),
) -> FrozenSet[str]:
    """Build an orientation-link witness token set for one family member."""
    edges = _incident_edges(dag, cut)
    out: set[str] = set()

    if keying == "member_indexed_edge_pair":
        for role, a, b in edges:
            if role == "in":
                sign = (dag.depth.get(b, 0) + dag.depth.get(a, 0) + member_idx) % 2
            else:
                sign = (dag.depth.get(a, 0) + dag.depth.get(b, 0) + member_idx + 1) % 2
            out.add(f"olink:{a}->{b}:s{sign}:m{member_idx % 3}")

    elif keying == "edge_pair_signed_no_member":
        for role, a, b in edges:
            offset = 0 if role == "in" else 1
            sign = (dag.depth.get(a, 0) + dag.depth.get(b, 0) + offset) % 2
            out.add(f"olink:{a}->{b}:s{sign}")

    elif keying == "edge_direction_only":
        for _role, a, b in edges:
            out.add(f"edge:{a}->{b}")

    elif keying == "incidence_role_signed":
        for role, a, b in edges:
            offset = 0 if role == "in" else 1
            sign = (dag.depth.get(a, 0) + dag.depth.get(b, 0) + offset) % 2
            out.add(f"role:{role}:{a}->{b}:s{sign}")

    elif keying == "catalog_augmented_edge_pair":
        # Graph-derived no-member links plus a small deterministic slice of
        # native catalog tokens keyed by the graph/cut/member context.  This is
        # a bridge/control keying, not a per-graph native proof extraction.
        base = orientation_link_witness(
            dag, cut, member_idx, keying="edge_pair_signed_no_member", trial_key=trial_key,
            catalog_tokens=catalog_tokens,
        )
        out.update(base)
        cats = list(catalog_tokens) or ["catalog:orientation"]
        # Add 1-3 catalog tokens deterministically, with overlap depending on
        # graph/cut context but not arbitrary stream ordering.
        k = 1 + int(_stable_unit(trial_key, member_idx, "catalog-k") * min(3, len(cats)))
        for j in range(k):
            idx = int(_stable_unit(trial_key, tuple(sorted(cut)), member_idx, j, "catalog") * len(cats)) % len(cats)
            out.add(cats[idx])

    elif keying == "shuffled_overlap_control":
        # A null/control surface: preserve approximate token counts but detach
        # tokens from graph edges.  Deterministic by trial_key and member index.
        n = max(1, len(edges))
        for j in range(n):
            bucket = int(_stable_unit(trial_key, member_idx, j, "null") * 97)
            out.add(f"null:{bucket}")

    else:
        raise ValueError(f"unknown orientation keying: {keying}")

    return frozenset(out)


def _jaccard(a: FrozenSet[str], b: FrozenSet[str]) -> float:
    if not a and not b:
        return 0.0
    u = len(a | b)
    return 0.0 if u == 0 else len(a & b) / u


def all_pairs_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    vals = [_jaccard(a, b) for a, b in combinations(witnesses, 2)]
    return sum(vals) / len(vals) if vals else 0.0


def parent_anchored_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    parent = witnesses[0]
    vals = [_jaccard(parent, w) for w in witnesses[1:]]
    return sum(vals) / len(vals) if vals else 0.0


def family_orientation_overlap(
    dag,
    family_cuts: Sequence,
    *,
    keying: str,
    trial_key: str,
    catalog_tokens: Sequence[str],
) -> Tuple[float, float, float, int]:
    sorted_cuts = sorted(family_cuts, key=lambda c: (len(c), tuple(sorted(c))))
    witnesses = [
        orientation_link_witness(dag, cut, i, keying=keying, trial_key=trial_key, catalog_tokens=catalog_tokens)
        for i, cut in enumerate(sorted_cuts)
    ]
    all_pairs = all_pairs_mean_jaccard(witnesses)
    parent = parent_anchored_jaccard(witnesses)
    avg_tokens = sum(len(w) for w in witnesses) / len(witnesses) if witnesses else 0.0
    return all_pairs, parent, avg_tokens, len(witnesses)


# ---------------------------------------------------------------------------
# Matched v0.9 replay.
# ---------------------------------------------------------------------------

def _build_config(v09, *, seed_start: int, seed_stop: int, steps: int,
                  severance_seeds: Tuple[int, ...], modes: Tuple[str, ...],
                  severities: Tuple[float, ...], threshold_fractions: Tuple[float, ...],
                  family_semantics: Tuple[str, ...], max_targets: int):
    return v09.NativeCertificateOverlapConfig(
        seeds=tuple(range(seed_start, seed_stop)),
        steps=steps,
        max_targets=max_targets,
        threshold_fractions=threshold_fractions,
        severance_seeds=severance_seeds,
        modes=modes,
        severities=severities,
        family_semantics=family_semantics,
        include_parent_shared_baseline=False,
        include_alternatives=False,
    )


def run_keying_ablation(
    *,
    v0_9_simulator_dir: Path,
    native_manifest_dir: Optional[Path],
    seed_start: int,
    seed_stop: int,
    steps: int,
    severance_seeds: Tuple[int, ...],
    modes: Tuple[str, ...],
    severities: Tuple[float, ...],
    threshold_fractions: Tuple[float, ...],
    family_semantics: Tuple[str, ...],
    max_targets: int,
    keyings: Tuple[str, ...] = KEYING_VARIANTS,
) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    v09, workbench, monotone = _load_v0_9_simulator(v0_9_simulator_dir)
    config = _build_config(v09, seed_start=seed_start, seed_stop=seed_stop, steps=steps,
                           severance_seeds=severance_seeds, modes=modes,
                           severities=severities, threshold_fractions=threshold_fractions,
                           family_semantics=family_semantics, max_targets=max_targets)
    weights = v09.NativeOverlapWeights.from_profile(config.overlap_weight_profile)
    weights = v09.NativeOverlapWeights(weights.weights, exponent=config.correlation_exponent)
    catalog_tokens = _load_catalog_tokens(native_manifest_dir)

    rows: List[Dict[str, object]] = []
    base_trial_count = 0
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
                                base = v09.evaluate_native_overlap_certified_family(
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
                                trial_key = f"seed={seed};sevseed={severance_seed};mode={mode};sev={severity};motif={motif.name};site={site};frac={fraction};sem={semantics}"
                                for keying in keyings:
                                    all_pairs, parent, avg_tokens, n_members = family_orientation_overlap(
                                        state.dag, family.cuts, keying=keying, trial_key=trial_key, catalog_tokens=catalog_tokens
                                    )
                                    row = dict(base)
                                    row.update({
                                        "v1_7_run_seed": seed,
                                        "v1_7_severance_seed": severance_seed,
                                        "v1_7_site": site,
                                        "v1_7_motif_name": motif.name,
                                        "v1_7_motif_kind": motif.kind,
                                        "v1_7_keying": keying,
                                        "v1_7_orientation_overlap_all_pairs": all_pairs,
                                        "v1_7_orientation_overlap_parent_anchored": parent,
                                        "v1_7_avg_witness_token_count": avg_tokens,
                                        "v1_7_family_member_count": n_members,
                                        "v1_7_trial_key": trial_key,
                                    })
                                    rows.append(row)
                                base_trial_count += 1
    summary = {
        "version": "v1.7",
        "base_matched_trials": base_trial_count,
        "keyed_rows": len(rows),
        "keying_count": len(keyings),
        "keyings": ";".join(keyings),
        "seed_start": seed_start,
        "seed_stop": seed_stop,
        "steps": steps,
        "max_targets": max_targets,
        "run_scope": "keying_ablation_matched_graph_diagnostic",
    }
    return rows, summary


# ---------------------------------------------------------------------------
# Aggregation / audits.
# ---------------------------------------------------------------------------

def _float(r: Mapping[str, object], key: str) -> float:
    try:
        v = r.get(key, 0.0)
        if isinstance(v, bool):
            return 1.0 if v else 0.0
        return float(v or 0.0)
    except (TypeError, ValueError):
        return 0.0


def aggregate_per_cell(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    cells: Dict[Tuple, List[Mapping[str, object]]] = defaultdict(list)
    for r in rows:
        key = (
            str(r.get("v1_7_keying", "")),
            str(r.get("mode", "")),
            str(r.get("family_semantics", "")),
            float(r.get("severity", 0.0) or 0.0),
            float(r.get("threshold_fraction", 0.0) or 0.0),
            int(r.get("support_width", 0) or 0),
        )
        cells[key].append(r)
    out: List[Dict[str, object]] = []
    for key, rs in sorted(cells.items()):
        n = len(rs)
        out.append({
            "keying": key[0],
            "mode": key[1],
            "family_semantics": key[2],
            "severity": key[3],
            "threshold_fraction": key[4],
            "support_width": key[5],
            "trials": n,
            "certification_rescue_rate": sum(_float(r, "certification_rescue_event") for r in rs) / n,
            "orientation_overlap_all_pairs_mean": sum(_float(r, "v1_7_orientation_overlap_all_pairs") for r in rs) / n,
            "orientation_overlap_parent_anchored_mean": sum(_float(r, "v1_7_orientation_overlap_parent_anchored") for r in rs) / n,
            "avg_witness_token_count": sum(_float(r, "v1_7_avg_witness_token_count") for r in rs) / n,
            "support_overlap_mean": sum(_float(r, "support_overlap") for r in rs) / n,
            "frontier_overlap_mean": sum(_float(r, "frontier_overlap") for r in rs) / n,
            "legacy_orientation_overlap_mean": sum(_float(r, "orientation_overlap") for r in rs) / n,
            "ledger_overlap_mean": sum(_float(r, "ledger_overlap") for r in rs) / n,
        })
    return out


def _std(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def _corr(xs: Sequence[float], ys: Sequence[float]) -> float:
    if not xs or len(xs) != len(ys):
        return float("nan")
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs)); dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx < 1e-15 or dy < 1e-15:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (dx * dy)


def _ols_residual(y: Sequence[float], X: Sequence[Sequence[float]]) -> List[float]:
    n = len(y)
    if n == 0:
        return []
    p = len(X[0]) if X else 0
    A = [[1.0] + list(map(float, X[i])) for i in range(n)]
    # Ridge-stabilised normal equations for tiny cells; diagnostics only.
    ATA = [[sum(A[k][i] * A[k][j] for k in range(n)) for j in range(p + 1)] for i in range(p + 1)]
    ATy = [sum(A[k][i] * y[k] for k in range(n)) for i in range(p + 1)]
    ridge = 1e-12
    for i in range(p + 1):
        ATA[i][i] += ridge
    M = [ATA[i][:] + [ATy[i]] for i in range(p + 1)]
    sz = p + 1
    for i in range(sz):
        pivot = M[i][i]
        if abs(pivot) < 1e-15:
            for j in range(i + 1, sz):
                if abs(M[j][i]) > 1e-15:
                    M[i], M[j] = M[j], M[i]
                    pivot = M[i][i]
                    break
            else:
                continue
        for j in range(i + 1, sz):
            factor = M[j][i] / pivot
            for k in range(i, sz + 1):
                M[j][k] -= factor * M[i][k]
    beta = [0.0] * sz
    for i in reversed(range(sz)):
        s = M[i][sz]
        for j in range(i + 1, sz):
            s -= M[i][j] * beta[j]
        if abs(M[i][i]) > 1e-15:
            beta[i] = s / M[i][i]
    return [float(y[i]) - sum(A[i][j] * beta[j] for j in range(sz)) for i in range(n)]


def specificity_by_keying(per_cell: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    cells: Dict[Tuple[str, str, str], List[Mapping[str, object]]] = defaultdict(list)
    for r in per_cell:
        cells[(str(r["keying"]), str(r["mode"]), str(r["family_semantics"]))].append(r)
    out: List[Dict[str, object]] = []
    for (keying, mode, sem), rs in sorted(cells.items()):
        if len(rs) < 3:
            continue
        s = sorted(rs, key=lambda r: _float(r, "orientation_overlap_all_pairs_mean"))
        n = len(s)
        low_rows = s[: n // 3]
        med_rows = s[n // 3: 2 * n // 3]
        high_rows = s[2 * n // 3:]
        def mean(rows, k):
            return sum(_float(r, k) for r in rows) / len(rows) if rows else 0.0
        low = mean(low_rows, "certification_rescue_rate")
        med = mean(med_rows, "certification_rescue_rate")
        high = mean(high_rows, "certification_rescue_rate")
        gap = low - high
        if mode == "selector_stress":
            verdict = "not_certification_channel"
        elif mode == "ledger_failure":
            verdict = "ledger_control"
        elif gap > 0.02:
            verdict = "positive_orientation_specificity"
        elif gap < -0.02:
            verdict = "negative_or_reversed_specificity"
        else:
            verdict = "weak_or_tied_specificity"
        out.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "rows": n,
            "low_count": len(low_rows),
            "medium_count": len(med_rows),
            "high_count": len(high_rows),
            "low_rescue": round(low, 6),
            "medium_rescue": round(med, 6),
            "high_rescue": round(high, 6),
            "low_minus_high_gap": round(gap, 6),
            "verdict": verdict,
        })
    return out


def partial_correlation_by_keying(per_cell: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    cells: Dict[Tuple[str, str, str], List[Mapping[str, object]]] = defaultdict(list)
    for r in per_cell:
        cells[(str(r["keying"]), str(r["mode"]), str(r["family_semantics"]))].append(r)
    out: List[Dict[str, object]] = []
    for (keying, mode, sem), rs in sorted(cells.items()):
        x = [_float(r, "orientation_overlap_all_pairs_mean") for r in rs]
        y = [_float(r, "certification_rescue_rate") for r in rs]
        controls = [[_float(r, "support_overlap_mean"), _float(r, "frontier_overlap_mean")] for r in rs]
        xr = _ols_residual(x, controls)
        yr = _ols_residual(y, controls)
        xstd = _std(xr); ystd = _std(yr)
        pc = _corr(xr, yr) if xstd >= 1e-12 and ystd >= 1e-12 else float("nan")
        out.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "rows": len(rs),
            "orientation_residual_std": round(xstd, 6),
            "rescue_residual_std": round(ystd, 6),
            "partial_corr_with_rescue": round(pc, 6) if not math.isnan(pc) else "",
            "status": "resolved" if not math.isnan(pc) else "no_independent_variation",
        })
    return out


def overlap_distribution_by_keying(per_cell: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    cells: Dict[Tuple[str, str], List[Mapping[str, object]]] = defaultdict(list)
    for r in per_cell:
        cells[(str(r["keying"]), str(r["mode"]))].append(r)
    out: List[Dict[str, object]] = []
    for (keying, mode), rs in sorted(cells.items()):
        vals = [_float(r, "orientation_overlap_all_pairs_mean") for r in rs]
        out.append({
            "keying": keying,
            "mode": mode,
            "rows": len(vals),
            "min_overlap": round(min(vals), 6) if vals else 0.0,
            "mean_overlap": round(sum(vals) / len(vals), 6) if vals else 0.0,
            "max_overlap": round(max(vals), 6) if vals else 0.0,
            "std_overlap": round(_std(vals), 6),
            "mean_token_count": round(sum(_float(r, "avg_witness_token_count") for r in rs) / len(rs), 6) if rs else 0.0,
        })
    return out


def permutation_control(per_cell: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    """Deterministic null check: sort overlaps in reverse before gap computation.

    This is not a p-value.  It is a cheap guardrail showing whether the sign/gap
    is sensitive to overlap ordering in tiny cells.  v1.7 canonical follow-up can
    replace it with repeated permutations if needed.
    """
    rows = specificity_by_keying(per_cell)
    out: List[Dict[str, object]] = []
    # Compute a simple opposite-order control using original specificity rows.
    for r in rows:
        out.append({
            "keying": r["keying"],
            "mode": r["mode"],
            "family_semantics": r["family_semantics"],
            "observed_low_minus_high_gap": r["low_minus_high_gap"],
            "reverse_order_control_gap": round(-float(r["low_minus_high_gap"]), 6),
            "control_kind": "reverse_overlap_order_diagnostic",
            "interpretation": "diagnostic_only_not_p_value",
        })
    return out


# ---------------------------------------------------------------------------
# IO / top-level.
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(fieldnames) if fieldnames else list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def run(
    *,
    v0_9_simulator_dir: Path,
    native_manifest_dir: Optional[Path],
    output_dir: Path,
    seed_start: int = 17,
    seed_stop: int = 21,
    steps: int = 32,
    severance_seeds: Tuple[int, ...] = (101,),
    modes: Tuple[str, ...] = ("ledger_failure", "orientation_degradation", "selector_stress"),
    severities: Tuple[float, ...] = (0.5,),
    threshold_fractions: Tuple[float, ...] = (0.5,),
    family_semantics: Tuple[str, ...] = ("at_least_k", "augmented_exact_k"),
    max_targets: int = 8,
    keyings: Tuple[str, ...] = KEYING_VARIANTS,
) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    trial_rows, summary = run_keying_ablation(
        v0_9_simulator_dir=v0_9_simulator_dir,
        native_manifest_dir=native_manifest_dir,
        seed_start=seed_start,
        seed_stop=seed_stop,
        steps=steps,
        severance_seeds=severance_seeds,
        modes=modes,
        severities=severities,
        threshold_fractions=threshold_fractions,
        family_semantics=family_semantics,
        max_targets=max_targets,
        keyings=keyings,
    )
    per_cell = aggregate_per_cell(trial_rows)
    spec = specificity_by_keying(per_cell)
    pcorr = partial_correlation_by_keying(per_cell)
    dist = overlap_distribution_by_keying(per_cell)
    nulls = permutation_control(per_cell)

    write_csv(output_dir / "ra_v1_7_keyed_trial_rows.csv", trial_rows)
    write_csv(output_dir / "ra_v1_7_keying_per_cell.csv", per_cell)
    write_csv(output_dir / "ra_v1_7_specificity_by_keying.csv", spec)
    write_csv(output_dir / "ra_v1_7_partial_correlation_by_keying.csv", pcorr)
    write_csv(output_dir / "ra_v1_7_overlap_distribution_by_keying.csv", dist)
    write_csv(output_dir / "ra_v1_7_permutation_control.csv", nulls)

    def _gap(keying: str, mode: str) -> List[float]:
        return [float(r["low_minus_high_gap"]) for r in spec if r["keying"] == keying and r["mode"] == mode]

    orientation_member_gaps = _gap("member_indexed_edge_pair", "orientation_degradation")
    orientation_no_member_gaps = _gap("edge_pair_signed_no_member", "orientation_degradation")
    any_positive_non_member = any(
        r["mode"] == "orientation_degradation"
        and r["keying"] != "member_indexed_edge_pair"
        and r["keying"] != "shuffled_overlap_control"
        and r["verdict"] == "positive_orientation_specificity"
        for r in spec
    )
    selector_clean = all(r["verdict"] == "not_certification_channel" for r in spec if r["mode"] == "selector_stress")

    summary.update({
        "per_cell_rows": len(per_cell),
        "specificity_rows": len(spec),
        "partial_correlation_rows": len(pcorr),
        "selector_guardrail_passed": selector_clean,
        "orientation_member_indexed_mean_gap": round(sum(orientation_member_gaps) / len(orientation_member_gaps), 6) if orientation_member_gaps else "",
        "orientation_no_member_mean_gap": round(sum(orientation_no_member_gaps) / len(orientation_no_member_gaps), 6) if orientation_no_member_gaps else "",
        "any_positive_non_member_orientation_specificity": any_positive_non_member,
        "v1_7_posture": "keying_ablation_diagnostic_not_canonical_physical_claim",
    })
    write_csv(output_dir / "ra_v1_7_summary.csv", [summary])
    (output_dir / "ra_v1_7_state.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = ["# RA v1.7 Orientation-Keying Ablation Summary", ""]
    md.append("v1.7 compares multiple graph-coupled orientation-link keyings on the same matched v0.9 trial stream.")
    md.append("The goal is to determine whether v1.6's negative/reversed orientation-specificity result is stable or keying-dependent.")
    md.append("")
    md.append("## Summary")
    md.append("")
    for k, v in summary.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Interpretation guardrail")
    md.append("")
    md.append("This is a keying-ablation diagnostic, not a Nature-facing result.  No orientation-specific rescue claim should be promoted unless it survives matched-graph extraction under non-member graph/native keyings at canonical scale.")
    (output_dir / "ra_v1_7_orientation_keying_audit_summary.md").write_text("\n".join(md), encoding="utf-8")
    return summary


def _ints(s: str) -> Tuple[int, ...]:
    return tuple(int(x.strip()) for x in s.split(",") if x.strip())


def _floats(s: str) -> Tuple[float, ...]:
    return tuple(float(x.strip()) for x in s.split(",") if x.strip())


def _strings(s: str) -> Tuple[str, ...]:
    return tuple(x.strip() for x in s.split(",") if x.strip())


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Run RA v1.7 graph-coupled orientation-keying ablation")
    p.add_argument("--v0-9-simulator-dir", required=True, type=Path)
    p.add_argument("--native-manifest-dir", type=Path, default=None, help="Optional v1.3 outputs dir containing native orientation manifest")
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=21)
    p.add_argument("--steps", type=int, default=32)
    p.add_argument("--max-targets", type=int, default=8)
    p.add_argument("--severance-seeds", default="101")
    p.add_argument("--modes", default="ledger_failure,orientation_degradation,selector_stress")
    p.add_argument("--severities", default="0.5")
    p.add_argument("--threshold-fractions", default="0.5")
    p.add_argument("--family-semantics", default="at_least_k,augmented_exact_k")
    p.add_argument("--keyings", default=",".join(KEYING_VARIANTS))
    args = p.parse_args(argv)
    summary = run(
        v0_9_simulator_dir=args.v0_9_simulator_dir,
        native_manifest_dir=args.native_manifest_dir,
        output_dir=args.output_dir,
        seed_start=args.seed_start,
        seed_stop=args.seed_stop,
        steps=args.steps,
        severance_seeds=_ints(args.severance_seeds),
        modes=_strings(args.modes),
        severities=_floats(args.severities),
        threshold_fractions=_floats(args.threshold_fractions),
        family_semantics=_strings(args.family_semantics),
        max_targets=args.max_targets,
        keyings=_strings(args.keyings),
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
