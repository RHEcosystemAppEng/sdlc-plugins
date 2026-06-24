## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Result: PASS (with caveat)

### Evidence

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses an index-based approach:

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

For `threshold=high`, `threshold_idx` would be 1. This means:
- `critical`: included (always included)
- `high`: `1 <= 1` is true, so included
- `medium`: `1 <= 2` is true -- **BUG**: medium is also included when it should be filtered out
- `low`: `1 <= 3` is true -- **BUG**: low is also included when it should be filtered out

Wait -- re-reading the logic more carefully: the index comparison is backwards. When `threshold_idx = 1` (high), `threshold_idx <= 2` is true, so medium IS included. This means the filtering is actually **wrong** -- it includes severities *below* the threshold rather than excluding them.

**Correction**: Actually, re-examining: the intent appears to be that severities at positions <= threshold_idx are "at or above" the threshold. In the array `["critical", "high", "medium", "low"]`, index 0 = critical (highest), index 1 = high, etc. So for `threshold=high` (idx=1), the condition `threshold_idx <= 1` for high means "is threshold index at most 1" -- this is checking if the *threshold* is at or above the *field's* position, not the other way around.

Let me re-trace:
- `threshold=high` -> `threshold_idx = 1`
- `critical`: always included (correct -- critical is above high)
- `high`: `threshold_idx <= 1` -> `1 <= 1` -> true -> included (correct)
- `medium`: `threshold_idx <= 2` -> `1 <= 2` -> true -> included (**INCORRECT** -- medium is below high and should be excluded)
- `low`: `threshold_idx <= 3` -> `1 <= 3` -> true -> included (**INCORRECT** -- low is below high and should be excluded)

The logic is inverted. The condition should be checking if each severity's index is <= threshold_idx (i.e., `severity_position <= threshold_idx`), not `threshold_idx <= severity_position`. The correct conditions would be:
- `high`: `1 <= threshold_idx` (where 1 is high's position)
- `medium`: `2 <= threshold_idx` (where 2 is medium's position)
- `low`: `3 <= threshold_idx` (where 3 is low's position)

So for `threshold=high` (idx=1): high (1 <= 1, included), medium (2 <= 1, excluded), low (3 <= 1, excluded).

The implemented logic `threshold_idx <= N` is the reverse of what's needed. This means the filtering is **broken** -- for `threshold=high`, all severities are still returned.

### Conclusion

**FAIL** -- The filtering logic is inverted. For `threshold=high`, medium and low counts are incorrectly included because the comparison `threshold_idx <= 2` and `threshold_idx <= 3` are both true when they should be false. The correct check should compare each severity's position against the threshold index, not the other way around.

Additionally, the `total` field is computed from unfiltered counts rather than from the filtered values, which is a secondary bug.
