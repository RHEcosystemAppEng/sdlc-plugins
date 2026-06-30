## Criterion 5

**Text**: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict**: FAIL

**Evidence**: The `AdvisorySummary` struct constructed in the filtering branch (lines 47-53 of the diff in `get.rs`) contains only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` boolean field anywhere in the diff. Neither the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`, not modified in this PR) nor the inline struct construction includes this field. The task acceptance criteria explicitly require a `threshold_applied` boolean to indicate whether filtering is active (`true` when a threshold parameter is provided, `false` otherwise). This field is completely missing from the implementation.
