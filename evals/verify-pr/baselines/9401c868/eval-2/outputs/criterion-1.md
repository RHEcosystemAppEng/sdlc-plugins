## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Result: FAIL

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses inverted comparison operators, causing the threshold filter to include severities that should be excluded.

The code defines:
```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx` = 1.

The filtering conditions are:
```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // 1 <= 1 = true -> INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 },  // 1 <= 2 = true -> INCLUDED (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },        // 1 <= 3 = true -> INCLUDED (BUG)
```

The comparison `threshold_idx <= N` is inverted. It should be `threshold_idx >= N` (or equivalently, `N <= threshold_idx`). The current logic asks "is the threshold severity at or above this level?" but the comparison direction is wrong.

With `threshold=high` (idx=1):
- `medium` (hardcoded index 2): `1 <= 2` evaluates to `true`, so medium is included. It should be excluded.
- `low` (hardcoded index 3): `1 <= 3` evaluates to `true`, so low is included. It should be excluded.

The correct condition would be `threshold_idx >= 1` for high, `threshold_idx >= 2` for medium, and `threshold_idx >= 3` for low. This way, `threshold=high` (idx=1) would yield: high: `1 >= 1` = true (include), medium: `1 >= 2` = false (exclude), low: `1 >= 3` = false (exclude).

### Additional Bug: Incorrect `total` calculation

The `total` field is computed from unfiltered counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

Even if the individual severity counts were correctly filtered to zero, the total would still reflect all severities. It should sum the filtered values instead.
