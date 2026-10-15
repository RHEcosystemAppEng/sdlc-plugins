## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Analysis

The filtered response constructs an `AdvisorySummary` with only the following fields:

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

For the `None` (no threshold) case, the raw `summary` is returned, which also does not include a `threshold_applied` field.

### What Should Happen

The `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) should be extended with a `threshold_applied: bool` field. It should be set to `true` when a valid threshold parameter is provided and filtering is active, and `false` (or absent via `#[serde(skip_serializing_if)]`) when no threshold is specified.

### Evidence

The `AdvisorySummary` struct construction in the diff shows only `critical`, `high`, `medium`, `low`, and `total` fields. No `threshold_applied` field is present in either the filtered or unfiltered response paths.
