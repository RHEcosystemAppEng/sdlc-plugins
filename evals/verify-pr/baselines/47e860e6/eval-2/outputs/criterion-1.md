# Criterion 1 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## What was checked
The new `match &params.threshold` block in `modules/fundamental/src/advisory/endpoints/get.rs` (handler `advisory_summary`).

## What was found
```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = ...position(...).unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high:   if threshold_idx <= 1 { summary.high }   else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low:    if threshold_idx <= 3 { summary.low }    else { 0 },
    total:  summary.critical + summary.high + summary.medium + summary.low,
}
```

For `threshold=high`, `threshold_idx = 1`. Then:
- `high`: `1 <= 1` -> kept
- `medium`: `1 <= 2` -> **kept** (should be excluded)
- `low`: `1 <= 3` -> **kept** (should be excluded)

The comparison is inverted. A severity at index `i` should be kept when `i <= threshold_idx`, but the code checks `threshold_idx <= i`. So `threshold=high` returns all four counts unfiltered. The inversion affects every threshold value:

| threshold | expected kept | actually kept |
|---|---|---|
| critical (0) | critical | critical, high, medium, low |
| high (1) | critical, high | critical, high, medium, low |
| medium (2) | critical, high, medium | critical, low |
| low (3) | all | critical, low |

Two more problems:
- `total` is summed from the **unfiltered** `summary` fields, so it never matches the filtered counts.
- Excluded severities come back as `0` rather than being left out of the response. The task description says "omitting `medium` and `low`". Zeroing them could be acceptable on its own, but here the values are not even zeroed correctly.

The task's Implementation Notes asked for filtering in the aggregation query (an optional WHERE clause on severity rank in `advisory.rs`). That was not done. The `advisory.rs` hunk adds no functional code.

No test exists for this behavior. The Test Requirements "threshold=high returns critical and high counts" and the planned `tests/api/advisory_summary.rs` file are both missing.

**Verdict: FAIL.** `threshold=high` returns medium and low counts too.
