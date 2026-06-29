# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

This criterion requires that the API response includes a `threshold_applied` boolean field that indicates whether threshold filtering is currently active.

### Code Inspection

The `AdvisorySummary` struct construction in the filtered branch contains only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Additionally, the `None => summary` branch returns the original `AdvisorySummary` without modification, which also would not include a `threshold_applied` field.

### What Was Expected

The implementation should:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`)
2. Set it to `true` when a valid threshold parameter is provided
3. Set it to `false` when no threshold parameter is provided

Neither the struct modification nor the field assignment appears anywhere in the diff.

### Evidence

- No `threshold_applied` field in the `AdvisorySummary` struct construction
- No modification to the `AdvisorySummary` struct definition (in `summary.rs`)
- The `None` branch returns the unmodified original `summary` which also lacks this field
- A search of the entire diff for "threshold_applied" yields zero matches

## Conclusion

This criterion FAILS. The `threshold_applied` boolean field is completely absent from the implementation. Neither the struct definition nor the response construction includes this field.
