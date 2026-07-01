# Criterion 5: Response includes a `threshold_applied` boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active.

**Verdict:** FAIL

## Analysis

The PR diff constructs the filtered `AdvisorySummary` response in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The response struct contains the fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the response.

Additionally, examining the diff for changes to the `AdvisorySummary` model struct (which lives in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure), there are **no changes** to that file in the PR diff. The diff only modifies:
1. `modules/fundamental/src/advisory/endpoints/get.rs` -- the endpoint handler
2. `modules/fundamental/src/advisory/service/advisory.rs` -- the service layer (minimal change, no new fields)

For this criterion to be satisfied, the `AdvisorySummary` struct would need a new `threshold_applied: bool` field, and the endpoint handler would need to set it:
- `threshold_applied: true` when a valid threshold parameter is provided
- `threshold_applied: false` when no threshold parameter is provided

Neither of these changes is present in the diff.

**Conclusion:** The `threshold_applied` boolean field is completely absent from the response. The `AdvisorySummary` struct was not modified to include this field, and the endpoint handler does not set it. This is a clear omission of a required acceptance criterion.
