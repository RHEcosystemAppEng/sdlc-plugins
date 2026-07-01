# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is inverted, causing incorrect results for all threshold values.

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

### Detailed Reasoning

The `severity_order` array assigns indices: critical=0, high=1, medium=2, low=3. For `threshold=high`, `threshold_idx` resolves to 1.

The threshold semantics require "include severities at or above the threshold." Since critical > high > medium > low, `threshold=high` should include only critical (index 0) and high (index 1) -- that is, severities with index <= threshold_idx.

The code's conditions check `threshold_idx <= severity_position`:
- `high`: `threshold_idx <= 1` => `1 <= 1` => true (included -- correct)
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true (included -- **incorrect**, should be excluded)
- `low`: `threshold_idx <= 3` => `1 <= 3` => true (included -- **incorrect**, should be excluded)

The correct condition should be `severity_position <= threshold_idx` (i.e., `1 <= threshold_idx` for high, `2 <= threshold_idx` for medium, `3 <= threshold_idx` for low). With this fix, for `threshold=high` (idx=1):
- `high`: `1 <= 1` => true (included)
- `medium`: `2 <= 1` => false (excluded)
- `low`: `3 <= 1` => false (excluded)

The comparison direction is backwards, causing the filter to include all severities regardless of the threshold value. This means `?threshold=high` returns counts for all four severities, not just critical and high.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values, so even if the filtering were correct, the total would be wrong.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines in the filtered branch
- The comparison `threshold_idx <= N` should be `N <= threshold_idx` (or equivalently, the severity's own index should be compared against the threshold index)
- For any threshold value, the current code includes ALL severities because `threshold_idx` (0-3) is always <= the larger severity position constants
