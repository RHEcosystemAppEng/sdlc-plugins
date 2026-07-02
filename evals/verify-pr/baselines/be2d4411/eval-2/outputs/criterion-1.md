# Criterion 1: threshold=high returns counts for critical and high only

## Verdict: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Evidence from Diff

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` (lines 41-54 of the diff) implements threshold filtering as follows:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

## Detailed Reasoning

### Bug 1: Inverted comparison logic

For `threshold=high`, `threshold_idx = 1`. The code checks whether `threshold_idx <= N` for each severity's position, but the correct check is whether `N <= threshold_idx` (i.e., whether the severity's rank is at or above the threshold).

Trace for `threshold=high` (idx=1):
- critical: always included (no condition) -- correct
- high: `1 <= 1` = true, included -- correct (coincidental)
- medium: `1 <= 2` = true, included -- **WRONG**, medium should be excluded
- low: `1 <= 3` = true, included -- **WRONG**, low should be excluded

The result is that `threshold=high` returns ALL severity counts, not just critical and high. The comparison is backwards: it should be `severity_position <= threshold_idx`, not `threshold_idx <= severity_position`.

This can also be verified for `threshold=critical` (idx=0): all four severities are included (0 <= 1, 0 <= 2, 0 <= 3 are all true), but only critical should be returned.

### Bug 2: Total uses unfiltered counts

The total field is computed as `summary.critical + summary.high + summary.medium + summary.low`, using the original unfiltered `summary` values rather than the filtered values. Even if the filtering conditions were corrected, the total would still reflect the full unfiltered count.

## Conclusion

The criterion fails due to two bugs: the inverted comparison logic means `threshold=high` includes all four severity levels instead of only critical and high, and the total uses unfiltered values regardless.
