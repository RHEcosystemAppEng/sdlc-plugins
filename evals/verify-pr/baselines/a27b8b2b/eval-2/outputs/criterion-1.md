## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation defines a `severity_order` array `["critical", "high", "medium", "low"]` and uses `position()` to find the threshold index. However, the filtering conditions are inverted.

For `threshold=high`, the threshold index is 1 (the position of "high" in the array). The code then applies these conditions:

```rust
critical: summary.critical,                                      // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },        // 1 <= 1 = true -> included
medium: if threshold_idx <= 2 { summary.medium } else { 0 },    // 1 <= 2 = true -> included (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },          // 1 <= 3 = true -> included (BUG)
```

The condition `threshold_idx <= N` is backwards. For threshold=high (idx=1), medium (checked as `1 <= 2 = true`) and low (checked as `1 <= 3 = true`) are both incorrectly included. The endpoint returns ALL severity counts, not just critical and high.

The correct condition should check whether each severity's rank is at or above the threshold rank, i.e., `severity_rank <= threshold_idx` or equivalently the conditions should use `>=` instead of `<=` (e.g., `if threshold_idx >= 1` for high, `if threshold_idx >= 2` for medium, `if threshold_idx >= 3` for low).

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, which would produce an incorrect total even if the filtering were fixed.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: filtering logic in the `Some(threshold)` match arm
- The comparison operators are inverted: `threshold_idx <= N` should be `threshold_idx >= N`
- The total field uses unfiltered sum values
