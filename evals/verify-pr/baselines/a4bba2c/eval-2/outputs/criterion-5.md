# Criterion 5: Response includes threshold_applied boolean field

## Criterion Text
Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR diff does not add a `threshold_applied` boolean field to the `AdvisorySummary` response. The filtered response struct constructed in the endpoint handler contains only the existing severity count fields and total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied: true` or `threshold_applied: false` field anywhere in the diff. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` (not part of the diff) would need to be modified to include this field, and both the filtered and unfiltered code paths would need to set it appropriately:
- `threshold_applied: true` when a valid threshold parameter is provided
- `threshold_applied: false` when no threshold parameter is provided (the `None` branch)

The `advisory/model/summary.rs` file is not even listed in the Files to Modify section of the task, which suggests this was an oversight in both the task specification and the implementation. However, the acceptance criterion is explicit and the implementation must satisfy it.

## Evidence

- No `threshold_applied` field appears anywhere in the PR diff
- The `AdvisorySummary` struct construction in the `Some(threshold)` branch has 5 fields: critical, high, medium, low, total -- no threshold_applied
- The `None` branch returns the unmodified summary, also without threshold_applied
- The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified in this PR
