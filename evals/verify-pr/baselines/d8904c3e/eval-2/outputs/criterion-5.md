# Criterion 5: Response includes threshold_applied boolean

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The diff constructs the filtered response as an `AdvisorySummary` struct with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in the response are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the response.

Additionally, the diff does not modify the `AdvisorySummary` struct definition (which lives in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure). No changes to the model file appear in the diff, meaning the struct was not extended with a `threshold_applied` field.

## What is missing

The `AdvisorySummary` struct should include a `threshold_applied: bool` field that is:
- `true` when a valid threshold parameter is provided and filtering is active
- `false` when no threshold parameter is provided (default behavior)

This would require:
1. Adding `threshold_applied: bool` to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Setting `threshold_applied: true` in the `Some(threshold)` branch
3. Setting `threshold_applied: false` in the `None` branch (or on the original summary)

Neither the struct modification nor the field assignment appears anywhere in the diff.

## Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- **File:** `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no struct change)
- **Expected:** A `threshold_applied: bool` field in the JSON response
- **Actual:** Field is entirely absent from both the model and the handler code
