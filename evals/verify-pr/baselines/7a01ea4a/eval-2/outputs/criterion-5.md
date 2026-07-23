# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task requires that the response body include a `threshold_applied` boolean field that indicates whether threshold filtering is active (true when a threshold parameter is provided, false otherwise).

### Code Under Review

The filtered `AdvisorySummary` struct is constructed with these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And in the `None` (no threshold) branch:
```rust
None => summary,
```

### Defect: Missing `threshold_applied` Field

The response struct contains only the following fields:
- `critical` (count)
- `high` (count)
- `medium` (count)
- `low` (count)
- `total` (count)

There is no `threshold_applied` boolean field in the `AdvisorySummary` struct or in the constructed response. The diff does not show any modification to the `AdvisorySummary` model (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) to add this field.

### Expected Implementation

The `AdvisorySummary` struct should be extended with a `threshold_applied: bool` field. When a threshold parameter is provided, `threshold_applied` should be set to `true`. When no threshold is provided, it should be `false`. This allows API consumers to programmatically determine whether the returned counts represent all severities or a filtered subset.

### Conclusion

The `threshold_applied` boolean field is entirely absent from the response. This criterion is not satisfied.
