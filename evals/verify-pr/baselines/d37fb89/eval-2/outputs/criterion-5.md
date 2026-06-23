# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The diff does not add a `threshold_applied` field to the response. The `AdvisorySummary` struct construction in the filtered branch only includes:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied: bool` field anywhere in the diff -- neither in the struct construction, nor in any struct definition visible in the changed code.

The `None` branch also returns the summary without any `threshold_applied` field.

This criterion is entirely unmet. No part of the diff addresses it.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The filtered `AdvisorySummary` construction has 5 fields: critical, high, medium, low, total
- No `threshold_applied` field appears anywhere in the diff
- The `AdvisorySummary` struct definition is not modified in the diff (it is in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure, and that file is not touched)
