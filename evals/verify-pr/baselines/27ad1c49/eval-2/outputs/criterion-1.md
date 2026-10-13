# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds a `threshold` query parameter to the `advisory_summary` handler in `modules/fundamental/src/advisory/endpoints/get.rs`. The filtering logic is implemented as follows:

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

### Why this fails the criterion

The comparison logic is **inverted**. The condition `threshold_idx <= N` checks whether the threshold's position is at or before severity position N, which is the opposite of the intended behavior.

For `threshold=high`, `threshold_idx` = 1 (the position of "high" in the array). The intended behavior is to include only severities at or above "high" (i.e., critical and high). Using the index system where critical=0, high=1, medium=2, low=3, a severity at position P should be included only when P <= threshold_idx.

Walkthrough for `threshold=high` (threshold_idx=1):
- **critical** (position 0): Always included (hardcoded). Correct.
- **high** (position 1): Condition is `1 <= 1` = true. Included. Correct.
- **medium** (position 2): Condition is `1 <= 2` = true. **Included. WRONG** -- medium is below the "high" threshold and should be zeroed out.
- **low** (position 3): Condition is `1 <= 3` = true. **Included. WRONG** -- low is below the "high" threshold and should be zeroed out.

The correct condition for each field should be:
- high: `if 1 <= threshold_idx` (i.e., threshold_idx >= 1)
- medium: `if 2 <= threshold_idx` (i.e., threshold_idx >= 2)
- low: `if 3 <= threshold_idx` (i.e., threshold_idx >= 3)

As implemented, `threshold=high` returns **all four** severity counts instead of just critical and high. This directly violates the criterion.

### Additional issue: total calculation

Even if the filtering were correct, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered counts. The total should reflect only the severities included after threshold filtering.
