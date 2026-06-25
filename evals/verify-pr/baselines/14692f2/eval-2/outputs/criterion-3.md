# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task requires that an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request error. The implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)".

### What the diff implements

The diff uses `unwrap_or(0)` when looking up the threshold value in the severity ordering:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like "invalid" is passed:
1. `.position()` returns `None` because "invalid" does not match any of `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` silently converts this to index 0 (equivalent to "critical")
3. The endpoint returns a 200 OK response with filtered data, treating the invalid input as if `threshold=critical` was requested

### What should happen

The handler should validate the threshold value against the known severity levels and return a 400 Bad Request error (using `AppError`) for unrecognized values. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!(
        "Invalid threshold '{}'. Must be one of: critical, high, medium, low",
        threshold
    )))?;
```

### Conclusion

This criterion is not met. Invalid threshold values are silently accepted instead of producing a 400 error. The `unwrap_or(0)` pattern masks input validation errors.
