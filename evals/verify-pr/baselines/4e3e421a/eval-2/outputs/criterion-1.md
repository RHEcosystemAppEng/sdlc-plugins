# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: NOT MET (FAIL)**

## Reasoning

The filter is in `modules/fundamental/src/advisory/endpoints/get.rs`:

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

Tracing `threshold=high`, which gives `threshold_idx = 1`:
- `critical`: always kept.
- `high`: `1 <= 1`, true, so kept.
- `medium`: `1 <= 2`, true, so **kept**. It should be dropped.
- `low`: `1 <= 3`, true, so **kept**. It should be dropped.

The comparisons are inverted. A severity at index `i` should be kept when `i <= threshold_idx`. The code checks `threshold_idx <= i` instead. So `?threshold=high` returns all four counts unchanged, which is the opposite of what the criterion asks for. Criterion 4 covers the same inversion.

There is a second, separate defect. `total` adds up the unfiltered `summary.*` values, so even if the per-severity filtering were fixed, `total` would still include the excluded severities. With 2 critical, 3 high, 5 medium and 7 low, the expected response is `critical=2, high=3, total=5`. This implementation returns `critical=2, high=3, medium=5, low=7, total=17`.

Other deviations from the task:
- The task description says medium and low should be *omitted*. At best this code zeroes them, and only for other thresholds.
- The filter was supposed to go into the aggregation query in `modules/fundamental/src/advisory/service/advisory.rs`, as an optional WHERE clause on severity rank. That file's only hunk (`@@ -45,6 +45,7 @@`) has context lines and no changes.

## Test coverage
None. The required test "threshold=high returns critical and high counts" is missing because `tests/api/advisory_summary.rs` was never created. That test would have caught both defects.
