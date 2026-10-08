## Criterion 4: Severity ordering is correct: critical > high > medium > low

### Result: PASS

### Analysis

The severity ordering is defined in the code as:
```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array places `critical` at index 0 (highest severity) and `low` at index 3 (lowest severity), correctly encoding the ordering critical > high > medium > low as specified in the task.

The ordering definition itself is correct. The filtering logic that uses this ordering has a separate bug (inverted comparison operators, covered in criterion 1), but the ordering declaration faithfully represents the required severity hierarchy.

Note: The task's implementation notes suggested defining a `Severity` enum with `Ord` implementation for type safety. The PR instead uses a string array with positional indexing, which is less robust but does encode the correct ordering. The enum approach would provide compile-time guarantees and cleaner validation.
