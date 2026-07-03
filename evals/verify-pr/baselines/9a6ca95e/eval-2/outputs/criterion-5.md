# Criterion 5

**Criterion**: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Analysis

The PR diff modifies two files:
1. `modules/fundamental/src/advisory/endpoints/get.rs` — handler logic
2. `modules/fundamental/src/advisory/service/advisory.rs` — service layer (minimal change)

Neither file adds a `threshold_applied` boolean field to the `AdvisorySummary` response struct. The response struct (defined in `modules/fundamental/src/advisory/model/summary.rs` according to the repo structure) is not modified in this PR at all.

The constructed `AdvisorySummary` in the filtered branch contains only:
```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field. The `None` branch also returns the original `summary` without any such field.

To satisfy this criterion, the `AdvisorySummary` struct would need a new `threshold_applied: bool` field, set to `true` when a threshold parameter is provided and `false` otherwise.

## Verdict: FAIL

The `threshold_applied` boolean field is completely absent from the response. The `AdvisorySummary` struct was not modified to include this field.
