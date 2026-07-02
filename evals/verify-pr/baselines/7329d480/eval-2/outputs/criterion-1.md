# Criterion 1: threshold=high returns counts for critical and high only

## Result: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses a reversed comparison operator, causing the threshold filter to include severities it should exclude.

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

### Trace for threshold="high"

- `threshold_idx` = 1 (position of "high" in the array)
- `critical`: always included (correct)
- `high`: `1 <= 1` = true, included (correct)
- `medium`: `1 <= 2` = true, included (WRONG -- should be excluded)
- `low`: `1 <= 3` = true, included (WRONG -- should be excluded)

The condition `threshold_idx <= N` checks whether the threshold's position is at or before the severity's position. This is the inverse of the intended logic. The correct condition should be `N <= threshold_idx` (i.e., include the severity only if its position in the ordering is at or before the threshold position).

### Correct Logic

For threshold="high" (idx=1), we want to include severities whose index <= 1:
- critical (idx 0): 0 <= 1 = true (include)
- high (idx 1): 1 <= 1 = true (include)
- medium (idx 2): 2 <= 1 = false (exclude)
- low (idx 3): 3 <= 1 = false (exclude)

### Additional Issue

The `total` field is computed from the original unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the filtering were corrected, the total would be wrong.

## Verdict

FAIL -- The filtering logic is reversed. With threshold=high, the response includes counts for all four severity levels instead of only critical and high.
