## Criterion 1

**Text:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**What I checked:** The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, specifically the conditional expressions that zero out severity counts based on the threshold parameter.

**Code evidence:**

The filtering logic in the diff:

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

For `threshold=high`, `threshold_idx = 1`. The comparisons evaluate as:
- `critical`: always included (no condition)
- `high`: `1 <= 1` = true -> included (correct)
- `medium`: `1 <= 2` = true -> **included (WRONG -- should be excluded)**
- `low`: `1 <= 3` = true -> **included (WRONG -- should be excluded)**

The comparison is inverted. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx` (i.e., include a severity only if its position in the ordered list is at or before the threshold position). With the current logic, `threshold=high` returns ALL four severity counts instead of just critical and high.

Additionally, the `total` field is computed from the original unfiltered summary values (`summary.critical + summary.high + summary.medium + summary.low`), not from the filtered values. Even if the filtering conditions were correct, the total would still reflect the unfiltered sum.

**Verdict: FAIL** -- The filtering logic comparison is inverted, causing `threshold=high` to include medium and low counts. The total is also computed from unfiltered values.
