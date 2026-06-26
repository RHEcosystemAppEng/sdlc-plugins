# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Result: FAIL

## Evidence

The severity ordering constant is defined correctly in the code:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This places critical at index 0 (highest), high at index 1, medium at index 2, and low at index 3 (lowest), which correctly represents the ordering critical > high > medium > low.

However, the filtering logic that uses this ordering is inverted. The conditions check `threshold_idx <= N` when they should check `threshold_idx >= N` (or equivalently, `N <= threshold_idx`). This means the ordering is not effectively applied correctly in practice:

- For `threshold=critical` (idx=0): all severities are included (should only be critical)
- For `threshold=high` (idx=1): all severities are included (should be critical + high)
- For `threshold=medium` (idx=2): critical and medium are included, but high is excluded (should be critical + high + medium)
- For `threshold=low` (idx=3): critical, medium, and low are included, but high is excluded (should be all four)

While the ordering array itself is correct, the logic that applies it produces results that contradict the severity ordering in every case except the trivial no-threshold case. The effective behavior does not respect the ordering, so this criterion is FAIL.
