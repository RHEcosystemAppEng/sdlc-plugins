## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Verdict: FAIL

### Analysis

The acceptance criterion requires the response to include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field is entirely absent from the implementation.

The `AdvisorySummary` struct (used as the response type) is not modified in the diff. The diff shows the response being constructed with only the existing fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in the struct construction. The struct definition in `modules/fundamental/src/advisory/model/summary.rs` would need to be updated to include this field, and the endpoint handler would need to set it to `true` when a threshold parameter is provided and `false` when it is not.

Neither the model file nor the endpoint handler includes this field. The `modules/fundamental/src/advisory/model/summary.rs` file does not appear in the PR diff at all.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs` -- `AdvisorySummary` constructed without `threshold_applied` field
- **File:** `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the PR diff
- **Missing:** The `threshold_applied: bool` field is not added to the struct definition
- **Missing:** The endpoint handler does not set `threshold_applied` based on `params.threshold.is_some()`
