# Criterion 1: Threshold filtering returns only relevant severity counts

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` does implement threshold filtering logic. The code adds a `SummaryParams` struct with an optional `threshold` field and applies filtering in the handler:

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

For `threshold=high`, `threshold_idx` would be 1 (position of "high" in the array). This means:
- `critical`: always included (correct)
- `high`: `threshold_idx <= 1` is `1 <= 1` = true, so included (correct)
- `medium`: `threshold_idx <= 2` is `1 <= 2` = true, so included (**INCORRECT** -- medium should be excluded when threshold is "high")
- `low`: `threshold_idx <= 3` is `1 <= 3` = true, so included (**INCORRECT** -- low should be excluded when threshold is "high")

Wait -- re-reading more carefully. Actually the logic is inverted. The condition checks if `threshold_idx <= N` to INCLUDE the count. For `threshold=high` (idx=1):
- critical is always included
- high: idx(1) <= 1 = true, include -- correct
- medium: idx(1) <= 2 = true, include -- **WRONG**, medium should be filtered out
- low: idx(1) <= 3 = true, include -- **WRONG**, low should be filtered out

The filtering logic is incorrect. The comparison should be reversed -- it should filter OUT severities whose index is GREATER than the threshold index, not include everything at or below. The correct logic should be: include severity if the severity's own index in the ordering is <= threshold_idx (i.e., include items ranked as important or more important than the threshold). But the code compares threshold_idx against hardcoded positions instead of comparing the severity's position against the threshold position.

Actually, let me re-examine. The intended semantics: threshold=high means "include only severities at or above high", which means critical (index 0) and high (index 1). For medium (index 2), we should NOT include it. For low (index 3), we should NOT include it.

The code checks `if threshold_idx <= 1` for high. With threshold=high, threshold_idx=1, so `1 <= 1` is true -- high is included. But for medium, the code checks `if threshold_idx <= 2` -- with threshold_idx=1, `1 <= 2` is true, so medium is ALSO included. This is wrong.

The correct condition should be: include severity if `severity_position <= threshold_idx`. For high (position=1), `1 <= 1` = true (include). For medium (position=2), `2 <= 1` = false (exclude). The code has it backwards -- it checks `threshold_idx <= severity_position` instead of `severity_position <= threshold_idx`.

Additionally, the `total` field is computed from unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered counts.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 in the diff
- The comparison direction is wrong: `threshold_idx <= N` should be `N <= threshold_idx` (or equivalent)
- The total calculation uses unfiltered counts instead of filtered counts

**Conclusion:** This criterion FAILS because the filtering logic is inverted -- it includes severities that should be excluded.
