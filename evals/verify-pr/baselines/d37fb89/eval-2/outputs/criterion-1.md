# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The diff adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation uses an array `["critical", "high", "medium", "low"]` to define severity ordering, finds the `threshold_idx` via `.position()`, and then conditionally includes each severity count.

However, the filtering comparisons are inverted. For `threshold=high`, `threshold_idx` is `1`. The conditions are:

- `critical: summary.critical` -- always included (correct)
- `high: if threshold_idx <= 1` -- `1 <= 1` = true, included (correct)
- `medium: if threshold_idx <= 2` -- `1 <= 2` = true, included (WRONG)
- `low: if threshold_idx <= 3` -- `1 <= 3` = true, included (WRONG)

The intent is to include only severities "at or above" the threshold. With `threshold=high`, only `critical` and `high` should be included (indices 0 and 1). But the condition `threshold_idx <= N` checks whether the threshold's index is less than or equal to each severity's hardcoded index. Since `threshold_idx=1` is less than or equal to `2` (medium) and `3` (low), those severities are incorrectly retained.

The correct logic should check whether each severity's index is less than or equal to `threshold_idx` (e.g., for medium at index 2: `2 <= threshold_idx`, which would be `2 <= 1` = false, correctly zeroing it out). The comparisons are backwards.

As a result, `threshold=high` returns counts for all four severities instead of only critical and high. This criterion is not satisfied.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines in diff constructing the filtered `AdvisorySummary`:
  ```rust
  high: if threshold_idx <= 1 { summary.high } else { 0 },
  medium: if threshold_idx <= 2 { summary.medium } else { 0 },
  low: if threshold_idx <= 3 { summary.low } else { 0 },
  ```
- For `threshold=high` (threshold_idx=1): all three conditions evaluate to true, so no counts are zeroed.
