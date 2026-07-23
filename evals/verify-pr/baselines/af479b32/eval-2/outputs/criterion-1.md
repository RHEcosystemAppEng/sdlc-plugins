# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses inverted comparison conditions, causing threshold=high to include ALL severity counts instead of only critical and high.

### Code Analysis

The relevant code from the diff:

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

For `threshold=high`, `threshold_idx = 1` (position of "high" in the severity_order array).

Evaluating each condition:

| Severity | Condition | Evaluation | Result | Expected |
|---|---|---|---|---|
| critical | always included | -- | included | included |
| high | `threshold_idx(1) <= 1` | `1 <= 1` = true | included | included |
| medium | `threshold_idx(1) <= 2` | `1 <= 2` = true | **included** | **should be 0** |
| low | `threshold_idx(1) <= 3` | `1 <= 3` = true | **included** | **should be 0** |

The conditions are inverted. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx` (i.e., include a severity only if its rank position is at or above the threshold's position).

### Additional Issue: Total Calculation

Even if the per-severity conditions were corrected, the `total` field is computed from the **unfiltered** counts:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This uses the original `summary` values rather than the filtered values, so the total would be incorrect even with proper filtering. The total should reflect only the included severity counts.

### Correct Implementation

The conditions should be:
```rust
high: if 1 <= threshold_idx { summary.high } else { 0 },
medium: if 2 <= threshold_idx { summary.medium } else { 0 },
low: if 3 <= threshold_idx { summary.low } else { 0 },
```

This ensures that for threshold=high (idx=1): high (1 <= 1 = true) is included, medium (2 <= 1 = false) is excluded, and low (3 <= 1 = false) is excluded.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines in the filtering match block
- The filtering conditions `threshold_idx <= N` are functionally equivalent to "include this severity whenever the threshold is at or more severe", which is the opposite of the intended behavior
- For threshold=high, the response would contain medium and low counts identical to an unfiltered request
