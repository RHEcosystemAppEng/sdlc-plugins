# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Reasoning

The severity ordering is defined in the array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array correctly represents the intended ordering (critical at index 0 is highest, low at index 3 is lowest). However, the ordering is not correctly applied in the filtering logic.

The filtering conditions check `threshold_idx <= N` where N is the hardcoded index for each severity. This means that when threshold_idx is lower (higher severity), MORE severities pass the check -- the opposite of the intended behavior. For example:

- `threshold=critical` (idx=0): critical included, high included (0<=1), medium included (0<=2), low included (0<=3) -- returns ALL counts, same as no threshold
- `threshold=low` (idx=3): critical included, high included (3<=1 false, zeroed), medium included (3<=2 false, zeroed), low included (3<=3) -- returns only critical and low

The actual behavior is inverted from the specification. Higher threshold values (lower severity) should include MORE severities, not fewer. The ordering definition is correct but the application of that ordering in the filtering logic is wrong.

While the array definition alone is correct, the criterion asks that severity ordering "is correct" in context of the feature's behavior. Since the filtering logic inverts the ordering, the severity ordering is effectively incorrect in practice.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Array definition is correct: `["critical", "high", "medium", "low"]`
- Filtering logic inverts the ordering through backwards comparisons
- `threshold=critical` should return only critical; instead returns all four
- `threshold=low` should return all four; instead returns only critical and low
