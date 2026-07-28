# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The diff does not add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. The response contains only the existing severity count fields (`critical`, `high`, `medium`, `low`, `total`) with no indication of whether threshold filtering was applied.

## Evidence

From the diff in `modules/fundamental/src/advisory/endpoints/get.rs`, the `AdvisorySummary` struct constructed in the filtering branch contains:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And in the no-threshold branch:

```rust
None => summary,
```

Neither branch adds a `threshold_applied` field. There is no modification to the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`, which is not touched by this diff) to include such a field.

A compliant implementation would need to:
1. Add `threshold_applied: bool` to the `AdvisorySummary` struct in `model/summary.rs`
2. Set `threshold_applied: true` when a threshold parameter is provided
3. Set `threshold_applied: false` when no threshold parameter is provided

None of these changes are present in the diff.

## Conclusion

This criterion is not satisfied. The `threshold_applied` boolean field is entirely absent from both the response struct and the handler logic. API consumers have no way to determine whether the returned counts reflect filtered or unfiltered data.
