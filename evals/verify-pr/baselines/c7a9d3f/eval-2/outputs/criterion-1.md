# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

This criterion requires that when `threshold=high` is provided, the response should contain counts only for `critical` and `high` severities, with `medium` and `low` excluded (zeroed out).

### Code Inspection

The filtering logic in `get.rs` uses the following approach:

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

For `threshold=high`, `threshold_idx = 1`. The conditions evaluate as:

- `critical`: always included (correct)
- `high`: `1 <= 1` is `true`, so high is included (correct)
- `medium`: `1 <= 2` is `true`, so medium is **included** (INCORRECT -- should be excluded)
- `low`: `1 <= 3` is `true`, so low is **included** (INCORRECT -- should be excluded)

### Root Cause

The comparison operators are inverted. The conditions use `threshold_idx <= N` when they should use `threshold_idx >= N` (or equivalently, `N <= threshold_idx`). With the current logic, lower threshold indices (stricter thresholds) include MORE severities rather than fewer, which is the opposite of intended behavior.

The correct conditions should be:
- `high`: `if threshold_idx >= 1` (include high when threshold is high or lower)
- `medium`: `if threshold_idx >= 2` (include medium when threshold is medium or lower)
- `low`: `if threshold_idx >= 3` (include low when threshold is low)

### Additional Issue: Incorrect `total` Field

The `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low`, which sums the **unfiltered** counts. Even if the filtering comparisons were corrected, the total would still be wrong because it does not reflect the filtered values. The total should sum the filtered counts that are actually included in the response.

## Conclusion

This criterion FAILS for two reasons:
1. The filtering comparison operators are inverted, causing all severities to be included regardless of the threshold value
2. The `total` field always uses unfiltered counts
