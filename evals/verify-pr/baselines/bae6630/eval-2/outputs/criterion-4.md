## Criterion 4: Severity ordering is correct: critical > high > medium > low

### Result: PASS

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the severity ordering is defined as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array places the severities in descending order:
- Index 0: critical (highest)
- Index 1: high
- Index 2: medium
- Index 3: low (lowest)

The ordering itself is correct -- `critical > high > medium > low` -- matching the requirement.

### Note

While the ordering definition is correct, the *use* of this ordering in the filtering logic has a bug (see Criterion 1). The ordering array itself, however, correctly represents the required severity hierarchy.

### Conclusion

The severity ordering definition is correct as specified.
