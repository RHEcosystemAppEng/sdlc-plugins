# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The response struct `AdvisorySummary` does not include a `threshold_applied` boolean field. The filtered response is constructed with only the severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the unfiltered case:
```rust
None => summary,
```

Neither branch includes a `threshold_applied` field. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be extended with a `threshold_applied: bool` field.

### What was required

The acceptance criterion requires a boolean field `threshold_applied` in the response that indicates whether threshold filtering is active:
- `true` when a valid threshold parameter is provided
- `false` when no threshold parameter is provided

### What is missing

1. The `AdvisorySummary` struct has no `threshold_applied` field
2. No modification to the model file (`modules/fundamental/src/advisory/model/summary.rs`) appears in the diff
3. Neither the filtered nor unfiltered response paths set such a field

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 47-55 (filtered case) and line 56 (unfiltered case) in the diff
- The `AdvisorySummary` struct construction includes only: critical, high, medium, low, total
- `modules/fundamental/src/advisory/model/summary.rs` is not modified in the diff
- The field `threshold_applied` does not appear anywhere in the diff
