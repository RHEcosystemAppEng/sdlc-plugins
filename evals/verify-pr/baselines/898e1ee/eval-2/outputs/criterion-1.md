# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is inverted and does not correctly filter severities at or above the threshold.

### Code trace for `threshold="high"`

The severity order array is `["critical", "high", "medium", "low"]`, so `"high"` maps to `threshold_idx = 1`.

The filtering conditions evaluate as follows:

| Field | Condition | Evaluation | Result | Expected |
|-------|-----------|------------|--------|----------|
| critical | always `summary.critical` | N/A | included | included |
| high | `threshold_idx <= 1` | `1 <= 1` = true | included | included |
| medium | `threshold_idx <= 2` | `1 <= 2` = true | **included** | **excluded** |
| low | `threshold_idx <= 3` | `1 <= 3` = true | **included** | **excluded** |

The condition `threshold_idx <= N` (where N is a hardcoded constant representing the severity's position) checks whether the threshold is at or above the severity's rank. This is the inverse of what is needed. The correct condition would be `N <= threshold_idx` (or equivalently, the severity's index should be <= the threshold index to be included).

With the current logic, `threshold=high` returns counts for all four severities instead of only critical and high, directly violating this criterion.

### Additional issue: total field

Even if the filtering logic were corrected, the `total` field is computed from **unfiltered** counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums all original severity counts regardless of whether filtering zeroed out some fields. The total should be computed from the filtered values.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` and `low: if threshold_idx <= 3 { summary.low } else { 0 }`
- The conditions are inverted; they include severities below the threshold instead of excluding them
