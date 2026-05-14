# Criterion 4: Severity ordering is correct (critical > high > medium > low)

## Criterion Text
Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Analysis

While the severity_order array is defined correctly as `["critical", "high", "medium", "low"]` (index 0 = highest, index 3 = lowest), the filtering logic that uses this ordering is broken, making the effective ordering incorrect in practice.

The array definition itself correctly encodes `critical > high > medium > low`:
```rust
let severity_order = ["critical", "high", "medium", "low"];
// critical=0, high=1, medium=2, low=3
```

However, the filtering conditions invert the intended ordering behavior:
```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For threshold=critical (idx=0), the result includes high (0<=1), medium (0<=2), and low (0<=3) -- all four levels, instead of only critical. The ordering is defined but not correctly applied in the filtering logic.

Additionally, no proper `Severity` enum with `Ord` implementation was created, as specified in the Implementation Notes ("Define a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`"). Instead, string comparisons with a hardcoded array are used, which is more error-prone.

## Evidence

- The severity_order array `["critical", "high", "medium", "low"]` is correctly ordered
- The filtering conditions use `threshold_idx <= N` (where N is the hardcoded position of each severity) which is inverted
- For threshold=critical (idx=0): high (0<=1=true), medium (0<=2=true), low (0<=3=true) -- all included incorrectly
- No `Severity` enum with `Ord` trait was implemented as specified in Implementation Notes
