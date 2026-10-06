# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When a threshold parameter is provided, the code looks up the threshold string in the `severity_order` array to get an index, then uses that index to decide which severity counts to include.

The `severity_order` array is defined as `["critical", "high", "medium", "low"]`, mapping to indices 0, 1, 2, 3 respectively.

For `threshold=high`, the position lookup returns index 1 (`threshold_idx = 1`).

The filtering conditions are:

```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // 1 <= 1 = true -> included
medium: if threshold_idx <= 2 { summary.medium } else { 0 },  // 1 <= 2 = true -> INCLUDED
low: if threshold_idx <= 3 { summary.low } else { 0 },        // 1 <= 3 = true -> INCLUDED
```

The comparison operators are **reversed**. The condition `threshold_idx <= N` checks whether the threshold is at or above the severity level N, which means it includes severities at or below the threshold -- the opposite of the intended behavior.

The correct condition should be `N <= threshold_idx` (or equivalently `threshold_idx >= N`), which would include a severity only if its index is within the threshold range:

- For `threshold=high` (idx=1): high (1 <= 1 = true), medium (2 <= 1 = false), low (3 <= 1 = false) -- correctly returns only critical and high.

With the current code, `threshold=high` returns counts for all four severity levels, which violates this acceptance criterion.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-44 in the diff
- The comparison `threshold_idx <= 2` for medium evaluates to `1 <= 2 = true`, incorrectly including medium
- The comparison `threshold_idx <= 3` for low evaluates to `1 <= 3 = true`, incorrectly including low
