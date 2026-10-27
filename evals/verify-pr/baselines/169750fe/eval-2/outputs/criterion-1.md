# Criterion 1: threshold=high returns counts for critical and high only

## Verdict: FAIL

## Analysis

The acceptance criterion requires:
> `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Evidence from the diff

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtering logic is:

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
- `critical`: always included (no conditional)
- `high`: `1 <= 1` = true — included
- `medium`: `1 <= 2` = true — **included (BUG)**
- `low`: `1 <= 3` = true — **included (BUG)**

The comparison is inverted. The code checks `threshold_idx <= field_index` when it should check `field_index <= threshold_idx`. As a result, `threshold=high` returns counts for all four severities instead of only critical and high.

### Conclusion

The filtering logic does not correctly restrict results to severities at or above the threshold. With `threshold=high`, medium and low counts are still included in the response. This criterion is **not satisfied**.
