## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is incorrect. The code builds a `severity_order` array with indices: critical=0, high=1, medium=2, low=3. When `threshold=high`, `position()` returns `Some(1)`, so `threshold_idx = 1`.

The filtering conditions then evaluate as follows:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },    // 1 <= 1 = true -> INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 = true -> INCLUDED (WRONG)
low: if threshold_idx <= 3 { summary.low } else { 0 },       // 1 <= 3 = true -> INCLUDED (WRONG)
```

With `threshold=high`, medium and low counts are still included because the condition checks `threshold_idx <= field_constant` instead of the correct `field_index <= threshold_idx`. The logic is inverted.

The correct condition should be checking whether each severity's index is at or above (numerically <=) the threshold index. For example, for the `medium` field (index 2), the condition should be `2 <= threshold_idx`, not `threshold_idx <= 2`.

As a result, `?threshold=high` returns all four severity counts, not just critical and high. The criterion is not met.

### Evidence

Lines 42-52 of the diff in `get.rs`:
```rust
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
