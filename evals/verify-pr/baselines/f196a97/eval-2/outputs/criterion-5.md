## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Verdict: FAIL

### Analysis

The acceptance criteria require that the response include a `threshold_applied` boolean field that indicates whether filtering is active (i.e., whether a threshold parameter was provided).

Examining the PR diff, the `AdvisorySummary` struct construction in the filtered branch contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the response.

Additionally, the `None` branch simply returns the original `summary` object, which also does not include a `threshold_applied` field.

For this criterion to be met, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be modified to include a `threshold_applied: bool` field, and the handler would need to set it to `true` when a threshold is provided and `false` when it is not. Neither of these changes appears in the diff.

The diff only modifies `modules/fundamental/src/advisory/endpoints/get.rs` and `modules/fundamental/src/advisory/service/advisory.rs`. The model file (`summary.rs`) is not modified, and no `threshold_applied` field is added anywhere.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in either the filtered or unfiltered response
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (should have been updated to add the field)
- The `AdvisorySummary` struct only contains `critical`, `high`, `medium`, `low`, and `total` fields
