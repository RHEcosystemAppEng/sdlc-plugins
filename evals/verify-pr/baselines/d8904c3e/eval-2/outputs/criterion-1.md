# Criterion 1: Threshold filtering returns only at-or-above counts

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds a `SummaryParams` struct with an `Option<String>` threshold field and extracts it via `Query(params)`. When `params.threshold` is `Some(threshold)`, the code defines a severity ordering array `["critical", "high", "medium", "low"]` and uses `position()` to find the threshold index.

The filtering logic sets each severity count to 0 if its index exceeds the threshold index:

```rust
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

For `threshold=high`, `threshold_idx` would be 1 (index of "high" in the array). This means:
- `critical` is always returned (index 0 <= any threshold_idx)
- `high` is returned because `threshold_idx(1) <= 1` is true
- `medium` is zeroed because `threshold_idx(1) <= 2` is true -- wait, that's wrong. Let me re-read.

Actually, the condition `if threshold_idx <= 1` for high means: include high when threshold_idx is 0 or 1. For threshold=high, threshold_idx=1, so high IS included. For threshold=critical, threshold_idx=0, so `0 <= 1` is true, so high would also be included. That is incorrect -- threshold=critical should only return critical.

Wait, let me re-check. For threshold=critical, threshold_idx=0:
- critical: always included
- high: `if 0 <= 1` -> true -> included (BUG: should be excluded)

This means threshold=critical would incorrectly include high counts. However, criterion 1 specifically asks about threshold=high, which would work correctly (returns critical and high). The ordering bug manifests for threshold=critical, which is tested under the test requirements but is not this specific criterion.

For the specific case of `threshold=high`:
- threshold_idx = 1
- critical: always included (correct)
- high: `1 <= 1` = true, included (correct)
- medium: `1 <= 2` = true, included (INCORRECT -- medium should be excluded when threshold=high)

This is a FAIL. When threshold=high, medium is still included because the condition `threshold_idx <= 2` evaluates to `1 <= 2 = true`. The filtering logic is inverted -- it includes severities below the threshold instead of excluding them.

**Corrected Verdict:** FAIL

The filtering conditions are inverted. For `threshold=high` (threshold_idx=1):
- medium: `if threshold_idx <= 2` evaluates to `if 1 <= 2` which is `true`, so medium is included when it should be excluded
- low: `if threshold_idx <= 3` evaluates to `if 1 <= 3` which is `true`, so low is included when it should be excluded

Wait -- let me reconsider. The severity_order array is `["critical", "high", "medium", "low"]`. For threshold=high, the intent is to include critical (index 0) and high (index 1), and exclude medium (index 2) and low (index 3). The threshold_idx for "high" is 1.

The condition for including a severity should be: include if the severity's index <= threshold_idx. But the code checks `if threshold_idx <= severity_index` which is the opposite.

Actually, re-reading the code more carefully:
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- this checks if the threshold index is at most 1. For threshold=high (idx=1), 1<=1 is true, so high is included. For threshold=critical (idx=0), 0<=1 is true, so high is INCORRECTLY included.
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- for threshold=high (idx=1), 1<=2 is true, so medium is INCORRECTLY included.

So for threshold=high, the code returns critical, high, AND medium -- it does NOT correctly filter to only critical and high.

**Final Verdict: FAIL**

The filtering logic is flawed. For `threshold=high` (threshold_idx=1), the conditions `threshold_idx <= 2` and `threshold_idx <= 3` evaluate to true, so medium and low are both included. The correct condition should compare the severity's own index against the threshold index (e.g., `if severity_idx <= threshold_idx`), not compare `threshold_idx` against hardcoded constants.
