# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The criterion requires that the JSON response includes a `threshold_applied` boolean field that indicates whether threshold filtering is active. When a threshold parameter is provided and valid, this field should be `true`; when no threshold is provided, it should be `false`.

### What the diff shows

The PR diff modifies the `AdvisorySummary` struct construction in `get.rs` but does not add a `threshold_applied` field. The filtered response is built as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the unfiltered response simply returns `summary`.

Neither path includes a `threshold_applied` field. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`, not modified in this diff) does not appear to have been updated to include this field.

### What is needed

1. The `AdvisorySummary` struct in `model/summary.rs` needs a new field: `threshold_applied: bool`
2. When `params.threshold` is `Some(...)` and valid, set `threshold_applied: true`
3. When `params.threshold` is `None`, set `threshold_applied: false`

This field is entirely absent from the implementation, making this criterion clearly unsatisfied.
