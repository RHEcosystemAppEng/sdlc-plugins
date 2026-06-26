# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## Evidence

The filtered response is constructed as an `AdvisorySummary` struct in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The struct contains five fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the response.

Additionally, the diff does not modify the `AdvisorySummary` struct definition (which lives in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure). No new field was added to the model, and no `threshold_applied` boolean appears anywhere in the diff.

The acceptance criterion explicitly requires a `threshold_applied` boolean field in the response to indicate whether filtering is active. This field is entirely absent. FAIL.
