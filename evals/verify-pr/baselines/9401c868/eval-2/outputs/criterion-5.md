## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Result: FAIL

### Analysis

The task requires that the response includes a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field is completely absent from the implementation.

The constructed `AdvisorySummary` in the filtered branch contains only:
```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

Fields present: `critical`, `high`, `medium`, `low`, `total`
Field missing: `threshold_applied`

Similarly, the unfiltered branch returns `summary` as-is, which also lacks any `threshold_applied` field.

### Expected Behavior

The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need a new `threshold_applied: bool` field. The endpoint should set:
- `threshold_applied: true` when a valid threshold parameter is provided
- `threshold_applied: false` when no threshold parameter is provided

This field allows API consumers to programmatically determine whether the returned counts represent the full set or a filtered subset, which is important for correct interpretation of the response data.

The diff does not modify the `AdvisorySummary` struct definition (in `model/summary.rs`), and the `summary.rs` file is not present in the diff at all, confirming that no structural change was made to the response type.
