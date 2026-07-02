# Criterion 5: Response includes threshold_applied boolean field

## Verdict: FAIL

## Criterion Text
Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Evidence from Diff

The filtered response is constructed in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the unfiltered path:

```rust
None => summary,
```

## Detailed Reasoning

The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is constructed with only the fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the diff.

The acceptance criterion requires that the response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be:
- `true` when a valid threshold parameter is provided and filtering is applied
- `false` when no threshold parameter is provided

To implement this, the developer would need to either:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct, or
2. Create a new response wrapper struct that includes the summary plus the boolean

Neither approach is present in the diff. The `AdvisorySummary` struct definition in `modules/fundamental/src/advisory/model/summary.rs` is not modified at all -- there are no changes to that file in the diff.

## Conclusion

The criterion fails because the `threshold_applied` boolean field is entirely absent from the response. Neither the response struct nor the handler code includes this field. Callers have no way to determine from the response whether threshold filtering was applied.
