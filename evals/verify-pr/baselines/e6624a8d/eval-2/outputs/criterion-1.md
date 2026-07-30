# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

This criterion requires that when `threshold=high` is provided, the response includes only the `critical` and `high` severity counts, omitting `medium` and `low`.

### Code Inspection

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses a position-based comparison against the `severity_order` array:

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

### Defect: Inverted Comparison Direction

The comparison `threshold_idx <= N` is backwards. For `threshold=high`, `threshold_idx = 1`:

- `critical`: always included (correct)
- `high`: `1 <= 1` evaluates to `true` -- included (correct)
- `medium`: `1 <= 2` evaluates to `true` -- included (WRONG -- should be excluded)
- `low`: `1 <= 3` evaluates to `true` -- included (WRONG -- should be excluded)

The correct condition to include a severity at position P is `P <= threshold_idx` (include if the severity's rank is at or above the threshold). The code instead checks `threshold_idx <= P`, which inverts the filter:

| Threshold | Expected Result | Actual Result |
|---|---|---|
| critical (idx=0) | critical only | all four severities |
| high (idx=1) | critical + high | all four severities |
| medium (idx=2) | critical + high + medium | all four severities |
| low (idx=3) | all four severities | critical + low only |

The filtering is completely inverted -- stricter thresholds include more results, and the most permissive threshold (low) excludes the most.

### Additional Issue: Total Calculation

The `total` field is computed from unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values. Even if the filtering logic were corrected, the total would still reflect all severities rather than the filtered subset.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: filtering block in `advisory_summary` handler
- The condition `threshold_idx <= 1` for high should be `1 <= threshold_idx`
- The condition `threshold_idx <= 2` for medium should be `2 <= threshold_idx`
- The condition `threshold_idx <= 3` for low should be `3 <= threshold_idx`
