# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR diff does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct constructed in the filtered branch contains only the existing severity count fields.

### Code Under Review

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

### Detailed Reasoning

The acceptance criterion requires that the response includes a `threshold_applied` boolean field that indicates whether filtering is active. This field should be:
- `true` when a valid `threshold` query parameter is provided and filtering is applied
- `false` when no `threshold` parameter is provided (the `None` branch)

The PR diff shows the `AdvisorySummary` struct being constructed with only five fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the diff.

To implement this, the developer would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct definition (likely in `modules/fundamental/src/advisory/model/summary.rs`)
2. Set `threshold_applied: true` in the `Some(threshold)` branch
3. Set `threshold_applied: false` in the `None` branch (or in the existing summary construction)

None of these changes are present in the diff. The `AdvisorySummary` struct definition is not modified in the diff at all (the file `modules/fundamental/src/advisory/model/summary.rs` does not appear in the diff), and the struct construction in `get.rs` does not include the field.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (struct definition unchanged)
- The response object contains only: `critical`, `high`, `medium`, `low`, `total`
- The `threshold_applied` boolean is explicitly listed as Acceptance Criterion 5 in the task
