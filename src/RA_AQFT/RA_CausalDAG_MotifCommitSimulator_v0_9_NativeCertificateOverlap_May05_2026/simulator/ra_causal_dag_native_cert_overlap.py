#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.9 native certificate-overlap workbench.

v0.8 showed that certification rescue decreases as an external certificate-
correlation parameter increases. v0.9 replaces that external knob with a
simulator-side RA-native overlap calculation over member certificate witnesses.

The overlap calculation is not yet a derived BDG-LLC law. It is a disciplined
anchoring layer: member witnesses carry support/frontier, causal-past,
orientation-link, ledger-gate, BDG-kernel-proxy, and firewall-exposure component
sets. Pairwise Jaccard overlap across these components induces an effective
certificate correlation used by the v0.8 independent-member certification
mechanism.

RA-native hypothesis under test:

  certification rescue decreases as native certificate-witness overlap increases.

The implementation preserves the guardrail that selector stress is not counted
as support/certification-family rescue.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple

try:
    from .ra_causal_dag_simulator import MotifCandidate, NodeId, SupportCut, rows_to_csv
    from .ra_causal_dag_channel_workbench import (
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        target_motifs_for_channel_severance,
    )
    from .ra_causal_dag_support_family_monotonicity import support_family_by_semantics
    from .ra_causal_dag_support_family_workbench import SupportCutFamily
    from .ra_causal_dag_independent_cert_families import (
        CERTIFICATION_MODES,
        evaluate_independent_certified_family,
        _rate,
        _mean,
    )
except ImportError:  # pragma: no cover - direct script mode
    from ra_causal_dag_simulator import MotifCandidate, NodeId, SupportCut, rows_to_csv  # type: ignore
    from ra_causal_dag_channel_workbench import (  # type: ignore
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        target_motifs_for_channel_severance,
    )
    from ra_causal_dag_support_family_monotonicity import support_family_by_semantics  # type: ignore
    from ra_causal_dag_support_family_workbench import SupportCutFamily  # type: ignore
    from ra_causal_dag_independent_cert_families import (  # type: ignore
        CERTIFICATION_MODES,
        evaluate_independent_certified_family,
        _rate,
        _mean,
    )

OVERLAP_COMPONENTS: Tuple[str, ...] = (
    "support",
    "frontier",
    "orientation",
    "ledger",
    "causal_past",
    "bdg_kernel",
    "firewall",
)

DEFAULT_OVERLAP_WEIGHTS: Mapping[str, float] = {
    "support": 0.18,
    "frontier": 0.16,
    "orientation": 0.18,
    "ledger": 0.18,
    "causal_past": 0.12,
    "bdg_kernel": 0.10,
    "firewall": 0.08,
}


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _jaccard(a: Iterable[object], b: Iterable[object]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    return len(sa & sb) / len(union) if union else 1.0


def _bin_overlap(value: float) -> str:
    v = _clip01(value)
    if v < 1.0 / 3.0:
        return "low"
    if v < 2.0 / 3.0:
        return "medium"
    return "high"


@dataclass(frozen=True)
class NativeOverlapWeights:
    """Weights for component-level native witness overlap."""

    weights: Mapping[str, float]
    exponent: float = 1.0
    floor: float = 0.0
    scale: float = 1.0

    @staticmethod
    def balanced() -> "NativeOverlapWeights":
        return NativeOverlapWeights(dict(DEFAULT_OVERLAP_WEIGHTS))

    @staticmethod
    def from_profile(profile: str) -> "NativeOverlapWeights":
        p = profile.strip().lower()
        if p == "balanced":
            return NativeOverlapWeights.balanced()
        if p == "support_heavy":
            return NativeOverlapWeights({
                "support": 0.30, "frontier": 0.24, "orientation": 0.10,
                "ledger": 0.10, "causal_past": 0.10, "bdg_kernel": 0.10, "firewall": 0.06,
            })
        if p == "certificate_heavy":
            return NativeOverlapWeights({
                "support": 0.08, "frontier": 0.08, "orientation": 0.28,
                "ledger": 0.28, "causal_past": 0.08, "bdg_kernel": 0.10, "firewall": 0.10,
            })
        raise ValueError(f"unknown overlap weight profile: {profile}")

    def normalized(self) -> Dict[str, float]:
        raw = {c: max(0.0, float(self.weights.get(c, 0.0))) for c in OVERLAP_COMPONENTS}
        total = sum(raw.values())
        if total <= 0:
            return dict(DEFAULT_OVERLAP_WEIGHTS)
        return {k: v / total for k, v in raw.items()}

    def induce_correlation(self, weighted_overlap: float) -> float:
        base = _clip01(weighted_overlap)
        if self.exponent != 1.0:
            base = math.pow(base, self.exponent)
        return round(_clip01(self.floor + self.scale * base), 6)


@dataclass(frozen=True)
class NativeCertificateWitness:
    """Component sets for one support-family member certificate witness."""

    cut: SupportCut
    support: FrozenSet[str]
    frontier: FrozenSet[str]
    orientation: FrozenSet[str]
    ledger: FrozenSet[str]
    causal_past: FrozenSet[str]
    bdg_kernel: FrozenSet[str]
    firewall: FrozenSet[str]

    def components(self) -> Mapping[str, FrozenSet[str]]:
        return {
            "support": self.support,
            "frontier": self.frontier,
            "orientation": self.orientation,
            "ledger": self.ledger,
            "causal_past": self.causal_past,
            "bdg_kernel": self.bdg_kernel,
            "firewall": self.firewall,
        }


@dataclass(frozen=True)
class NativeOverlapProfile:
    """Pairwise-overlap profile for a support-family's certificate witnesses."""

    family_size: int
    pair_count: int
    component_overlap: Mapping[str, float]
    weighted_overlap: float
    induced_certificate_correlation: float
    overlap_bin: str
    weight_profile: str

    def to_row(self) -> Dict[str, object]:
        row: Dict[str, object] = {
            "family_size": self.family_size,
            "pair_count": self.pair_count,
            "weighted_native_overlap": self.weighted_overlap,
            "induced_certificate_correlation": self.induced_certificate_correlation,
            "native_overlap_bin": self.overlap_bin,
            "overlap_weight_profile": self.weight_profile,
        }
        for c in OVERLAP_COMPONENTS:
            row[f"{c}_overlap"] = self.component_overlap.get(c, 0.0)
        return row


@dataclass(frozen=True)
class NativeCertificateOverlapConfig:
    """Configuration for the v0.9 native certificate-overlap workbench."""

    seeds: Tuple[int, ...] = tuple(range(17, 21))
    steps: int = 16
    max_parents: int = 4
    target_frontier_min: int = 5
    branch_probability: float = 0.42
    wide_join_probability: float = 0.72
    conflict_rate: float = 0.22
    defect_rate: float = 0.02
    orientation_defect_rate: float = 0.02
    conflict_witness_defect_rate: float = 0.08
    severance_seeds: Tuple[int, ...] = (101, 103)
    severities: Tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.0)
    modes: Tuple[str, ...] = ("ledger_failure", "orientation_degradation", "selector_stress")
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.50, 0.25)
    family_semantics: Tuple[str, ...] = ("at_least_k", "augmented_exact_k")
    include_parent_shared_baseline: bool = True
    overlap_weight_profile: str = "balanced"
    correlation_exponent: float = 1.0
    include_alternatives: bool = False
    max_targets: Optional[int] = 8
    sample_limit: int = 1000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "NativeCertificateOverlapConfig":
        seeds = tuple(range(args.seed_start, args.seed_stop)) if args.seed_list is None else tuple(int(x) for x in args.seed_list.split(",") if x.strip())
        return cls(
            seeds=seeds,
            steps=args.steps,
            max_parents=args.max_parents,
            target_frontier_min=args.target_frontier_min,
            branch_probability=args.branch_probability,
            wide_join_probability=args.wide_join_probability,
            conflict_rate=args.conflict_rate,
            defect_rate=args.defect_rate,
            orientation_defect_rate=args.orientation_defect_rate,
            conflict_witness_defect_rate=args.conflict_witness_defect_rate,
            severance_seeds=tuple(int(x) for x in args.severance_seeds.split(",") if x.strip()),
            severities=tuple(float(x) for x in args.severities.split(",") if x.strip()),
            modes=tuple(x.strip() for x in args.modes.split(",") if x.strip()),
            threshold_fractions=tuple(float(x) for x in args.threshold_fractions.split(",") if x.strip()),
            family_semantics=tuple(x.strip() for x in args.family_semantics.split(",") if x.strip()),
            include_parent_shared_baseline=not args.no_parent_shared_baseline,
            overlap_weight_profile=args.overlap_weight_profile,
            correlation_exponent=args.correlation_exponent,
            include_alternatives=args.include_alternatives,
            max_targets=None if args.max_targets < 0 else args.max_targets,
            sample_limit=args.sample_limit,
        )

    def channel_config(self, seed: int) -> ChannelSeparatedRunConfig:
        return ChannelSeparatedRunConfig(
            seeds=(seed,),
            steps=self.steps,
            max_parents=self.max_parents,
            target_frontier_min=self.target_frontier_min,
            branch_probability=self.branch_probability,
            wide_join_probability=self.wide_join_probability,
            conflict_rate=self.conflict_rate,
            defect_rate=self.defect_rate,
            orientation_defect_rate=self.orientation_defect_rate,
            conflict_witness_defect_rate=self.conflict_witness_defect_rate,
            severance_seeds=self.severance_seeds,
            severities=self.severities,
            modes=self.modes,
            include_alternatives=self.include_alternatives,
            max_targets=self.max_targets,
            sample_limit=self.sample_limit,
        )


def _node_label(prefix: str, n: NodeId) -> str:
    return f"{prefix}:{int(n)}"


def _witness_for_cut(state: ChannelSeedState, motif: MotifCandidate, cut: SupportCut, site: int) -> NativeCertificateWitness:
    dag = state.dag
    support = frozenset(_node_label("support", v) for v in cut)
    frontier = frozenset(_node_label("frontier", v) for v in cut)
    causal_nodes = set()
    for v in cut:
        causal_nodes.update(dag.ancestors(v, include_self=True))
    # Orientation links: local incidence around the cut.  These use graph-native
    # parent/child relations as a simulator-side proxy for orientation witnesses.
    orientation = set()
    for v in cut:
        parents = sorted(dag.parents.get(v, ()))
        children = sorted(dag.children.get(v, ()))
        if not parents and not children:
            orientation.add(f"orient:isolated:{v}")
        for p in parents:
            orientation.add(f"orient:{p}->{v}:s{1 if (p + v) % 2 == 0 else -1}")
        for c in children:
            orientation.add(f"orient:{v}->{c}:s{1 if (c - v) % 2 == 0 else -1}")
    # Ledger gates: local depth/modular signatures and a motif-local ledger tag.
    # These are not particle labels; they are simulator gate names used to track
    # native-ledger overlap among family members.
    ledger = set()
    for v in cut:
        ledger.add(f"ledger:depth:{dag.depth.get(v, 0) % 5}")
        ledger.add(f"ledger:qN1:7")
        ledger.add(f"ledger:node-class:{v % 7}")
        ledger.add(f"ledger:motif-kind:{motif.kind}")
    # BDG/LLC kernel proxy: small local neighborhood around support vertices.
    bdg_nodes = set(cut)
    for v in cut:
        bdg_nodes.update(dag.parents.get(v, ()))
        bdg_nodes.update(dag.children.get(v, ()))
    # Causal firewall proxy: boundary edges crossing the causal-past set.
    firewall = set()
    for p, c in dag.edges:
        inside_p = p in causal_nodes
        inside_c = c in causal_nodes
        if inside_p != inside_c:
            firewall.add(f"firewall:{p}->{c}")
    if not firewall:
        # keep empty firewall overlap meaningful but avoid all-empty equivalence
        firewall.add(f"firewall:none:{len(cut)}")
    return NativeCertificateWitness(
        cut=cut,
        support=support,
        frontier=frontier,
        orientation=frozenset(orientation),
        ledger=frozenset(ledger),
        causal_past=frozenset(_node_label("past", v) for v in causal_nodes),
        bdg_kernel=frozenset(_node_label("bdg", v) for v in bdg_nodes),
        firewall=frozenset(firewall),
    )


def _mean_pairwise_component_overlap(witnesses: Sequence[NativeCertificateWitness]) -> Tuple[int, Dict[str, float]]:
    if len(witnesses) <= 1:
        return 0, {c: 1.0 for c in OVERLAP_COMPONENTS}
    sums = {c: 0.0 for c in OVERLAP_COMPONENTS}
    pairs = 0
    for i in range(len(witnesses)):
        for j in range(i + 1, len(witnesses)):
            pairs += 1
            ci = witnesses[i].components()
            cj = witnesses[j].components()
            for c in OVERLAP_COMPONENTS:
                sums[c] += _jaccard(ci[c], cj[c])
    return pairs, {c: round(sums[c] / pairs, 6) if pairs else 1.0 for c in OVERLAP_COMPONENTS}


def native_overlap_profile_for_family(
    state: ChannelSeedState,
    motif: MotifCandidate,
    family: SupportCutFamily,
    site: int,
    *,
    weights: NativeOverlapWeights,
    weight_profile: str = "balanced",
) -> NativeOverlapProfile:
    witnesses = [_witness_for_cut(state, motif, cut, site) for cut in sorted(family.cuts, key=lambda cut: (len(cut), tuple(sorted(cut))))]
    pair_count, comp = _mean_pairwise_component_overlap(witnesses)
    norm = weights.normalized()
    weighted = round(sum(float(comp[c]) * float(norm[c]) for c in OVERLAP_COMPONENTS), 6)
    induced = weights.induce_correlation(weighted)
    return NativeOverlapProfile(
        family_size=family.family_size,
        pair_count=pair_count,
        component_overlap=comp,
        weighted_overlap=weighted,
        induced_certificate_correlation=induced,
        overlap_bin=_bin_overlap(induced),
        weight_profile=weight_profile,
    )


def evaluate_native_overlap_certified_family(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    *,
    threshold_fraction: float,
    family_semantics: str,
    mode: str,
    severity: float,
    seed: int,
    weights: NativeOverlapWeights,
    weight_profile: str,
    parent_shared_baseline: bool = False,
) -> Dict[str, object]:
    family = support_family_by_semantics(motif, threshold_fraction, family_semantics)
    profile = native_overlap_profile_for_family(state, motif, family, site, weights=weights, weight_profile=weight_profile)
    if parent_shared_baseline:
        regime = "parent_shared"
        corr = 1.0
        native_regime = "parent_shared_baseline"
    else:
        regime = "independent_member"
        corr = profile.induced_certificate_correlation
        native_regime = "native_overlap_induced"
    row = evaluate_independent_certified_family(
        state,
        motif,
        site,
        threshold_fraction=threshold_fraction,
        family_semantics=family_semantics,
        certification_regime=regime,
        certificate_correlation=corr,
        mode=mode,
        severity=severity,
        seed=seed,
    )
    row.update(profile.to_row())
    row["native_certification_regime"] = native_regime
    row["certificate_correlation_source"] = "parent_shared_baseline" if parent_shared_baseline else "native_witness_overlap"
    row["external_certificate_correlation"] = row.get("certificate_correlation")
    row["certificate_correlation"] = corr
    return row


def iter_native_overlap_rows_for_seed(config: NativeCertificateOverlapConfig, seed: int) -> Iterator[Dict[str, object]]:
    state = build_channel_seed_state(config.channel_config(seed), seed)
    targets = target_motifs_for_channel_severance(state.motifs, include_alternatives=config.include_alternatives, max_targets=config.max_targets)
    weights = NativeOverlapWeights.from_profile(config.overlap_weight_profile)
    weights = NativeOverlapWeights(weights.weights, exponent=config.correlation_exponent)
    for severance_seed in config.severance_seeds:
        for mode in config.modes:
            for severity in config.severities:
                for motif in targets:
                    site = max(motif.carrier) if motif.carrier else -1
                    if site < 0 or not motif.support_cut:
                        continue
                    for fraction in config.threshold_fractions:
                        for semantics in config.family_semantics:
                            row = evaluate_native_overlap_certified_family(
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
                            row["run_seed"] = seed
                            yield row
                            if config.include_parent_shared_baseline and mode in CERTIFICATION_MODES:
                                base = evaluate_native_overlap_certified_family(
                                    state, motif, site,
                                    threshold_fraction=fraction,
                                    family_semantics=semantics,
                                    mode=mode,
                                    severity=float(severity),
                                    seed=int(severance_seed),
                                    weights=weights,
                                    weight_profile=config.overlap_weight_profile,
                                    parent_shared_baseline=True,
                                )
                                base["run_seed"] = seed
                                yield base


def _bool_count(rows: Sequence[Mapping[str, object]], key: str) -> int:
    return sum(1 for r in rows if bool(r.get(key)))


def aggregate_native_overlap_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float, str, str], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((
            str(r["native_certification_regime"]),
            str(r["mode"]),
            str(r["family_semantics"]),
            float(r["severity"]),
            float(r["threshold_fraction"]),
            str(r["native_overlap_bin"]),
            str(r["overlap_weight_profile"]),
        ), []).append(r)
    out: List[Dict[str, object]] = []
    for (native_regime, mode, semantics, severity, threshold, overlap_bin, profile), items in sorted(buckets.items()):
        valid = [r for r in items if bool(r.get("comparison_valid_strict_vs_family"))]
        deltas = [float(r.get("apples_to_apples_loss_delta")) for r in valid if r.get("apples_to_apples_loss_delta") not in (None, "")]
        out.append({
            "native_certification_regime": native_regime,
            "mode": mode,
            "family_semantics": semantics,
            "severity": severity,
            "threshold_fraction": threshold,
            "native_overlap_bin": overlap_bin,
            "overlap_weight_profile": profile,
            "samples": len(items),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "mean_weighted_native_overlap": _mean([float(r.get("weighted_native_overlap", 0.0)) for r in items]),
            "mean_induced_certificate_correlation": _mean([float(r.get("induced_certificate_correlation", 0.0)) for r in items]),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "comparison_valid_rate": _rate(items, "comparison_valid_strict_vs_family"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
            "mean_apples_to_apples_loss_delta": _mean(deltas),
        })
    return out


def component_overlap_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, float, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        if str(r.get("native_certification_regime")) != "native_overlap_induced":
            continue
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), float(r["severity"]), float(r["threshold_fraction"]), int(r["support_width"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, severity, threshold, width), items in sorted(buckets.items()):
        row: Dict[str, object] = {
            "mode": mode,
            "family_semantics": semantics,
            "severity": severity,
            "threshold_fraction": threshold,
            "support_width": width,
            "samples": len(items),
            "mean_weighted_native_overlap": _mean([float(r.get("weighted_native_overlap", 0.0)) for r in items]),
            "mean_induced_certificate_correlation": _mean([float(r.get("induced_certificate_correlation", 0.0)) for r in items]),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
        }
        for c in OVERLAP_COMPONENTS:
            row[f"mean_{c}_overlap"] = _mean([float(r.get(f"{c}_overlap", 0.0)) for r in items])
        out.append(row)
    return out


def rescue_by_native_overlap_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if str(r.get("native_certification_regime")) == "native_overlap_induced" and bool(r.get("certification_mode")) and float(r.get("severity", 0.0)) > 0]
    buckets: Dict[Tuple[str, str, str], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), str(r["native_overlap_bin"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, bin_name), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "native_overlap_bin": bin_name,
            "samples": len(items),
            "mean_induced_certificate_correlation": _mean([float(r.get("induced_certificate_correlation", 0.0)) for r in items]),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
        })
    return out


def overlap_signature_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    """Summarize whether rescue declines from low to high native overlap."""
    rb = rescue_by_native_overlap_rows(rows)
    grouped: Dict[Tuple[str, str], Dict[str, Mapping[str, object]]] = {}
    for r in rb:
        grouped.setdefault((str(r["mode"]), str(r["family_semantics"])), {})[str(r["native_overlap_bin"])] = r
    out: List[Dict[str, object]] = []
    for (mode, semantics), by_bin in sorted(grouped.items()):
        low = float(by_bin.get("low", {}).get("certification_rescue_rate", 0.0)) if "low" in by_bin else None
        med = float(by_bin.get("medium", {}).get("certification_rescue_rate", 0.0)) if "medium" in by_bin else None
        high = float(by_bin.get("high", {}).get("certification_rescue_rate", 0.0)) if "high" in by_bin else None
        available = [x for x in (low, med, high) if x is not None]
        monotone = True
        if low is not None and med is not None and med > low + 1e-12: monotone = False
        if med is not None and high is not None and high > med + 1e-12: monotone = False
        if low is not None and high is not None and high > low + 1e-12: monotone = False
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "low_overlap_rescue_rate": "" if low is None else low,
            "medium_overlap_rescue_rate": "" if med is None else med,
            "high_overlap_rescue_rate": "" if high is None else high,
            "low_minus_high_rescue": "" if (low is None or high is None) else round(low - high, 6),
            "monotone_nonincreasing_by_overlap_bin": monotone,
            "bin_count": len(available),
        })
    return out


def selector_guardrail_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if str(r.get("mode")) == "selector_stress"]
    buckets: Dict[Tuple[str, str], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["native_certification_regime"]), str(r["family_semantics"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (regime, semantics), items in sorted(buckets.items()):
        bad = any(bool(r.get("certification_rescue_event")) or bool(r.get("family_certification_resilience_event")) for r in items)
        out.append({
            "native_certification_regime": regime,
            "family_semantics": semantics,
            "samples": len(items),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "selector_guardrail_passed": not bad,
        })
    return out


def run_native_certificate_overlap(config: NativeCertificateOverlapConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    for seed in config.seeds:
        seed_rows = list(iter_native_overlap_rows_for_seed(config, seed))
        all_rows.extend(seed_rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(seed_rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in seed_rows}),
            "overlap_bins": sorted({str(r.get("native_overlap_bin")) for r in seed_rows}),
            "mean_induced_certificate_correlation": _mean([float(r.get("induced_certificate_correlation", 0.0)) for r in seed_rows]),
            "certification_rescue_rate": _rate(seed_rows, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(seed_rows, "family_certification_resilience_event"),
        })
    elapsed = time.perf_counter() - started
    aggregate = aggregate_native_overlap_rows(all_rows)
    comp = component_overlap_rows(all_rows)
    rescue = rescue_by_native_overlap_rows(all_rows)
    signature = overlap_signature_rows(all_rows)
    selectors = selector_guardrail_rows(all_rows)
    native_rows = [r for r in all_rows if str(r.get("native_certification_regime")) == "native_overlap_induced"]
    cert_native = [r for r in native_rows if bool(r.get("certification_mode")) and float(r.get("severity", 0.0)) > 0]
    selector_pass = not any(not bool(r.get("selector_guardrail_passed")) for r in selectors)
    valid_deltas = [float(r.get("apples_to_apples_loss_delta")) for r in all_rows if r.get("apples_to_apples_loss_delta") not in (None, "")]
    summary = {
        "version": "0.9",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed else None,
        "support_width_classes": sorted({int(r.get("support_width", 0)) for r in all_rows}),
        "support_width_count": len({int(r.get("support_width", 0)) for r in all_rows}),
        "native_overlap_bins": sorted({str(r.get("native_overlap_bin")) for r in native_rows}),
        "native_overlap_bin_count": len({str(r.get("native_overlap_bin")) for r in native_rows}),
        "mean_induced_certificate_correlation": _mean([float(r.get("induced_certificate_correlation", 0.0)) for r in native_rows]),
        "min_induced_certificate_correlation": min((float(r.get("induced_certificate_correlation", 0.0)) for r in native_rows), default=None),
        "max_induced_certificate_correlation": max((float(r.get("induced_certificate_correlation", 0.0)) for r in native_rows), default=None),
        "certification_rescues": _bool_count(all_rows, "certification_rescue_event"),
        "family_certification_resilience_events": _bool_count(all_rows, "family_certification_resilience_event"),
        "native_certification_rescue_rate": _rate(cert_native, "certification_rescue_event"),
        "native_family_certification_resilience_rate": _rate(cert_native, "family_certification_resilience_event"),
        "comparison_valid_rate": _rate(all_rows, "comparison_valid_strict_vs_family"),
        "metric_artifact_risk_rate": _rate(all_rows, "metric_artifact_risk"),
        "mean_valid_apples_to_apples_loss_delta": _mean(valid_deltas),
        "selector_guardrail_passed": selector_pass,
        "overlap_signature_rows": len(signature),
        "overlap_signature_monotone_count": sum(1 for r in signature if bool(r.get("monotone_nonincreasing_by_overlap_bin"))),
    }
    return summary, run_rows, aggregate, comp, rescue, signature, selectors, all_rows[: config.sample_limit], all_rows


def write_prediction_note(summary: Mapping[str, object], rescue: Sequence[Mapping[str, object]], signature: Sequence[Mapping[str, object]], selectors: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    best = sorted(rescue, key=lambda r: float(r.get("certification_rescue_rate") or 0.0), reverse=True)[:12]
    failing = [r for r in signature if not bool(r.get("monotone_nonincreasing_by_overlap_bin")) and int(r.get("bin_count", 0)) >= 2]
    selector_failures = [r for r in selectors if not bool(r.get("selector_guardrail_passed"))]
    lines = [
        "# RA Native Certificate Overlap — v0.9",
        "",
        "This workbench replaces the external v0.8 certificate-correlation knob with a native overlap calculation over support-family member certificate witnesses.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        f"- native_overlap_bins: {summary.get('native_overlap_bins')}",
        f"- induced_certificate_correlation range: {summary.get('min_induced_certificate_correlation')}..{summary.get('max_induced_certificate_correlation')}",
        "",
        "## Highest native-overlap-induced certification rescue rows",
        "",
    ]
    if not best:
        lines.append("- No native-overlap-induced certification rescue rows observed.")
    for r in best:
        lines.append(
            f"- mode={r['mode']} semantics={r['family_semantics']} bin={r['native_overlap_bin']} "
            f"corr_mean={r['mean_induced_certificate_correlation']}: cert_rescue={r['certification_rescue_rate']} "
            f"resilience={r['family_certification_resilience_rate']} loss={r['family_internal_loss_rate']}"
        )
    lines += [
        "",
        "## Overlap signature",
        "",
        f"- signature rows: {summary.get('overlap_signature_rows')}",
        f"- monotone non-increasing by overlap bin: {summary.get('overlap_signature_monotone_count')}",
    ]
    if failing:
        lines.append("- Non-monotone bin signatures observed; inspect finite-sample and bin-population effects:")
        for r in failing[:10]:
            lines.append(f"  - mode={r['mode']} semantics={r['family_semantics']} low={r['low_overlap_rescue_rate']} medium={r['medium_overlap_rescue_rate']} high={r['high_overlap_rescue_rate']}")
    else:
        lines.append("- No non-monotone overlap-bin signatures with at least two populated bins were observed.")
    lines += ["", "## Selector guardrail", ""]
    if selector_failures:
        lines.append(f"- WARNING: selector guardrail failures observed: {len(selector_failures)} rows.")
    else:
        lines.append("- Selector stress produced no certification-rescue or family-certification-resilience events.")
    lines += [
        "",
        "## RAKB caution",
        "",
        "The native-overlap calculation is an operational bridge, not yet a derived BDG-LLC law. The intended RA-native claim is structural: certification-level resilience should depend on member-witness distinctness, and native overlap is a candidate proxy for shared failure fate.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(summary: Mapping[str, object], runs: Sequence[Mapping[str, object]], aggregate: Sequence[Mapping[str, object]], comp: Sequence[Mapping[str, object]], rescue: Sequence[Mapping[str, object]], signature: Sequence[Mapping[str, object]], selectors: Sequence[Mapping[str, object]], sample: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "version": "0.9",
        "summary": dict(summary),
        "runs": list(runs),
        "aggregate": list(aggregate),
        "component_overlap": list(comp),
        "rescue_by_native_overlap": list(rescue),
        "overlap_signature": list(signature),
        "selector_guardrail": list(selectors),
        "sample": list(sample),
    }, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.9 native certificate-overlap workbench.")
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=21)
    p.add_argument("--seed-list", default=None)
    p.add_argument("--steps", type=int, default=16)
    p.add_argument("--max-parents", type=int, default=4)
    p.add_argument("--target-frontier-min", type=int, default=5)
    p.add_argument("--branch-probability", type=float, default=0.42)
    p.add_argument("--wide-join-probability", type=float, default=0.72)
    p.add_argument("--conflict-rate", type=float, default=0.22)
    p.add_argument("--defect-rate", type=float, default=0.02)
    p.add_argument("--orientation-defect-rate", type=float, default=0.02)
    p.add_argument("--conflict-witness-defect-rate", type=float, default=0.08)
    p.add_argument("--severance-seeds", default="101,103")
    p.add_argument("--severities", default="0.0,0.25,0.5,0.75,1.0")
    p.add_argument("--modes", default="ledger_failure,orientation_degradation,selector_stress")
    p.add_argument("--threshold-fractions", default="1.0,0.75,0.5,0.25")
    p.add_argument("--family-semantics", default="at_least_k,augmented_exact_k")
    p.add_argument("--overlap-weight-profile", default="balanced", choices=("balanced", "support_heavy", "certificate_heavy"))
    p.add_argument("--correlation-exponent", type=float, default=1.0)
    p.add_argument("--no-parent-shared-baseline", action="store_true")
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=8)
    p.add_argument("--sample-limit", type=int, default=1000)
    p.add_argument("--output-dir", default="outputs")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    config = NativeCertificateOverlapConfig.from_args(args)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary, runs, aggregate, comp, rescue, signature, selectors, sample, _all = run_native_certificate_overlap(config)
    rows_to_csv([summary], output_dir / "ra_native_certificate_overlap_summary_v0_9.csv")
    rows_to_csv(runs, output_dir / "ra_native_certificate_overlap_runs_v0_9.csv")
    rows_to_csv(aggregate, output_dir / "ra_native_certificate_overlap_aggregate_v0_9.csv")
    rows_to_csv(comp, output_dir / "ra_witness_overlap_components_v0_9.csv")
    rows_to_csv(rescue, output_dir / "ra_cert_rescue_by_native_overlap_v0_9.csv")
    rows_to_csv(signature, output_dir / "ra_overlap_induced_correlation_curve_v0_9.csv")
    rows_to_csv(selectors, output_dir / "ra_native_certificate_overlap_selector_guardrail_v0_9.csv")
    rows_to_csv(sample, output_dir / "ra_native_certificate_overlap_evaluations_sample_v0_9.csv")
    write_prediction_note(summary, rescue, signature, selectors, output_dir / "ra_native_cert_overlap_predictions_v0_9.md")
    write_state(summary, runs, aggregate, comp, rescue, signature, selectors, sample, output_dir / "ra_native_certificate_overlap_state_v0_9.json")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
