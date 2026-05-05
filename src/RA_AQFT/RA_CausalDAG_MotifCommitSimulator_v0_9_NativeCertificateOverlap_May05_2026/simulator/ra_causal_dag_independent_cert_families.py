#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.8 independent certified support families.

v0.7 introduced support-cut families. v0.7.2 repaired the metrics by separating
strict-parent rescue from family-internal resilience. v0.8 asks the next
RA-native question: when can support-family alternatives rescue certification
channels themselves?

The answer should not be smuggled in through threshold subcuts alone. v0.8 adds
an explicit certification-witness regime:

  parent_shared
      one parent certificate gates the strict parent cut and every family member.

  cut_level
      family-member cuts are targeted as a set, matching the v0.7/v0.7.2 audit
      regime and preserving the parent-in-family comparability flag.

  independent_member
      each family member, and the strict parent cut, carries its own certificate
      fate. A certificate-correlation parameter interpolates between independent
      member failures and fully shared failure.

This remains a disciplined simulator layer, not a derived law of Nature. It is
intended to test whether certification-level redundancy is possible once family
members have distinct ledger/orientation witnesses.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterator, List, Mapping, Optional, Sequence, Tuple

try:
    from .ra_causal_dag_simulator import (
        MotifCandidate,
        SupportCut,
        min_finality_depth,
        motif_site,
        readiness_recovery_length,
        rows_to_csv,
        remove_edges,
    )
    from .ra_causal_dag_channel_workbench import (
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        causal_edges_inside_site_past,
        choose_fraction,
        target_motifs_for_channel_severance,
    )
    from .ra_causal_dag_support_family_workbench import (
        FamilyInterventionState,
        SupportCutFamily,
        _family_recovery_length,
        _intervention_state,
        _rng_for,
        family_ready_at,
        strict_ready_at,
    )
    from .ra_causal_dag_support_family_monotonicity import (
        CERTIFICATION_MODES,
        FAMILY_SEMANTICS,
        support_family_by_semantics,
        family_includes_strict_cut,
    )
except ImportError:
    from ra_causal_dag_simulator import (  # type: ignore
        MotifCandidate,
        SupportCut,
        min_finality_depth,
        motif_site,
        readiness_recovery_length,
        rows_to_csv,
        remove_edges,
    )
    from ra_causal_dag_channel_workbench import (  # type: ignore
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        causal_edges_inside_site_past,
        choose_fraction,
        target_motifs_for_channel_severance,
    )
    from ra_causal_dag_support_family_workbench import (  # type: ignore
        FamilyInterventionState,
        SupportCutFamily,
        _family_recovery_length,
        _intervention_state,
        _rng_for,
        family_ready_at,
        strict_ready_at,
    )
    from ra_causal_dag_support_family_monotonicity import (  # type: ignore
        CERTIFICATION_MODES,
        FAMILY_SEMANTICS,
        support_family_by_semantics,
        family_includes_strict_cut,
    )


CERTIFICATION_REGIMES_V08: Tuple[str, ...] = ("parent_shared", "cut_level", "independent_member")
DEFAULT_CERTIFICATE_CORRELATIONS: Tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.0)


@dataclass(frozen=True)
class IndependentCertifiedFamilyConfig:
    """Parameters for the v0.8 independent certified-family workbench."""

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
    modes: Tuple[str, ...] = SEVERANCE_MODES
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.50, 0.25)
    family_semantics: Tuple[str, ...] = ("at_least_k", "augmented_exact_k")
    certification_regimes: Tuple[str, ...] = CERTIFICATION_REGIMES_V08
    certificate_correlations: Tuple[float, ...] = DEFAULT_CERTIFICATE_CORRELATIONS
    include_alternatives: bool = False
    max_targets: Optional[int] = 8
    sample_limit: int = 1000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "IndependentCertifiedFamilyConfig":
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
            certification_regimes=tuple(x.strip() for x in args.certification_regimes.split(",") if x.strip()),
            certificate_correlations=tuple(float(x) for x in args.certificate_correlations.split(",") if x.strip()),
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


@dataclass(frozen=True)
class CertificationFailureState:
    """Certification failures for strict parent and family-member cuts."""

    strict_parent_uncertified: bool
    uncertified_family_cuts: FrozenSet[SupportCut]
    regime: str
    correlation: float
    shared_failure_used: bool
    shared_failure_value: bool
    detail: str

    @property
    def uncertified_family_cut_count(self) -> int:
        return len(self.uncertified_family_cuts)


def _rate(rows: Sequence[Mapping[str, object]], key: str) -> float:
    return round(sum(1 for r in rows if bool(r.get(key))) / len(rows), 6) if rows else 0.0


def _mean(values: Sequence[float]) -> Optional[float]:
    return round(sum(values) / len(values), 6) if values else None


def _num(rows: Sequence[Mapping[str, object]], key: str) -> List[float]:
    out: List[float] = []
    for r in rows:
        value = r.get(key)
        if value not in (None, ""):
            out.append(float(value))
    return out


def _cert_rng(motif: MotifCandidate, site: int, mode: str, severity: float, seed: int, regime: str, correlation: float, salt: int = 113) -> random.Random:
    return random.Random(
        seed
        + 7919 * site
        + 104729 * len(motif.support_cut)
        + 15485863 * salt
        + int(severity * 10000)
        + int(correlation * 1000) * 32452843
        + sum(ord(c) for c in motif.name + mode + regime)
    )


def _choose_family_cuts(family: SupportCutFamily, severity: float, rng: random.Random) -> FrozenSet[SupportCut]:
    if severity <= 0 or not family.cuts:
        return frozenset()
    chosen = choose_fraction(list(family.cuts), severity, rng)
    return frozenset(chosen)


def _certification_failure_state(
    motif: MotifCandidate,
    family: SupportCutFamily,
    site: int,
    *,
    mode: str,
    severity: float,
    seed: int,
    certification_regime: str,
    certificate_correlation: float,
) -> CertificationFailureState:
    """Generate certification failures for a support-family row.

    The independent-member regime preserves a fixed marginal failure probability
    `severity` for each certificate while interpolating between independent and
    shared failure fate via `certificate_correlation`.
    """
    if mode not in CERTIFICATION_MODES or severity <= 0:
        return CertificationFailureState(False, frozenset(), certification_regime, certificate_correlation, False, False, "no_certification_stress")

    if certification_regime not in CERTIFICATION_REGIMES_V08:
        raise ValueError(f"unknown certification regime: {certification_regime}")
    c = max(0.0, min(1.0, float(certificate_correlation)))
    rng = _cert_rng(motif, site, mode, float(severity), int(seed), certification_regime, c)

    if certification_regime == "parent_shared":
        failed = bool(rng.random() < severity)
        return CertificationFailureState(
            strict_parent_uncertified=failed,
            uncertified_family_cuts=frozenset(family.cuts) if failed else frozenset(),
            regime=certification_regime,
            correlation=1.0,
            shared_failure_used=True,
            shared_failure_value=failed,
            detail=f"parent_shared_certificate_failed={failed}",
        )

    if certification_regime == "cut_level":
        uncertified = _choose_family_cuts(family, severity, rng)
        return CertificationFailureState(
            strict_parent_uncertified=motif.support_cut in uncertified,
            uncertified_family_cuts=uncertified,
            regime=certification_regime,
            correlation=c,
            shared_failure_used=False,
            shared_failure_value=False,
            detail=f"cut_level_uncertified_family_cuts={len(uncertified)}",
        )

    # independent_member: the parent cut and every family member have an explicit
    # certificate fate.  Correlation is modeled as a mixture between a shared fate
    # draw and independent per-cut draws, preserving each cut's marginal failure
    # probability at `severity`.
    domain = sorted(set(family.cuts).union({motif.support_cut}), key=lambda cut: (len(cut), tuple(sorted(cut))))
    use_shared = bool(rng.random() < c)
    shared_failed = bool(rng.random() < severity) if use_shared else False
    failures = set()
    for cut in domain:
        if use_shared:
            failed = shared_failed
        else:
            # stable per-cut jitter through the same RNG stream; deterministic
            # for the row but independent across cuts under the mixture branch.
            failed = bool(rng.random() < severity)
        if failed:
            failures.add(cut)
    uncertified_family = frozenset(cut for cut in family.cuts if cut in failures)
    strict_failed = motif.support_cut in failures
    return CertificationFailureState(
        strict_parent_uncertified=strict_failed,
        uncertified_family_cuts=uncertified_family,
        regime=certification_regime,
        correlation=c,
        shared_failure_used=use_shared,
        shared_failure_value=shared_failed,
        detail=(
            f"independent_member domain={len(domain)} uncertified_family_cuts={len(uncertified_family)} "
            f"strict_parent_uncertified={strict_failed} correlation={c} shared_used={use_shared} shared_failed={shared_failed}"
        ),
    )


def _non_cert_intervention_state(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    family: SupportCutFamily,
    *,
    mode: str,
    severity: float,
    seed: int,
) -> FamilyInterventionState:
    if mode in CERTIFICATION_MODES:
        return FamilyInterventionState(
            after_dag=state.dag,
            unavailable_support=frozenset(),
            uncertified_cuts=frozenset(),
            delay_depth=0,
            selector_stress=False,
            affected_edges=(),
            detail="certification_state_supplied_separately",
        )
    return _intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)


def evaluate_independent_certified_family(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    *,
    threshold_fraction: float,
    family_semantics: str,
    certification_regime: str,
    certificate_correlation: float,
    mode: str,
    severity: float,
    seed: int,
) -> Dict[str, object]:
    family = support_family_by_semantics(motif, threshold_fraction, family_semantics)
    before_strict = strict_ready_at(state.dag, motif.support_cut, site)
    before_family = family_ready_at(state.dag, family, site)
    intervention = _non_cert_intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)
    cert_state = _certification_failure_state(
        motif,
        family,
        site,
        mode=mode,
        severity=severity,
        seed=seed,
        certification_regime=certification_regime,
        certificate_correlation=certificate_correlation,
    )
    combined_uncertified = frozenset(set(intervention.uncertified_cuts).union(cert_state.uncertified_family_cuts))
    strict_uncertified = bool(cert_state.strict_parent_uncertified or motif.support_cut in intervention.uncertified_cuts)

    after_strict = strict_ready_at(
        intervention.after_dag,
        motif.support_cut,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=strict_uncertified,
        delay_depth=intervention.delay_depth,
    )
    after_family = family_ready_at(
        intervention.after_dag,
        family,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=combined_uncertified,
        delay_depth=intervention.delay_depth,
    )

    strict_loss = before_strict and not after_strict
    family_loss = before_family and not after_family
    strict_rescue = strict_loss and after_family
    family_internal_survival = before_family and after_family
    cert_mode = mode in CERTIFICATION_MODES
    cert_rescue = cert_mode and bool(cert_state.strict_parent_uncertified) and after_family
    family_cert_resilience = cert_mode and severity > 0 and family_internal_survival

    # Comparability from v0.7.2: cut-level certification can target family cuts
    # while leaving the strict parent outside the target domain when exact-k omits it.
    parent_in_family = family_includes_strict_cut(family)
    metric_artifact_risk = cert_mode and certification_regime == "cut_level" and not parent_in_family and severity > 0
    comparison_valid = not metric_artifact_risk
    apples_delta: object = int(family_loss) - int(strict_loss) if comparison_valid else ""
    certified_member_count = max(family.family_size - len(combined_uncertified), 0)
    finality_before = min_finality_depth(state.dag, motif.support_cut)
    finality_after = min_finality_depth(intervention.after_dag, motif.support_cut)
    if intervention.delay_depth and finality_after is not None:
        finality_after += intervention.delay_depth
    strict_recovery = readiness_recovery_length(
        intervention.after_dag,
        motif.support_cut,
        site,
        unavailable_support=intervention.unavailable_support,
        delay_depth=intervention.delay_depth,
    )
    family_recovery = _family_recovery_length(
        intervention.after_dag,
        family,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=combined_uncertified,
        delay_depth=intervention.delay_depth,
    )

    return {
        "motif": motif.name,
        "site": site,
        "run_seed": "",
        "seed": seed,
        "mode": mode,
        "severity": float(severity),
        "support_width": len(motif.support_cut),
        "threshold_fraction": float(threshold_fraction),
        "threshold_k": family.threshold_k,
        "family_semantics": family_semantics,
        "certification_regime": certification_regime,
        "certificate_correlation": max(0.0, min(1.0, float(certificate_correlation))),
        "family_size": family.family_size,
        "parent_cut_in_family": parent_in_family,
        "strict_before_ready": before_strict,
        "family_before_ready": before_family,
        "strict_after_ready": after_strict,
        "family_after_ready": after_family,
        "strict_parent_loss": strict_loss,
        "family_internal_loss": family_loss,
        "strict_rescue_event": strict_rescue,
        "family_internal_survival": family_internal_survival,
        "certification_mode": cert_mode,
        "strict_parent_cert_failed": cert_state.strict_parent_uncertified,
        "certification_rescue_event": cert_rescue,
        "family_certification_resilience_event": family_cert_resilience,
        "shared_failure_used": cert_state.shared_failure_used,
        "shared_failure_value": cert_state.shared_failure_value,
        "comparison_valid_strict_vs_family": comparison_valid,
        "metric_artifact_risk": metric_artifact_risk,
        "apples_to_apples_loss_delta": apples_delta,
        "uncertified_family_cut_count": len(combined_uncertified),
        "certified_family_member_count": certified_member_count,
        "uncertified_family_member_fraction": round(len(combined_uncertified) / family.family_size, 6) if family.family_size else 0.0,
        "unavailable_support_count": len(intervention.unavailable_support),
        "affected_edge_count": len(intervention.affected_edges),
        "delay_depth": intervention.delay_depth,
        "selector_stress": intervention.selector_stress,
        "strict_finality_depth_before": finality_before,
        "strict_finality_depth_after": finality_after,
        "strict_recovery_length": strict_recovery,
        "family_recovery_length": family_recovery,
        "intervention_detail": intervention.detail,
        "certification_detail": cert_state.detail,
    }


def iter_independent_cert_rows_for_seed(config: IndependentCertifiedFamilyConfig, seed: int) -> Iterator[Dict[str, object]]:
    state = build_channel_seed_state(config.channel_config(seed), seed)
    targets = target_motifs_for_channel_severance(state.motifs, include_alternatives=config.include_alternatives, max_targets=config.max_targets)
    for severance_seed in config.severance_seeds:
        for mode in config.modes:
            for severity in config.severities:
                for motif in targets:
                    site = motif_site(motif)
                    if site < 0 or not motif.support_cut:
                        continue
                    for fraction in config.threshold_fractions:
                        for semantics in config.family_semantics:
                            for regime in config.certification_regimes:
                                correlations = config.certificate_correlations if mode in CERTIFICATION_MODES else (0.0,)
                                for corr in correlations:
                                    row = evaluate_independent_certified_family(
                                        state,
                                        motif,
                                        site,
                                        threshold_fraction=fraction,
                                        family_semantics=semantics,
                                        certification_regime=regime,
                                        certificate_correlation=corr,
                                        mode=mode,
                                        severity=float(severity),
                                        seed=int(severance_seed),
                                    )
                                    row["run_seed"] = seed
                                    yield row


def aggregate_independent_cert_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((
            str(r["family_semantics"]),
            str(r["certification_regime"]),
            str(r["mode"]),
            float(r["severity"]),
            float(r["threshold_fraction"]),
            float(r["certificate_correlation"]),
        ), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, mode, severity, threshold, corr), items in sorted(buckets.items()):
        valid = [r for r in items if bool(r.get("comparison_valid_strict_vs_family"))]
        deltas = [float(r.get("apples_to_apples_loss_delta")) for r in valid if r.get("apples_to_apples_loss_delta") not in (None, "")]
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "mode": mode,
            "severity": severity,
            "threshold_fraction": threshold,
            "certificate_correlation": corr,
            "samples": len(items),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "parent_in_family_rate": _rate(items, "parent_cut_in_family"),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "strict_rescue_rate": _rate(items, "strict_rescue_event"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
            "strict_parent_cert_failure_rate": _rate(items, "strict_parent_cert_failed"),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "comparison_valid_rate": _rate(items, "comparison_valid_strict_vs_family"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
            "mean_apples_to_apples_loss_delta": _mean(deltas),
            "mean_certified_family_member_count": _mean([float(r.get("certified_family_member_count", 0)) for r in items]),
            "mean_uncertified_family_member_fraction": _mean([float(r.get("uncertified_family_member_fraction", 0.0)) for r in items]),
        })
    return out


def certification_correlation_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if bool(r.get("certification_mode")) and float(r.get("severity", 0.0)) > 0]
    buckets: Dict[Tuple[str, str, str, float, float, float], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((
            str(r["mode"]),
            str(r["family_semantics"]),
            str(r["certification_regime"]),
            float(r["severity"]),
            float(r["threshold_fraction"]),
            float(r["certificate_correlation"]),
        ), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, regime, severity, threshold, corr), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "certification_regime": regime,
            "severity": severity,
            "threshold_fraction": threshold,
            "certificate_correlation": corr,
            "samples": len(items),
            "family_size_mean": _mean([float(r.get("family_size", 0)) for r in items]),
            "strict_parent_cert_failure_rate": _rate(items, "strict_parent_cert_failed"),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
            "mean_certified_family_member_count": _mean([float(r.get("certified_family_member_count", 0)) for r in items]),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
        })
    return out


def regime_comparison_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if bool(r.get("certification_mode")) and float(r.get("severity", 0.0)) > 0]
    buckets: Dict[Tuple[str, str, float, float], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), float(r["severity"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, severity, threshold), items in sorted(buckets.items()):
        by_regime: Dict[str, List[Mapping[str, object]]] = {}
        for r in items:
            by_regime.setdefault(str(r["certification_regime"]), []).append(r)
        row: Dict[str, object] = {
            "mode": mode,
            "family_semantics": semantics,
            "severity": severity,
            "threshold_fraction": threshold,
            "samples": len(items),
        }
        for regime in CERTIFICATION_REGIMES_V08:
            ritems = by_regime.get(regime, [])
            row[f"{regime}_certification_rescue_rate"] = _rate(ritems, "certification_rescue_event")
            row[f"{regime}_family_certification_resilience_rate"] = _rate(ritems, "family_certification_resilience_event")
            row[f"{regime}_family_loss_rate"] = _rate(ritems, "family_internal_loss")
        row["independent_minus_parent_rescue"] = round(float(row.get("independent_member_certification_rescue_rate") or 0.0) - float(row.get("parent_shared_certification_rescue_rate") or 0.0), 6)
        row["independent_minus_cut_level_resilience"] = round(float(row.get("independent_member_family_certification_resilience_rate") or 0.0) - float(row.get("cut_level_family_certification_resilience_rate") or 0.0), 6)
        out.append(row)
    return out


def width_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((
            str(r["mode"]),
            str(r["family_semantics"]),
            str(r["certification_regime"]),
            float(r["severity"]),
            float(r["threshold_fraction"]),
            float(r["certificate_correlation"]),
            int(r["support_width"]),
        ), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, regime, severity, threshold, corr, width), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "certification_regime": regime,
            "severity": severity,
            "threshold_fraction": threshold,
            "certificate_correlation": corr,
            "support_width": width,
            "samples": len(items),
            "family_size_mean": _mean([float(r.get("family_size", 0)) for r in items]),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "mean_certified_family_member_count": _mean([float(r.get("certified_family_member_count", 0)) for r in items]),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
        })
    return out


def selector_guardrail_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if str(r.get("mode")) == "selector_stress"]
    buckets: Dict[Tuple[str, str, float], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, threshold), items in sorted(buckets.items()):
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "threshold_fraction": threshold,
            "samples": len(items),
            "strict_rescue_rate": _rate(items, "strict_rescue_event"),
            "family_certification_resilience_rate": _rate(items, "family_certification_resilience_event"),
            "certification_rescue_rate": _rate(items, "certification_rescue_event"),
            "selector_guardrail_passed": not any(bool(r.get("strict_rescue_event")) or bool(r.get("family_certification_resilience_event")) or bool(r.get("certification_rescue_event")) for r in items),
        })
    return out


def run_independent_certified_families(config: IndependentCertifiedFamilyConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    for seed in config.seeds:
        seed_rows = list(iter_independent_cert_rows_for_seed(config, seed))
        all_rows.extend(seed_rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(seed_rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in seed_rows}),
            "certification_rescue_rate": _rate(seed_rows, "certification_rescue_event"),
            "family_certification_resilience_rate": _rate(seed_rows, "family_certification_resilience_event"),
            "metric_artifact_risk_rate": _rate(seed_rows, "metric_artifact_risk"),
        })
    elapsed = time.perf_counter() - started
    aggregate = aggregate_independent_cert_rows(all_rows)
    corr = certification_correlation_rows(all_rows)
    regimes = regime_comparison_rows(all_rows)
    widths = width_rows(all_rows)
    selectors = selector_guardrail_rows(all_rows)
    valid_deltas = [float(r.get("apples_to_apples_loss_delta")) for r in all_rows if r.get("apples_to_apples_loss_delta") not in (None, "")]
    summary = {
        "version": "0.8",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed else None,
        "support_width_classes": sorted({int(r.get("support_width", 0)) for r in all_rows}),
        "support_width_count": len({int(r.get("support_width", 0)) for r in all_rows}),
        "family_semantics": sorted({str(r.get("family_semantics")) for r in all_rows}),
        "certification_regimes": sorted({str(r.get("certification_regime")) for r in all_rows}),
        "certificate_correlations": sorted({float(r.get("certificate_correlation", 0.0)) for r in all_rows}),
        "threshold_fractions": sorted({float(r.get("threshold_fraction", 0.0)) for r in all_rows}),
        "strict_parent_losses": sum(1 for r in all_rows if bool(r.get("strict_parent_loss"))),
        "family_internal_losses": sum(1 for r in all_rows if bool(r.get("family_internal_loss"))),
        "strict_rescues": sum(1 for r in all_rows if bool(r.get("strict_rescue_event"))),
        "certification_rescues": sum(1 for r in all_rows if bool(r.get("certification_rescue_event"))),
        "family_certification_resilience_events": sum(1 for r in all_rows if bool(r.get("family_certification_resilience_event"))),
        "metric_artifact_risk_events": sum(1 for r in all_rows if bool(r.get("metric_artifact_risk"))),
        "comparison_valid_rate": _rate(all_rows, "comparison_valid_strict_vs_family"),
        "metric_artifact_risk_rate": _rate(all_rows, "metric_artifact_risk"),
        "mean_valid_apples_to_apples_loss_delta": _mean(valid_deltas),
    }
    return summary, run_rows, aggregate, corr, regimes, widths, selectors, all_rows[: config.sample_limit], all_rows


def write_prediction_note(summary: Mapping[str, object], corr: Sequence[Mapping[str, object]], regimes: Sequence[Mapping[str, object]], selectors: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    independent_rows = [r for r in corr if str(r.get("certification_regime")) == "independent_member" and float(r.get("severity", 0.0)) > 0]
    best_rescue = sorted(independent_rows, key=lambda r: float(r.get("certification_rescue_rate") or 0.0), reverse=True)[:10]
    corr_curve = [r for r in independent_rows if float(r.get("threshold_fraction", 0.0)) == 0.5 and float(r.get("severity", 0.0)) == 0.5]
    selector_failures = [r for r in selectors if not bool(r.get("selector_guardrail_passed"))]
    lines = [
        "# RA Independent Certified Support Families — v0.8",
        "",
        "This workbench tests certification-witness redundancy. It distinguishes parent-shared, cut-level, and independent-member certificate regimes and sweeps certificate correlation.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        f"- certification_regimes: {summary.get('certification_regimes')}",
        f"- certificate_correlations: {summary.get('certificate_correlations')}",
        "",
        "## Reading",
        "",
        "Independent-member certification is the first simulator regime in this line that can rescue ledger/orientation certificate failure through alternative certified family members. Parent-shared certification should not rescue a parent-certificate failure, and rescue should decline as certificate correlation approaches one.",
        "",
        "## Highest independent-member certification rescue rows",
        "",
    ]
    if not best_rescue:
        lines.append("- No independent-member certification rescue observed in this run.")
    for r in best_rescue:
        lines.append(
            f"- mode={r['mode']} semantics={r['family_semantics']} sev={r['severity']} threshold={r['threshold_fraction']} "
            f"corr={r['certificate_correlation']}: cert_rescue={r['certification_rescue_rate']} "
            f"family_cert_resilience={r['family_certification_resilience_rate']} loss={r['family_internal_loss_rate']}"
        )
    lines += ["", "## Correlation sweep slice: independent_member, severity=0.5, threshold=0.5", ""]
    if not corr_curve:
        lines.append("- No rows in the default correlation slice.")
    for r in sorted(corr_curve, key=lambda x: (str(x['mode']), float(x['certificate_correlation']))):
        lines.append(
            f"- mode={r['mode']} corr={r['certificate_correlation']}: rescue={r['certification_rescue_rate']} "
            f"resilience={r['family_certification_resilience_rate']} loss={r['family_internal_loss_rate']}"
        )
    lines += ["", "## Selector guardrail", ""]
    if selector_failures:
        lines.append(f"- WARNING: selector guardrail failures observed: {len(selector_failures)} rows.")
    else:
        lines.append("- Selector stress produced no support-family certification rescue events in this run.")
    lines += [
        "",
        "## RAKB caution",
        "",
        "The certification-correlation model is exploratory. The RA-native claim is not that Nature uses this stochastic mechanism; the claim is that certification-level support-family resilience requires member-distinct certificates or equivalent native witnesses rather than a shared parent certificate.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(summary: Mapping[str, object], runs: Sequence[Mapping[str, object]], aggregate: Sequence[Mapping[str, object]], corr: Sequence[Mapping[str, object]], regimes: Sequence[Mapping[str, object]], widths: Sequence[Mapping[str, object]], selectors: Sequence[Mapping[str, object]], sample: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "version": "0.8",
        "summary": dict(summary),
        "runs": list(runs),
        "aggregate": list(aggregate),
        "correlation": list(corr),
        "regime_comparison": list(regimes),
        "widths": list(widths),
        "selector_guardrail": list(selectors),
        "sample": list(sample),
    }, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.8 independent certified support-family workbench.")
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
    p.add_argument("--modes", default=",".join(SEVERANCE_MODES))
    p.add_argument("--threshold-fractions", default="1.0,0.75,0.5,0.25")
    p.add_argument("--family-semantics", default="at_least_k,augmented_exact_k")
    p.add_argument("--certification-regimes", default=",".join(CERTIFICATION_REGIMES_V08))
    p.add_argument("--certificate-correlations", default=",".join(str(x) for x in DEFAULT_CERTIFICATE_CORRELATIONS))
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=8)
    p.add_argument("--sample-limit", type=int, default=1000)
    p.add_argument("--output-dir", default="outputs")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    config = IndependentCertifiedFamilyConfig.from_args(args)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary, runs, aggregate, corr, regimes, widths, selectors, sample, _all_rows = run_independent_certified_families(config)
    rows_to_csv([summary], output_dir / "ra_independent_cert_family_summary_v0_8.csv")
    rows_to_csv(runs, output_dir / "ra_independent_cert_family_runs_v0_8.csv")
    rows_to_csv(aggregate, output_dir / "ra_independent_cert_family_aggregate_v0_8.csv")
    rows_to_csv(corr, output_dir / "ra_certification_correlation_sweep_v0_8.csv")
    rows_to_csv(regimes, output_dir / "ra_certification_resilience_by_regime_v0_8.csv")
    rows_to_csv(widths, output_dir / "ra_independent_cert_family_by_width_v0_8.csv")
    rows_to_csv(selectors, output_dir / "ra_independent_cert_selector_guardrail_v0_8.csv")
    rows_to_csv(sample, output_dir / "ra_independent_cert_family_evaluations_sample_v0_8.csv")
    write_prediction_note(summary, corr, regimes, selectors, output_dir / "ra_independent_cert_family_predictions_v0_8.md")
    write_state(summary, runs, aggregate, corr, regimes, widths, selectors, sample, output_dir / "ra_independent_cert_family_state_v0_8.json")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
