# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The PR diff does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct is not modified anywhere in the diff.

### What the response currently contains

Based on the existing `AdvisorySummary` struct (visible in `modules/fundamental/src/advisory/service/advisory.rs` and referenced in the endpoint handler), the response contains only:
- `critical`: count
- `high`: count
- `medium`: count
- `low`: count
- `total`: count

### What is missing

The acceptance criterion requires a `threshold_applied` boolean field that indicates whether filtering is active. This field should be:
- `true` when a valid `threshold` query parameter is provided and filtering is applied
- `false` when no `threshold` parameter is provided (all counts returned)

### What was needed

To satisfy this criterion, the implementation should have:
1. Added a `threshold_applied: bool` field to the `AdvisorySummary` struct (likely in `modules/fundamental/src/advisory/model/summary.rs`)
2. Set it to `true` when the threshold parameter is `Some(...)` and valid
3. Set it to `false` when the threshold parameter is `None`

### Evidence

- File: `modules/fundamental/src/advisory/service/advisory.rs` -- the struct is unchanged; only a blank line was added
- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `AdvisorySummary` construction in the `Some` branch does not include a `threshold_applied` field
- No changes to the model file (`modules/fundamental/src/advisory/model/summary.rs`) appear in the diff
- The word "threshold_applied" does not appear anywhere in the diff
