## Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: FAIL**

### Analysis

While the `severity_order` array itself is defined in the correct order (`["critical", "high", "medium", "low"]`), the filtering logic that uses this ordering is inverted, which means the ordering is not correctly applied.

The code checks `threshold_idx <= field_constant` for each severity field:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

This produces incorrect results for every threshold value:

| threshold | threshold_idx | high (<=1) | medium (<=2) | low (<=3) | Expected included |
|-----------|--------------|------------|--------------|-----------|-------------------|
| critical  | 0            | included   | included     | included  | critical only     |
| high      | 1            | included   | included     | included  | critical, high    |
| medium    | 2            | excluded   | included     | included  | critical, high, medium |
| low       | 3            | excluded   | excluded     | included  | all               |

For `threshold=medium`, the code excludes `high` but includes `low` -- the exact opposite of the intended behavior. The severity ordering is defined correctly in the array but applied incorrectly in the filtering conditions.

Additionally, the task's Implementation Notes call for defining a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`. No such enum was created; instead, the code uses raw string comparison and hardcoded index constants.

### Evidence

Lines 43-51 of the diff in `get.rs`:
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
```
