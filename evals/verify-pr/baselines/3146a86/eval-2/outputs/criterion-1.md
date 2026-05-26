# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR introduces threshold filtering in `modules/fundamental/src/advisory/endpoints/get.rs`. The filtering logic uses a `severity_order` array `["critical", "high", "medium", "low"]` and computes a `threshold_idx` via `position()`.

For `threshold=high`, `threshold_idx = 1`. The code then applies these conditions:
- `critical`: always included (no condition) -- correct
- `high`: included if `threshold_idx <= 1` -- for threshold=high (idx=1), 1 <= 1 = true -- correct
- `medium`: included if `threshold_idx <= 2` -- for threshold=high (idx=1), 1 <= 2 = true -- **INCORRECT**, medium should be excluded
- `low`: included if `threshold_idx <= 3` -- for threshold=high (idx=1), 1 <= 3 = true -- **INCORRECT**, low should be excluded

The condition logic is inverted. The code checks whether the threshold's index is less than or equal to the severity level's position, but it should check whether each severity level's position is less than or equal to the threshold's index. The correct conditions would be:
- `high`: include if `1 <= threshold_idx` (severity index <= threshold index)
- `medium`: include if `2 <= threshold_idx`
- `low`: include if `3 <= threshold_idx`

With `threshold=high` (threshold_idx=1):
- high: 1 <= 1 = true (include) -- correct
- medium: 2 <= 1 = false (exclude) -- correct
- low: 3 <= 1 = false (exclude) -- correct

As implemented, `threshold=high` would return counts for critical, high, medium, AND low -- effectively no filtering occurs for any threshold value except `critical`.

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the filtering conditions were correct, the total would not reflect the filtered result.

## Evidence

From the PR diff in `get.rs`, lines 41-53:
```rust
let filtered = match &params.threshold {
    Some(threshold) => {
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
    }
    None => summary,
};
```

The conditions `threshold_idx <= N` should be `N <= threshold_idx` for correct at-or-above filtering.
