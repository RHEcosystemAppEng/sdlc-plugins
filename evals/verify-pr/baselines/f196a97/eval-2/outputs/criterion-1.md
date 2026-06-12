## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Verdict: FAIL

### Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds a `threshold` query parameter via the `SummaryParams` struct and applies filtering logic in the `advisory_summary` handler.

Examining the filtering logic:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

For `?threshold=high`, `threshold_idx` would be 1 (the index of "high" in the array). The filtering then:
- `critical`: always included (no conditional) -- correct
- `high`: included when `threshold_idx <= 1` -- 1 <= 1 is true -- correct
- `medium`: included when `threshold_idx <= 2` -- 1 <= 2 is true -- **INCORRECT**, medium should be excluded when threshold=high
- `low`: included when `threshold_idx <= 3` -- 1 <= 3 is true -- **INCORRECT**, low should be excluded when threshold=high

Wait -- re-reading more carefully. The conditional returns the summary value when the condition is true and 0 when false. For `threshold=high` (idx=1):
- `critical`: always returned (correct)
- `high`: `1 <= 1` is true, so `summary.high` is returned (correct)
- `medium`: `1 <= 2` is true, so `summary.medium` is returned -- **BUG**: should be 0
- `low`: `1 <= 3` is true, so `summary.low` is returned -- **BUG**: should be 0

The filtering logic is inverted. The condition `threshold_idx <= N` means "include severity at index N if the threshold index is at or before N". But the intent should be "include severity at index N only if N is at or before the threshold index". The correct condition would be `N <= threshold_idx` (or equivalently, the conditional checks should use `threshold_idx >= N`).

For example, with `threshold=high` (idx=1):
- Index 0 (critical): should be included -- `0 <= 1` is true (correct with corrected logic)
- Index 1 (high): should be included -- `1 <= 1` is true (correct)
- Index 2 (medium): should be excluded -- `2 <= 1` is false (correct with corrected logic)
- Index 3 (low): should be excluded -- `3 <= 1` is false (correct with corrected logic)

The implementation has the comparison backwards. With `threshold=high`, medium and low counts are still included, which violates this criterion.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, which means even if the individual fields were filtered correctly, the total would be wrong.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines in the filtering block
- The conditional `threshold_idx <= 2` for medium should be `2 <= threshold_idx` (or equivalent)
- The `total` field sums all unfiltered values instead of only the filtered ones
