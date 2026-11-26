# Criterion 4 — FAIL

**Criterion:** Severity ordering is correct: critical > high > medium > low

## What was checked
- The ordering representation in `modules/fundamental/src/advisory/endpoints/get.rs`: `let severity_order = ["critical", "high", "medium", "low"];`
- How that ordering is used in the filter comparisons.
- Whether the `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord` (required by the Implementation Notes) exists.

## What was found
- The string array lists the severities in the right rank order (index 0 = most severe).
- The comparisons that use that order are **inverted**. Each bucket is kept when `threshold_idx <= i` when it should be kept when `i <= threshold_idx`. The result is that the ordering is applied backwards:
  - `threshold=critical` (idx 0) keeps all four severities.
  - `threshold=high` (idx 1) keeps all four severities.
  - `threshold=medium` (idx 2) keeps critical, medium and low, and drops high.
  - `threshold=low` (idx 3) keeps critical and low only.
  If the ordering were applied correctly, `threshold=low` would include every severity and `threshold=critical` only critical. The handler does the reverse. `critical` is always kept only because it has no condition at all.
- No `Severity` enum implementing `Ord` was added. The ordering exists only as an ad-hoc local string array, and invalid values fall back to index 0 without warning. This departs from the Implementation Notes.
- No tests cover the ordering (Test Requirements for threshold=critical/high/medium are not met).

## Conclusion
The array lists the severities in the right order, but the threshold behavior does not respect critical > high > medium > low. The criterion is not satisfied.

**Verdict: FAIL**
