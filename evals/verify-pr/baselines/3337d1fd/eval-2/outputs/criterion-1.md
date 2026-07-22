## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Verdict: FAIL

### What was checked

The PR diff was inspected for filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` that restricts the severity counts returned when `threshold=high` is specified. The expected behavior is that only `critical` and `high` counts are included, with `medium` and `low` set to zero (or omitted).

### Evidence

The filtering logic in `get.rs` (lines 41-56 of the diff) uses the following approach:

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

For `threshold=high`, `threshold_idx = 1`. Tracing the conditions:

- `critical`: always included (no condition) -- correct
- `high`: `threshold_idx(1) <= 1` evaluates to `true` -- included -- correct
- `medium`: `threshold_idx(1) <= 2` evaluates to `true` -- included -- **INCORRECT** (should be excluded)
- `low`: `threshold_idx(1) <= 3` evaluates to `true` -- included -- **INCORRECT** (should be excluded)

The condition is inverted. The code checks whether `threshold_idx <= severity_fixed_index`, which evaluates to true for all severities at or below the threshold. The correct condition should check whether the severity's index is at or above the threshold index in the ordering (i.e., `severity_index <= threshold_idx`), which would correctly include only those severities ranked at or above the threshold.

### Gap

The filtering logic is fundamentally broken -- it includes severities below the threshold instead of excluding them. For `threshold=high`, the response would include counts for all four severities (critical, high, medium, low) instead of only critical and high.

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`), so even if the individual fields were correctly zeroed, the total would still reflect all severities.
