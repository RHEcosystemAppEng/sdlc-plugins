# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The diff introduces threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When a `threshold` query parameter is provided, the code looks up the threshold value's position in the severity ordering array and uses conditional expressions to zero out severity counts below the threshold.

However, the filtering conditions are **inverted**. The code uses `threshold_idx <= N` (where N is the hardcoded index of each severity level) when it should use `N <= threshold_idx` (i.e., include the severity only if its position is at or above the threshold position).

## Evidence

From the diff in `modules/fundamental/src/advisory/endpoints/get.rs`:

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

The severity ordering array maps: critical=0, high=1, medium=2, low=3.

For `threshold=high` (threshold_idx=1):
- `critical`: always included (hardcoded) -- correct
- `high`: `threshold_idx(1) <= 1` is true -- includes high -- correct
- `medium`: `threshold_idx(1) <= 2` is true -- includes medium -- **WRONG** (should be excluded)
- `low`: `threshold_idx(1) <= 3` is true -- includes low -- **WRONG** (should be excluded)

The condition `threshold_idx <= N` evaluates to true for every severity at or below the threshold, which is the opposite of the desired behavior ("at or above"). With `threshold=high`, all four severity counts are returned instead of only critical and high.

The correct condition would be `N <= threshold_idx` (include the severity at index N only if N is less than or equal to the threshold index), e.g.:
- `high`: `if 1 <= threshold_idx` -- include high when threshold is high, medium, or low
- `medium`: `if 2 <= threshold_idx` -- include medium when threshold is medium or low
- `low`: `if 3 <= threshold_idx` -- include low only when threshold is low

Additionally, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the per-severity fields were correctly zeroed, the total would still reflect the pre-filter sum.

## Conclusion

This criterion is not satisfied. The filtering logic is inverted, causing `threshold=high` to return all severity counts rather than only critical and high. The total field also does not reflect filtered counts.
