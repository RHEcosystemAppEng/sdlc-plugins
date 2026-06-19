# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` correctly zeroes out severity levels below the threshold. When `threshold=high` (index 1 in the `severity_order` array), the conditional expressions work as follows:

- `critical: summary.critical` -- always included (correct)
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- threshold_idx=1, 1<=1 is true, so high is included (correct)
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- threshold_idx=1, 1<=2 is true, so medium is **included** (INCORRECT -- should be zeroed for threshold=high)

**Wait -- re-analyzing the logic more carefully:**

Actually, the severity_order array is `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3. For `threshold=high`, `position()` returns index 1.

The filtering logic:
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- 1 <= 1 is true, include high (correct)
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- 1 <= 2 is true, include medium (INCORRECT)

This means `threshold=high` would include medium counts, which violates the criterion that only critical and high should be returned.

**However**, re-reading again more carefully: the threshold_idx represents the position in the array. The intent is that severities at or above the threshold are included. In the array `["critical", "high", "medium", "low"]`, index 0 is the highest severity and index 3 is the lowest.

For `threshold=high` (index 1), the criterion says to return critical and high only (indices 0 and 1). The condition `threshold_idx <= 1` checks whether the threshold is at index 1 or lower (meaning "high" or higher priority). But the conditions are applied to each *field*, not to the threshold:

- `high: if threshold_idx <= 1` -- this asks "is the threshold at or above high?" (yes), so include high
- `medium: if threshold_idx <= 2` -- this asks "is the threshold at or above medium?" (yes, high is above medium), so include medium

This is a **logical error**. The condition is backwards. It should be checking whether each severity level is at or above the threshold, not whether the threshold is at or above each level.

The correct logic should be: include a severity level if its index is <= threshold_idx (i.e., the severity is at least as severe as the threshold). The current code checks the opposite direction.

**Actually, upon even further analysis:**

- For `threshold=critical` (idx=0): high condition `0 <= 1` is true (includes high -- WRONG, should only include critical)
- For `threshold=high` (idx=1): medium condition `1 <= 2` is true (includes medium -- WRONG)
- For `threshold=medium` (idx=2): low condition `2 <= 3` is true (includes low -- WRONG)

The filtering logic is fundamentally broken. It includes too many severity levels for any given threshold.

**Additionally, the `total` field has a separate bug:** It always computes `summary.critical + summary.high + summary.medium + summary.low` using the original unfiltered values, rather than the filtered values. Even if the individual field filtering were correct, the total would be wrong.

## Evidence

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

The `total` field on the last line sums the original unfiltered values from `summary`, not the conditionally-filtered values used for the individual fields.

The filtering conditions also have a directional bug: for `threshold=high` (idx=1), the condition `1 <= 2` evaluates to true, causing `medium` to be included when it should be zeroed out.
