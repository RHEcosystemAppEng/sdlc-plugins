# Criterion 4: Severity ordering is correct (critical > high > medium > low)

**Criterion:** Severity ordering is correct: critical > high > medium > low

**Verdict:** FAIL

## Analysis

The PR defines the severity ordering as:
```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array places severity levels in the correct descending order: critical (index 0, highest), high (index 1), medium (index 2), low (index 3, lowest). The ordering definition itself is correct.

However, the filtering logic that uses this ordering is broken. The conditions applied are:

```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // include if threshold is critical or high
medium: if threshold_idx <= 2 { summary.medium } else { 0 },   // include if threshold is critical, high, or medium
low: if threshold_idx <= 3 { summary.low } else { 0 },         // include if threshold is critical, high, medium, or low
```

The condition `threshold_idx <= N` checks whether the threshold index is at or below N. Since lower indices mean higher severity, this logic reads: "include this severity if the threshold is at least as severe as this severity." But this is backwards -- for `threshold=high` (idx=1), we get:
- medium: `1 <= 2` = true (included, but should be excluded)
- low: `1 <= 3` = true (included, but should be excluded)

The correct condition should be `N <= threshold_idx` (or equivalently, the severity's index should be less than or equal to the threshold's index), which would mean "include severities at or above the threshold level."

While the ordering array is correct, the filtering logic that depends on the ordering produces incorrect results. The task requires that `threshold=high` returns only critical and high, but the implementation returns all four severities for any threshold value except "low" (which would also return all four).

The only threshold that produces correct filtering is `threshold=critical` (idx=0): high (0<=1 true), medium (0<=2 true), low (0<=3 true) -- but that also includes everything, which is wrong. Actually no threshold value produces correct behavior.

## Conclusion

The severity ordering definition is correct but the filtering logic that uses the ordering is inverted, rendering the severity ordering effectively non-functional. This criterion fails because the ordering is not correctly applied.
