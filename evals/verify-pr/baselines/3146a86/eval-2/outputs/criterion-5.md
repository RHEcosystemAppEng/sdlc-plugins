# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task requires that the response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a valid `threshold` parameter is provided and `false` (or present with value `false`) when no threshold is specified.

The PR diff does not add a `threshold_applied` field to the `AdvisorySummary` struct. The filtered response only contains the existing fields: `critical`, `high`, `medium`, `low`, and `total`. No modification to the `AdvisorySummary` model (in `modules/fundamental/src/advisory/model/summary.rs`) is present in the diff.

The `AdvisorySummary` struct would need to be extended with:
```rust
pub threshold_applied: bool,
```

And the filtering logic in `get.rs` would need to set this field to `true` when `params.threshold` is `Some(_)` and `false` when it is `None`.

## Evidence

The filtered `AdvisorySummary` construction in the PR diff (lines 47-53 of `get.rs`):
```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

No `threshold_applied` field is present. The `AdvisorySummary` model file (`modules/fundamental/src/advisory/model/summary.rs`) is not modified in the diff.
