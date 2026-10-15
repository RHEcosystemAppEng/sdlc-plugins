## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Analysis

The endpoint handler in `modules/fundamental/src/advisory/endpoints/get.rs` adds threshold filtering logic, but the comparison direction is inverted, causing incorrect results.

The code constructs a severity ordering array and uses `position()` to find the threshold index:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx = 1`.

The filtering conditions are:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

Tracing through with `threshold_idx = 1`:
- `high`: `1 <= 1` = true => included (correct)
- `medium`: `1 <= 2` = true => **included** (WRONG -- medium should be excluded when threshold=high)
- `low`: `1 <= 3` = true => **included** (WRONG -- low should be excluded when threshold=high)

The comparison is inverted. The code checks `threshold_idx <= severity_fixed_index` but should check `severity_fixed_index <= threshold_idx`. The correct conditions would be:
- `high`: `if 1 <= threshold_idx` (include high when threshold is high or lower)
- `medium`: `if 2 <= threshold_idx` (include medium when threshold is medium or lower)
- `low`: `if 3 <= threshold_idx` (include low only when threshold is low)

With the correct logic and `threshold=high` (idx=1): high `1 <= 1` = true, medium `2 <= 1` = false, low `3 <= 1` = false -- which correctly returns only critical and high.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) instead of from the filtered values, so even if the per-severity filtering worked correctly, the total would still be wrong.

### Evidence

Lines from the diff in `get.rs`:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
total: summary.critical + summary.high + summary.medium + summary.low,
```
