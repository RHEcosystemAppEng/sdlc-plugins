# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` has the comparison direction inverted. The code constructs the filtered response as follows:

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

For `threshold=high`, `threshold_idx` resolves to 1. The conditions evaluate as:

| Field | Condition | Evaluation | Result | Expected |
|-------|-----------|------------|--------|----------|
| critical | always included | -- | included | included |
| high | `1 <= 1` | true | included | included |
| medium | `1 <= 2` | true | **included** | **should be 0** |
| low | `1 <= 3` | true | **included** | **should be 0** |

The condition `threshold_idx <= N` checks whether the threshold index is at or before position N, but the correct logic should check whether each severity's position is at or before the threshold index, i.e., `N <= threshold_idx`. With the current code, `threshold=high` returns all four severity counts instead of only critical and high.

### Additional defect: incorrect total computation

The `total` field is computed from unfiltered values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

Even if the filtering conditions were correct and some counts were zeroed out, the total would still reflect the original (unfiltered) sum. The total should be computed from the filtered values.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-54 in the diff
- The comparison `threshold_idx <= 1` / `threshold_idx <= 2` / `threshold_idx <= 3` is inverted; correct logic would be `1 <= threshold_idx` / `2 <= threshold_idx` / `3 <= threshold_idx`
- The total is hardcoded to the sum of all unfiltered counts regardless of threshold
