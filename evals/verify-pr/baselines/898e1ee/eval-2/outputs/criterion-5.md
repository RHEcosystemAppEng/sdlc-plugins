# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The response struct `AdvisorySummary` as constructed in the filtering logic contains only severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the response.

The task requires that the response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be:
- `true` when a valid threshold parameter is provided and filtering is applied
- `false` when no threshold parameter is provided (all counts returned)

This field is completely absent from the implementation. The `AdvisorySummary` struct would need to be extended to include this field, and both the filtered and unfiltered response paths would need to set it appropriately.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `AdvisorySummary` construction includes only: critical, high, medium, low, total
- No `threshold_applied` field exists in either the `Some(threshold)` branch or the `None` branch
- The `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) would also need updating to include this field
