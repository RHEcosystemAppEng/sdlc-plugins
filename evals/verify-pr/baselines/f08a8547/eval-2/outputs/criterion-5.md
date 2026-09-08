## Criterion 5: Response includes threshold_applied boolean field

**Verdict: FAIL**

### Requirement

Response includes a `threshold_applied` boolean field indicating whether filtering is active.

### Analysis

The PR diff does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct constructed in the filtering logic contains only the severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied: true` field when a threshold is provided, nor a `threshold_applied: false` field when no threshold is provided.

The `AdvisorySummary` struct definition is not modified in the diff (the changes to `modules/fundamental/src/advisory/service/advisory.rs` do not alter the struct). The struct would need a new `threshold_applied: bool` field added to satisfy this criterion.

### What should happen

The response should include a boolean field indicating whether threshold filtering was applied:
- When `?threshold=high` is provided: `"threshold_applied": true`
- When no threshold is provided: `"threshold_applied": false`

This allows API consumers to programmatically determine whether the returned counts represent filtered or unfiltered data.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs` -- the constructed `AdvisorySummary` lacks a `threshold_applied` field
- **File:** `modules/fundamental/src/advisory/service/advisory.rs` -- no modifications to the `AdvisorySummary` struct definition
- **Missing:** No `threshold_applied` field in the struct, no assignment in either the `Some(threshold)` or `None` branches
- **Impact:** API consumers cannot distinguish between "all counts returned because no threshold was set" and "all counts returned because threshold=low was specified"
