# Criterion 5 Analysis

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The response does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct construction in the diff only includes the severity count fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in the response are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

### What Should Happen

The response should include a boolean field `threshold_applied` that is:
- `true` when a valid threshold parameter is provided and filtering is active
- `false` when no threshold parameter is provided (default behavior)

This would require:
1. Adding a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`)
2. Setting `threshold_applied: true` in the `Some(threshold)` branch
3. Setting `threshold_applied: false` in the `None` branch (or in the original summary construction)

### Gap

Neither the `AdvisorySummary` struct definition nor its construction in the handler includes a `threshold_applied` field. The diff does not modify the model file (`modules/fundamental/src/advisory/model/summary.rs`) where the struct is defined, so the field was never added.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the AdvisorySummary construction
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no field added to the struct definition)
- The `None` branch returns the raw `summary` without any `threshold_applied` field
