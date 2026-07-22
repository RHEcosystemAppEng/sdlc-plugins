## Criterion 4: Severity ordering is correct: critical > high > medium > low

### Verdict: PASS

### What was checked

The PR diff was inspected for the definition of the severity ordering. The expected ordering is critical > high > medium > low, meaning critical is the most severe and low is the least severe.

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the severity ordering is defined as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array correctly represents the ordering with the most severe (critical) at index 0 and the least severe (low) at index 3. The ordering definition itself is correct.

### Note

While the ordering is correctly defined, the filtering logic that uses this ordering is broken (see Criterion 1). The ordering definition satisfies this criterion, but its application in the filter conditions is inverted. The task also specified defining a `Severity` enum with `Ord` implementation, which was not done -- the implementation uses a simple string array instead. This is a design deviation but the ordering values themselves are correct.
