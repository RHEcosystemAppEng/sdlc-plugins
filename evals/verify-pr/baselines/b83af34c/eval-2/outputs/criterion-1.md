## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Verdict: FAIL

### Analysis

The PR introduces threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. Tracing through the code for `threshold=high`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold="high"`, `position` returns `Some(1)`, so `threshold_idx = 1`.

The filtering logic then applies:

```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // 1 <= 1 -> true -> INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 },  // 1 <= 2 -> true -> INCLUDED (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },        // 1 <= 3 -> true -> INCLUDED (BUG)
```

The comparison is backwards. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx`. With the current logic, `threshold=high` includes medium and low counts, violating the acceptance criterion that only critical and high should be returned.

The correct comparison would be:
- `high: if 1 <= threshold_idx { summary.high } else { 0 }`
- `medium: if 2 <= threshold_idx { summary.medium } else { 0 }`
- `low: if 3 <= threshold_idx { summary.low } else { 0 }`

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of threshold, which would produce an incorrect total even if the per-severity filtering were fixed.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 in the diff
- **Bug:** Comparison `threshold_idx <= N` is backwards; should be `N <= threshold_idx`
- **Bug:** `total` always uses unfiltered counts
- **Result for threshold=high:** Returns all four severities instead of only critical and high
