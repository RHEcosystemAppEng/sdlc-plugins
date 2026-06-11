## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Analysis

The response structure in the diff does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct constructed in the filtering branch contains only the existing severity count fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied: true` or `threshold_applied: false` field in either the filtered or unfiltered response paths. The `AdvisorySummary` model (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) was not modified to add this field.

The acceptance criterion explicitly requires a boolean field so that API consumers can programmatically determine whether the response has been filtered. This is entirely absent from the implementation.

### Evidence

The complete response construction (lines 47-53 of the diff) shows only `critical`, `high`, `medium`, `low`, and `total` fields. No `threshold_applied` field exists anywhere in the diff. The `AdvisorySummary` model file (`modules/fundamental/src/advisory/model/summary.rs`) does not appear in the diff at all, confirming that no structural changes were made to the response type.
