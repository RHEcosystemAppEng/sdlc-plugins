# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The diff adds a `SummaryParams` struct with an `Option<String>` threshold field and filtering logic in the `advisory_summary` handler. However, the filtering logic contains a fundamental correctness bug.

### Filtering logic in the diff

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

### Bug: comparison direction is inverted

The severity ordering is `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3. When `threshold=high`, `threshold_idx = 1`.

The code checks whether `threshold_idx <= N` for each field. For `threshold=high` (idx=1):
- `high`: `1 <= 1` = true (included) -- correct
- `medium`: `1 <= 2` = true (included) -- WRONG, should be excluded
- `low`: `1 <= 3` = true (included) -- WRONG, should be excluded

The comparison should check whether each severity's index is at or above the threshold (i.e., `severity_index <= threshold_idx`), not whether the threshold index is less than or equal to a hardcoded constant. The logic as written effectively includes ALL severities regardless of threshold for most threshold values.

### Additional issue: total field uses unfiltered counts

The `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low` which uses the original unfiltered values, not the filtered values. Even if the filtering were correct, the total would be wrong.

### Conclusion

The filtering mechanism is present in skeleton form but does not correctly filter severities. With `threshold=high`, medium and low counts would still be included rather than zeroed out. This criterion is not met.
