# Acceptance Criterion 5

**Criterion**: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result**: FAIL

## Evidence

The `AdvisorySummary` struct constructed in `modules/fundamental/src/advisory/endpoints/get.rs` contains only the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the response.

Additionally, the `None` branch simply returns the original `summary` object unchanged, which also lacks a `threshold_applied` field.

The diff does not modify the `AdvisorySummary` struct definition (located in `modules/fundamental/src/advisory/model/summary.rs`), so no new field was added to the model.

To satisfy this criterion, the `AdvisorySummary` struct would need a `threshold_applied: bool` field, set to `true` when a valid threshold is provided and `false` otherwise.

**Verdict**: FAIL -- no `threshold_applied` boolean field exists in the response.
