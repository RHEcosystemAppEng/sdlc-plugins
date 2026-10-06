# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The acceptance criterion requires the response to include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a valid threshold parameter is provided and `false` when no threshold is specified.

The PR diff does not add a `threshold_applied` field to the `AdvisorySummary` struct. The response struct contains only the existing fields: `critical`, `high`, `medium`, `low`, and `total`. No modification to the `AdvisorySummary` struct definition appears in the diff (the struct is defined in `modules/fundamental/src/advisory/model/summary.rs`, which is not modified by this PR).

The `AdvisorySummary` constructed in the filtering logic:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

This construct has no `threshold_applied` field. Clients consuming this endpoint cannot determine from the response alone whether filtering was applied.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the `AdvisorySummary` construction
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified by the PR (no struct change)
- The field is completely absent from the implementation
