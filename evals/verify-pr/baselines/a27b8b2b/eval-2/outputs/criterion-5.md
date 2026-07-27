## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Analysis

The PR does not add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. The filtered response object only contains the existing fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

To satisfy this criterion, the `AdvisorySummary` struct (likely defined in `modules/fundamental/src/advisory/model/summary.rs`) would need a new `threshold_applied: bool` field, and the handler would need to set it to `true` when a threshold parameter is provided and `false` otherwise.

Neither the model struct modification nor the field assignment exists in the diff.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `AdvisorySummary` struct construction in the `Some(threshold)` arm has no `threshold_applied` field
- The `None` arm returns the unmodified summary, which also lacks this field
- No changes to `modules/fundamental/src/advisory/model/summary.rs` appear in the diff
