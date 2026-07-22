## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Verdict: FAIL

### What was checked

The PR diff was inspected for the addition of a `threshold_applied` boolean field to the `AdvisorySummary` response struct. This field should be `true` when a valid threshold parameter is provided and filtering is active, and `false` when no threshold is specified.

### Evidence

The filtered response constructed in `modules/fundamental/src/advisory/endpoints/get.rs` creates an `AdvisorySummary` with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

Additionally, the `AdvisorySummary` struct definition is not modified in the diff (the struct is defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure, and that file does not appear in the diff). Without adding the field to the struct, it cannot be serialized in the JSON response.

The `None` branch (`None => summary`) also does not set any `threshold_applied` field.

### Gap

The `threshold_applied` boolean field is completely absent from the implementation. Neither the struct definition nor the response construction includes this field. Implementing this would require:

1. Adding `threshold_applied: bool` to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Setting `threshold_applied: true` in the `Some(threshold)` branch
3. Setting `threshold_applied: false` in the `None` branch (or ensuring the existing struct default handles it)
