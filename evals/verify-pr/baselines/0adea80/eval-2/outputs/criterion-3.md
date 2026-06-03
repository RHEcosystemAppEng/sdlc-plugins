# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The PR does NOT implement any validation for invalid threshold values. The relevant code is:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `.position()` returns `None`, and `.unwrap_or(0)` silently falls back to index 0 (which corresponds to "critical"). This means:

1. No 400 Bad Request error is returned for invalid input.
2. Invalid threshold values are silently treated as `threshold=critical`.
3. The `AppError` type from `common/src/error.rs` is not used for validation, despite being imported and the task notes explicitly requiring it.

The correct implementation should check whether the threshold value is a valid severity level and return a 400 Bad Request via `AppError` if it is not.

## Conclusion

This criterion is entirely unmet. Invalid threshold values are silently accepted and treated as "critical" rather than returning a 400 error response. There is no input validation whatsoever.
