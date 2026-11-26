# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

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

## Reasoning

- `threshold=high` gives `threshold_idx = 1`. `critical` and `high` are kept, and `medium` and `low` are set to `0`. The individual counts are masked correctly.
- **`total` is computed from the unfiltered `summary` fields.** It still includes the medium and low counts. Example: with critical=2, high=3, medium=5, low=7 the response is `{critical:2, high:3, medium:0, low:0, total:17}`. The correct total is 5. The response contradicts itself: its total covers severities that were supposedly filtered out.
- The task Description says medium and low should be *omitted*. Instead they are returned as `0`, which a client cannot tell apart from "no medium/low advisories exist".
- The filtering is done in the handler after aggregation. The Implementation Notes asked for an optional WHERE clause on severity rank in the aggregation query in `advisory.rs`. That hunk in the diff contains only context lines and changes nothing.
- No test covers this behavior. The required `tests/api/advisory_summary.rs` is missing, including the "threshold=high returns critical and high counts" test.

Because `total` still reflects all severities, the endpoint does not return "counts for critical and high only". The criterion is not met.
