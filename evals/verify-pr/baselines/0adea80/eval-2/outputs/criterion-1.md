# Criterion 1: Threshold=high returns counts for critical and high only

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Analysis

The PR introduces threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation defines `severity_order = ["critical", "high", "medium", "low"]` with indices critical=0, high=1, medium=2, low=3, and uses `threshold_idx` to determine which severities to include.

However, the filtering conditions are inverted. The code uses:
```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For `threshold=high`, `threshold_idx = 1`:
- `critical`: always included (correct)
- `high`: `1 <= 1` = true, included (correct)
- `medium`: `1 <= 2` = true, **included** (INCORRECT -- should be excluded)
- `low`: `1 <= 3` = true, **included** (INCORRECT -- should be excluded)

The condition `threshold_idx <= N` means "include this severity if the threshold is at or above this severity level," but the comparison direction is wrong. The correct logic should be something like `if N <= threshold_idx` (include severities whose index is at or below the threshold index, i.e., severities at or above the threshold in severity ranking).

Additionally, the `total` field is always computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, which means even if the individual fields were correctly zeroed, the total would still be wrong.

## Conclusion

The filtering logic is broken due to an inverted comparison. When `threshold=high`, medium and low counts are still returned instead of being zeroed out. This criterion is not satisfied.
