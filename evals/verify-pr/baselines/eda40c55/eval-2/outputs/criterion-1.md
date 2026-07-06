## Criterion 1 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

### Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` has an inverted comparison that causes incorrect severity filtering. Tracing through the code for `threshold=high`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
// For threshold="high", threshold_idx = 1

AdvisorySummary {
    critical: summary.critical,                              // always included
    high: if threshold_idx <= 1 { summary.high } else { 0 }, // 1 <= 1 -> true -> INCLUDED
    medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 -> true -> INCLUDED (BUG)
    low: if threshold_idx <= 3 { summary.low } else { 0 },      // 1 <= 3 -> true -> INCLUDED (BUG)
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The condition `threshold_idx <= N` checks whether the threshold's position is at or before the severity's position in the array. This is backwards. The correct condition should be `N <= threshold_idx` (i.e., include the severity if its position index is within the included range, at or before the threshold).

With the correct logic (`N <= threshold_idx` where N is the severity's index):
- critical (idx 0): 0 <= 1 -> true (included) -- correct
- high (idx 1): 1 <= 1 -> true (included) -- correct
- medium (idx 2): 2 <= 1 -> false (excluded) -- correct
- low (idx 3): 3 <= 1 -> false (excluded) -- correct

The current inverted logic means that when `threshold=high`, medium and low counts are incorrectly included in the response instead of being zeroed out. The endpoint does NOT return counts for critical and high only.

Additionally, the `total` field is computed from the original unfiltered summary values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the filtering were corrected, the total would not match the filtered counts.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-56 in the diff
- The comparison `threshold_idx <= N` should be `N <= threshold_idx`
- The `total` field uses unfiltered counts
- No test exists to verify this behavior (test file `tests/api/advisory_summary.rs` is missing from the diff)
