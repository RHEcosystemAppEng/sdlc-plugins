# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering with the following logic:

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

For `?threshold=high`, `threshold_idx` resolves to `1`. Tracing each condition:

- `critical`: always included (correct)
- `high`: `1 <= 1` evaluates to `true` -- included (correct)
- `medium`: `1 <= 2` evaluates to `true` -- included (INCORRECT: should be zeroed)
- `low`: `1 <= 3` evaluates to `true` -- included (INCORRECT: should be zeroed)

The comparison logic is inverted. The condition `threshold_idx <= N` checks whether the threshold's rank is at or above the severity's rank, but the intent is the opposite: each severity should be included only if its rank is at or above the threshold. The correct condition would be `N <= threshold_idx` (i.e., `1 <= threshold_idx` for high, `2 <= threshold_idx` for medium, etc.) or equivalently `threshold_idx >= N`.

Additionally, the `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low`, which sums the unfiltered counts. Even if the per-severity filtering were corrected, the total would not reflect the filtered result.

Both issues cause this criterion to fail: with `?threshold=high`, the response would still include medium and low counts, and the total would not match the filtered severities.
