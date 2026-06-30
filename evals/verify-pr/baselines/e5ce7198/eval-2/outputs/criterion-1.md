## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Evidence

The filtering logic in `get.rs` uses an inverted comparison that produces incorrect results for every threshold value except the degenerate case.

The code at lines 42-53 of the diff:

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
- `high`: `1 <= 1` = true, included (correct)
- `medium`: `1 <= 2` = true, included (INCORRECT -- medium should be excluded when threshold=high)
- `low`: `1 <= 3` = true, included (INCORRECT -- low should be excluded when threshold=high)

The comparison is backwards. The code checks `threshold_idx <= severity_index` but the correct check is `severity_index <= threshold_idx`. The condition for medium should be `if 2 <= threshold_idx` (i.e., include medium only when threshold is medium or lower), not `if threshold_idx <= 2` (which includes medium for almost any threshold).

### Additional Issue: `total` field is computed from unfiltered counts

The `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low`, which uses the original unfiltered counts regardless of the threshold. This means `total` does not reflect the filtered result, which is semantically incorrect.

### Conclusion

This criterion fails because the filtering logic is inverted. With `threshold=high`, the endpoint returns all four severity counts (critical, high, medium, low) instead of only critical and high.
