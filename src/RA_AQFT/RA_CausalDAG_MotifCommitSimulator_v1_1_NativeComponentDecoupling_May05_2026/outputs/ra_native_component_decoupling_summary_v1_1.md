# RA v1.1 Native Component Decoupling Summary

## Verdict

`decoupling_audit_reveals_orientation_support_frontier_confounding`

## Key findings

- Support/frontier/orientation triplet status: `orientation_confounded_with_support_frontier`.
- Ledger component resolved: `False`.
- Orientation component resolved: `False`.
- Matched-strata orientation variation available: `False`.
- Matched-strata ledger variation available: `False`.

## Interpretation

v1.1 does not force a false orientation-specific attribution. It confirms that
ledger overlap is decoupled from the support/frontier proxy, while orientation
overlap remains numerically tied to support/frontier in the current component
surface. Therefore orientation-degradation rescue should be described as carried
by a joint support/frontier/orientation proxy until a distinct orientation-link
surface is generated or derived.

## Recommended next step

Define or derive a distinct orientation-link overlap surface from native
orientation witnesses, then rerun the matched-strata audit:

```text
hold support/frontier overlap fixed
vary orientation-link overlap
measure orientation-degradation rescue
```

Until that succeeds, v1.0/v1.1 should retain the caveat:

```text
ledger attribution is clean; orientation attribution is component-anchored but
not yet independently resolved from support/frontier overlap.
```
