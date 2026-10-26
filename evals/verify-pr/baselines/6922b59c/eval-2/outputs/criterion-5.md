# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The diff does not add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. The filtered response is constructed with only the existing fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied: true` or `threshold_applied: false` field in either the filtered or unfiltered response paths. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) would need to be updated to include this field, but that file does not appear in the diff at all.

Consumers of this endpoint have no way to determine from the response whether threshold filtering was applied, which was an explicit requirement.
