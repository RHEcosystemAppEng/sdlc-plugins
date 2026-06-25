# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task requires that the response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a threshold parameter is provided and `false` when no threshold is specified.

### What the diff implements

The diff constructs an `AdvisorySummary` struct in the filtered case:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct fields shown are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Additionally, no changes were made to the `AdvisorySummary` struct definition (which lives in `modules/fundamental/src/advisory/model/summary.rs` according to the repo structure). The diff only modifies `endpoints/get.rs` and `service/advisory.rs` -- the model file is not touched.

### What should happen

The `AdvisorySummary` struct should be extended with a `threshold_applied: bool` field, and the handler should set it to `true` when a threshold parameter is provided and `false` otherwise:

```rust
AdvisorySummary {
    // ... severity counts ...
    threshold_applied: params.threshold.is_some(),
}
```

### Conclusion

This criterion is not met. The `threshold_applied` boolean field is completely absent from the response. Neither the model struct nor the handler code includes this field.
