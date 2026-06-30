# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The acceptance criteria explicitly require that the response includes a `threshold_applied` boolean field. This field should be `true` when a valid threshold parameter is provided and filtering is active, and `false` when no threshold is specified.

Examining the diff in `modules/fundamental/src/advisory/endpoints/get.rs`, the response is constructed as an `AdvisorySummary` struct with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The struct contains only: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the diff.

## Evidence

- **Expected:** The `AdvisorySummary` response struct should include `threshold_applied: bool`
- **Actual:** The struct is constructed with only severity count fields and `total` -- no `threshold_applied` field
- The diff does not modify `modules/fundamental/src/advisory/model/summary.rs` (where the `AdvisorySummary` struct is defined), so no new field was added to the struct definition
- Neither the `Some(threshold)` branch nor the `None` branch sets a `threshold_applied` value

## What Should Be Implemented

1. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` should be extended with a `threshold_applied: bool` field
2. In the `Some(threshold)` branch, `threshold_applied` should be set to `true`
3. In the `None` branch, `threshold_applied` should be set to `false`
