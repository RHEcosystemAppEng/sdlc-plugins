# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted comparison that causes the threshold filter to include too many severity levels instead of restricting them.

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

### Defect: Inverted Comparison

For `threshold=high`, the `threshold_idx` resolves to `1` (the position of "high" in the `severity_order` array).

The conditions evaluate as:
- `critical`: always included (correct)
- `high`: `threshold_idx <= 1` -> `1 <= 1` -> true -> included (correct)
- `medium`: `threshold_idx <= 2` -> `1 <= 2` -> true -> **included** (WRONG -- should be 0)
- `low`: `threshold_idx <= 3` -> `1 <= 3` -> true -> **included** (WRONG -- should be 0)

The condition is backwards. It checks whether `threshold_idx <= severity_position` when it should check whether `severity_position <= threshold_idx`. The correct conditions would be:
- `high`: `if 1 <= threshold_idx` (include high when threshold is high or lower)
- `medium`: `if 2 <= threshold_idx` (include medium when threshold is medium or lower)
- `low`: `if 3 <= threshold_idx` (include low only when threshold is low)

With the correct logic for `threshold=high` (idx=1): high would be included (1<=1), medium excluded (2<=1 is false), low excluded (3<=1 is false). This matches the expected behavior.

### Additional Defect: Total Not Recomputed from Filtered Counts

The `total` field is computed from the unfiltered summary values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

Even if the filtering worked correctly, the total would reflect all four severity counts rather than just the filtered ones. It should sum only the values that survived the filter.

### Conclusion

The endpoint does NOT return counts for critical and high only when `threshold=high` is specified. Due to the inverted comparison, all four severity counts are returned. This criterion is not satisfied.
