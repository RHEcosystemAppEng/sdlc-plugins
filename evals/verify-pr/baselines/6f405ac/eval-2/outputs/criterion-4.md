# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: PASS

## Reasoning

The severity ordering is defined by the `severity_order` array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This places "critical" at index 0 (highest severity) and "low" at index 3 (lowest severity). The ordering correctly reflects the requirement that critical > high > medium > low.

The `.position()` call returns the index of the matched severity string in this array. Higher severity levels have lower indices, which is used by the subsequent comparison logic to determine which severity levels to include.

While the filtering logic that uses this ordering has bugs (see Criterion 1), the ordering definition itself is correct.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Array: `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3
- critical (0) < high (1) < medium (2) < low (3) in index terms, meaning critical has the highest priority
- This correctly encodes critical > high > medium > low
