## Criterion 1: threshold=high returns counts for critical and high only

**Verdict: FAIL**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses comparison conditions that are inverted. The code constructs:

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
    ...
}
```

For `threshold=high`, `threshold_idx` resolves to `1`. The conditions then evaluate as:

| Field    | Condition      | Evaluates To | Included? | Expected |
|----------|---------------|--------------|-----------|----------|
| critical | always        | --           | Yes       | Yes      |
| high     | 1 <= 1        | true         | Yes       | Yes      |
| medium   | 1 <= 2        | true         | Yes       | **No**   |
| low      | 1 <= 3        | true         | Yes       | **No**   |

The comparison `threshold_idx <= N` is backwards. The correct condition to include severity at array position N when the threshold is at position `threshold_idx` should be `N <= threshold_idx` (include severities whose position is at or before the threshold position). With the current logic, `threshold=high` would return counts for all four severity levels, not just critical and high.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-56 in the diff
- The conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` produce incorrect filtering for any threshold value other than `low`
- For `threshold=critical` (idx=0): includes all four severities instead of only critical
- For `threshold=high` (idx=1): includes all four severities instead of only critical and high
- For `threshold=medium` (idx=2): excludes high but includes low, when it should include high and exclude low

### Conclusion

The filtering logic does not correctly implement the threshold semantics. The criterion is not satisfied.
