## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Analysis

This criterion requires that when `threshold=high` is provided, the response includes severity counts only for `critical` and `high`, omitting `medium` and `low`.

### Code Inspection

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering as follows:

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

For `threshold=high`, `severity_order.iter().position(...)` returns `Some(1)`, so `threshold_idx = 1`.

Tracing the conditionals for each field:

| Field | Condition | Evaluation | Result |
|-------|-----------|------------|--------|
| critical | always included | -- | included |
| high | `threshold_idx <= 1` | `1 <= 1` = true | **included** |
| medium | `threshold_idx <= 2` | `1 <= 2` = true | **included (BUG)** |
| low | `threshold_idx <= 3` | `1 <= 3` = true | **included (BUG)** |

The comparison is inverted. The code checks whether the threshold index is less than or equal to each severity's hardcoded position constant, but it should check whether each severity's position is less than or equal to the threshold index. The correct condition would be `N <= threshold_idx` (where N is the severity position), not `threshold_idx <= N`.

With the current logic, `threshold=high` returns counts for all four severity levels instead of just `critical` and `high`.

### Additional Defect: Total Computation

The `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the per-severity filtering worked correctly, the total would still reflect all original counts rather than the sum of only the included severities.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Defect:** Inverted comparison operator in threshold filtering conditions
- **Expected behavior:** `threshold=high` returns only `critical` and `high` counts with `medium` and `low` set to 0
- **Actual behavior:** All four severity counts are returned unchanged
- **Root cause:** `threshold_idx <= N` should be `N <= threshold_idx`
