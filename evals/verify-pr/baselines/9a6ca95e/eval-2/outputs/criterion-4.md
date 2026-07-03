# Criterion 4

**Criterion**: Severity ordering is correct: critical > high > medium > low

## Analysis

The severity ordering is defined in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array correctly represents the severity ordering with `critical` (index 0) as the most severe and `low` (index 3) as the least severe.

However, the task specifies: "Define a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`." The implementation uses a hardcoded string array instead of a proper enum with `Ord`. This is a deviation from the implementation notes, though not directly stated in the acceptance criterion.

More critically, while the ordering in the array is correct, the comparison logic that uses this ordering is inverted (as detailed in Criterion 1). The conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` do not correctly filter based on the severity ordering. For example, with `threshold=critical` (idx=0), the code includes all severities because `0 <= 1`, `0 <= 2`, and `0 <= 3` are all true — the opposite of the intended behavior of showing only critical.

## Verdict: FAIL

While the severity ordering in the array definition is correct (critical > high > medium > low), the comparison logic that applies this ordering is inverted, causing the filtering to produce incorrect results. Additionally, no `Severity` enum with `Ord` implementation was created as specified.
