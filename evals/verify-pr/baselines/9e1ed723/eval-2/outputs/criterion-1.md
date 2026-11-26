# Criterion 1 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## What was checked
- `modules/fundamental/src/advisory/endpoints/get.rs`, the `Some(threshold)` arm of the new `match &params.threshold` block.
- `modules/fundamental/src/advisory/service/advisory.rs` (the diff hunk only shows context lines; nothing was added or removed there).

## What was found
For `threshold=high`, `threshold_idx` is 1. Each condition then evaluates as follows:
- `critical` = `summary.critical` (always kept, no condition)
- `high: if threshold_idx <= 1` gives `1 <= 1`, true, so high is **kept**
- `medium: if threshold_idx <= 2` gives `1 <= 2`, true, so medium is **kept** (it should be removed)
- `low: if threshold_idx <= 3` gives `1 <= 3`, true, so low is **kept** (it should be removed)

**The comparisons are inverted.** A severity at index `i` should be kept only when `i <= threshold_idx`. The code checks `threshold_idx <= i` instead. What each threshold actually returns:

| threshold | idx | Expected non-zero buckets | Actual non-zero buckets |
|---|---|---|---|
| critical | 0 | critical | critical, high, medium, low (no filtering) |
| high | 1 | critical, high | critical, high, medium, low (no filtering) |
| medium | 2 | critical, high, medium | critical, medium, low |
| low | 3 | all | critical, low |

So `?threshold=high` gives the same counts as no threshold at all, and lower thresholds remove the wrong buckets.

Also:
- **`total` is computed from unfiltered counts**: `total: summary.critical + summary.high + summary.medium + summary.low` uses the original `summary` values, so `total` always reflects every severity, whatever the threshold.
- Filtered severities would be returned as `0`, not left out. The task description says medium and low should be "omitted".
- The task's Implementation Notes asked for filtering in the aggregation query in `advisory.rs` (an optional WHERE clause on severity rank). That was not done. The filtering is done in the handler after aggregation instead.

## Conclusion
The response for `threshold=high` still carries medium and low counts and an unfiltered total. The criterion is not satisfied.

**Verdict: FAIL**
