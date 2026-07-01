## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Analysis

The diff implements threshold filtering in `modules/fundamental/src/advisory/endpoints/get.rs` using an index-based comparison against a `severity_order` array:

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
- critical: always included (correct)
- high: `1 <= 1` = true, included (correct)
- medium: `1 <= 2` = true, included (INCORRECT -- medium should be excluded)
- low: `1 <= 3` = true, included (INCORRECT -- low should be excluded)

The comparison is inverted. The code checks `threshold_idx <= severity_position` but should check `severity_position <= threshold_idx` (i.e., include the severity only if its rank is at or above the threshold). As written, `threshold=high` returns all four severity counts, not just critical and high.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, meaning the total would be incorrect even if the individual fields were filtered properly.

### Evidence

The filtering logic in the diff at lines 41-55 of `get.rs` demonstrates the inverted comparison. The condition `threshold_idx <= N` means that any threshold with a lower index (higher severity) will include ALL lower-severity counts, which is the opposite of the intended behavior.

### Verdict

FAIL -- The filtering logic is inverted and `threshold=high` would include medium and low counts instead of excluding them.
