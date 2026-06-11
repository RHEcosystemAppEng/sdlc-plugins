## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Reasoning

The filtering logic in `get.rs` is inverted. The code uses:

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

The severity indices are: critical=0, high=1, medium=2, low=3. For `threshold=high`, `threshold_idx=1`. The conditions evaluate as:

- critical: always included (correct)
- high: `1 <= 1` is true, included (correct)
- medium: `1 <= 2` is true, included (WRONG -- should be zeroed out)
- low: `1 <= 3` is true, included (WRONG -- should be zeroed out)

The comparison direction is backwards. The code checks whether the threshold index is less than or equal to the severity's hardcoded position, which is almost always true. The correct logic should check whether the severity's own index is at or before the threshold index (e.g., `if 1 <= threshold_idx` for high, `if 2 <= threshold_idx` for medium, `if 3 <= threshold_idx` for low), or equivalently use `threshold_idx >= N` instead of `threshold_idx <= N`.

This bug causes every threshold value except "low" to produce incorrect results:
- `threshold=critical` (idx=0): returns all four severities instead of only critical
- `threshold=high` (idx=1): returns all four severities instead of critical+high
- `threshold=medium` (idx=2): returns all four instead of critical+high+medium

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values, so even if the comparison were fixed, the total would still be incorrect.
