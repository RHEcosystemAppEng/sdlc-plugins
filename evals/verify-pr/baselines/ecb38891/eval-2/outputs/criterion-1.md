# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, but the comparison logic is inverted, causing incorrect filtering results.

### Code Under Review

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

### Analysis

For `threshold=high`, `threshold_idx = 1` (the position of "high" in the `severity_order` array).

Evaluating each field:
- `critical`: always included (hardcoded) -- correct
- `high`: `threshold_idx <= 1` evaluates to `1 <= 1` = true -- included (correct)
- `medium`: `threshold_idx <= 2` evaluates to `1 <= 2` = true -- included (WRONG, should be 0)
- `low`: `threshold_idx <= 3` evaluates to `1 <= 3` = true -- included (WRONG, should be 0)

The condition `threshold_idx <= N` checks "is the threshold severity at or above this severity level", which is the opposite of the intended logic. The correct condition should be `N <= threshold_idx` ("is this severity level at or above the threshold").

With the current code, `threshold=high` returns all four severity counts instead of only critical and high, violating this acceptance criterion.

### Additional Bug

The `total` field is computed from the unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the filtering comparison were corrected, the total would not reflect the filtered counts.
