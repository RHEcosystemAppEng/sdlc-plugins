# Criterion 4 — FAIL

**Criterion:** Severity ordering is correct: critical > high > medium > low

## What was checked
How severity order is represented and applied in `advisory_summary` (`modules/fundamental/src/advisory/endpoints/get.rs`).

## What was found
- The ordering is a string array, `["critical", "high", "medium", "low"]`. The array itself lists the severities in the right order.
- The Implementation Notes required "a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`". No such enum exists.
- The comparisons that apply the ordering are inverted (`threshold_idx <= i` instead of `i <= threshold_idx`; see criterion 1). In practice:
  - `threshold=critical` keeps everything. It should keep only critical.
  - `threshold=medium` and `threshold=low` drop high (and medium) while keeping low. A lower severity passes the filter while a higher one does not.
  - `critical` is always kept, whatever the threshold.

So the filter does not respect critical > high > medium > low. Lower severities are sometimes kept while higher ones are dropped.

**Verdict: FAIL.** The ordering array is correct but is applied backwards, and the required `Ord`-implementing `Severity` enum is missing.
