# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The diff constructs an `AdvisorySummary` struct in the `Some(threshold)` branch of `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in the constructed struct are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Furthermore, the diff does not modify the `AdvisorySummary` struct definition (which lives in `modules/fundamental/src/advisory/model/summary.rs` based on the repository structure). Without adding the field to the struct definition, it cannot appear in the JSON response.

Neither branch of the `match` expression (the `Some` branch for filtered results, nor the `None` branch for unfiltered results) includes a `threshold_applied` value. The expected behavior is:

- When a valid threshold is provided: `threshold_applied: true`
- When no threshold is provided: `threshold_applied: false`

This field is completely absent from the implementation.
