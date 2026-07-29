# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted comparison that causes incorrect filtering behavior. Additionally, the `total` field is computed from unfiltered counts.

### Filtering Logic Bug (Inverted Conditions)

The code defines `severity_order = ["critical", "high", "medium", "low"]` with indices:
- critical = 0, high = 1, medium = 2, low = 3

For `threshold=high`, `threshold_idx = 1`. The intent is to include only severities at or above "high" (i.e., critical and high, which have indices 0 and 1).

The code checks `threshold_idx <= severity_constant` for each severity:

| Severity | Condition | Evaluation (threshold=high, idx=1) | Result | Expected |
|----------|-----------|-------------------------------------|--------|----------|
| critical | always included | -- | included | included |
| high | `threshold_idx <= 1` | `1 <= 1` = true | included | included |
| medium | `threshold_idx <= 2` | `1 <= 2` = true | **included** | **excluded** |
| low | `threshold_idx <= 3` | `1 <= 3` = true | **included** | **excluded** |

The conditions are inverted. The code checks whether the threshold index is at or below each severity's fixed index, which is the opposite of the intended filter. The correct condition should be `severity_index <= threshold_idx` (e.g., `1 <= threshold_idx` for high, `2 <= threshold_idx` for medium).

With the current logic, `?threshold=high` returns counts for ALL four severities instead of just critical and high.

### Total Field Bug

Even if the filtering conditions were correct, the `total` field is computed as:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums the **unfiltered** counts regardless of which severity fields were zeroed out. The total should reflect only the filtered counts (e.g., `summary.critical + summary.high` when threshold=high).

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 31-43 of the diff
- The `unwrap_or(0)` on the position lookup defaults invalid thresholds to index 0 (critical) rather than returning an error, compounding the issue
