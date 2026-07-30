# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

This criterion requires that the API response includes a `threshold_applied` boolean field that indicates whether threshold filtering is currently active.

### Code Inspection

The filtered response struct constructed in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the no-threshold path:

```rust
None => summary,
```

### Defect: Missing `threshold_applied` Field

The response struct `AdvisorySummary` does not include a `threshold_applied` field. The diff shows only five fields in the response: `critical`, `high`, `medium`, `low`, and `total`. There is no boolean field indicating whether filtering is active.

Neither the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`, not modified in the diff) nor the handler code adds a `threshold_applied` field to the response.

### Expected Implementation

The response should include:
- `threshold_applied: true` when a valid threshold parameter is provided and filtering is active
- `threshold_applied: false` when no threshold parameter is provided

This would require either:
1. Adding a `threshold_applied` field to the existing `AdvisorySummary` struct, or
2. Creating a new response struct that wraps `AdvisorySummary` with the additional field

Neither approach was implemented.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `AdvisorySummary` struct fields visible in the diff: `critical`, `high`, `medium`, `low`, `total`
- No `threshold_applied` field exists in the constructed struct or the response
- The `advisory/model/summary.rs` file was not modified in the diff to add the field
