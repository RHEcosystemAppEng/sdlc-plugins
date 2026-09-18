## Criterion 1: threshold=high returns counts for critical and high only

**Verdict: FAIL**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses index-based comparison to determine which severity counts to include. The `severity_order` array is `["critical", "high", "medium", "low"]`, so `threshold=high` resolves to `threshold_idx = 1`.

The filtering conditions are:

```rust
critical: summary.critical,                              // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },    // 1 <= 1 -> true -> INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 -> true -> INCLUDED (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },       // 1 <= 3 -> true -> INCLUDED (BUG)
```

The comparison direction is inverted. The condition `threshold_idx <= N` checks whether the threshold is "above or at" the severity's hardcoded position, but it should check whether the severity's position is at or above the threshold. The correct condition would be `N <= threshold_idx` (i.e., the severity index must be less than or equal to the threshold index to be included).

### Trace for threshold=high (idx=1)

| Severity | Index | Condition | Result | Expected | Correct? |
|----------|-------|-----------|--------|----------|----------|
| critical | 0 | always | included | included | Yes |
| high | 1 | 1 <= 1 | included | included | Yes |
| medium | 2 | 1 <= 2 | included | excluded (0) | **No** |
| low | 3 | 1 <= 3 | included | excluded (0) | **No** |

### Additional trace for threshold=critical (idx=0)

For threshold=critical, the behavior is even more clearly wrong -- all severities are included (0 <= 1, 0 <= 2, 0 <= 3 are all true), when only critical should be returned.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-56 in the diff
- **Bug:** Comparison `threshold_idx <= N` should be `N <= threshold_idx`
- **Impact:** Threshold filtering is effectively non-functional for most threshold values; medium and low counts are incorrectly included when threshold=high

### Additional issue: total uses unfiltered counts

The total field is computed as `summary.critical + summary.high + summary.medium + summary.low`, which uses the original unfiltered counts rather than the filtered values. Even if the per-severity filtering were correct, the total would be inconsistent with the filtered individual counts.
