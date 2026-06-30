## Criterion 4: Severity ordering is correct: critical > high > medium > low

**Result: PASS (with caveats)**

### Evidence

The severity ordering is defined in `get.rs` as a static array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array assigns index 0 to critical, 1 to high, 2 to medium, and 3 to low. Since lower indices represent higher severity, the ordering critical (0) > high (1) > medium (2) > low (3) is correctly represented.

The task specified implementing a `Severity` enum with `Ord`, but the implementation uses a string array with positional indexing instead. While the ordering is technically encoded correctly in the array, the approach is fragile -- it depends on the array ordering being correct and does not leverage Rust's type system for compile-time safety.

### Caveats

Although the ordering itself is correctly defined, the filtering logic that depends on it is broken (see Criterion 1). The ordering is correct in isolation, but the comparisons that use it produce wrong results due to the inverted condition.

### Conclusion

This criterion narrowly passes because the ordering definition itself is correct (critical > high > medium > low), even though the code that uses the ordering is incorrect.
