# Criterion 5: Response includes threshold_applied boolean field

## Verdict: FAIL

## Criterion Text
Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Analysis

The `AdvisorySummary` struct used in the response does not include a `threshold_applied` boolean field. The PR diff shows the response struct contains only the severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in the response are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

### Expected Behavior

The acceptance criterion requires a `threshold_applied` boolean field that indicates whether severity filtering is active. This field should be:
- `true` when a valid `threshold` query parameter is provided and filtering is applied
- `false` when no `threshold` parameter is provided (no filtering)

This would require:
1. Adding a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`)
2. Setting it to `true` in the `Some(threshold)` branch and `false` in the `None` branch

### Actual Behavior

The field is completely absent from both the struct definition and the response construction. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` was not modified in this PR (the diff only touches `get.rs` and `advisory.rs`). There is no way for API consumers to determine whether threshold filtering was applied from the response alone.

## Evidence
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 47-53 (response construction)
- File: `modules/fundamental/src/advisory/service/advisory.rs` (no changes to struct)
- The `AdvisorySummary` struct fields are: `critical`, `high`, `medium`, `low`, `total`
- No `threshold_applied` field exists anywhere in the PR diff
- The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified in this PR
