## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Analysis

The diff constructs a filtered `AdvisorySummary` when a threshold is provided:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct is not modified to include a `threshold_applied` boolean field. The response only contains the existing fields (critical, high, medium, low, total). There is no indication in the response body whether threshold filtering was applied.

The diff does not touch `modules/fundamental/src/advisory/model/summary.rs` where the `AdvisorySummary` struct is defined, and no `threshold_applied` field appears anywhere in the diff.

### Expected Implementation

The `AdvisorySummary` struct should include:
```rust
pub threshold_applied: bool,
```

And the handler should set it to `true` when a threshold is provided and `false` otherwise.

### Evidence

The complete diff shows no occurrence of `threshold_applied` in any file. The `AdvisorySummary` struct construction in the `Some(threshold)` branch contains only: critical, high, medium, low, total. The model file `summary.rs` is not modified.

### Verdict

FAIL -- The `threshold_applied` boolean field is completely absent from both the response struct and the handler logic.
