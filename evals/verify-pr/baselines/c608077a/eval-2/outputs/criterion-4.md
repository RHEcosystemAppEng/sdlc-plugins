# Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: PASS**

## Reasoning

The ordering is encoded as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

A lower index means a higher severity. Each count is kept when `threshold_idx <= <its index>`, and `critical` is always kept:

| threshold | idx | critical | high | medium | low |
|---|---|---|---|---|---|
| critical | 0 | kept | 0 | 0 | 0 |
| high | 1 | kept | kept | 0 | 0 |
| medium | 2 | kept | kept | kept | 0 |
| low | 3 | kept | kept | kept | kept |

So the relative ordering critical > high > medium > low is applied correctly. The comparison is case-insensitive because of `to_lowercase()`.

Notes, which do not change the verdict:
- The Implementation Notes specified a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`. The diff uses a string array instead. The ordering is correct, but the requested design was not followed, and an enum would also have made the 400 validation in criterion 3 straightforward.
- No tests check the ordering. The threshold=critical, high and medium tests are all missing.

## Evidence
- `get.rs`: `severity_order` array and the `threshold_idx <= N` comparisons
