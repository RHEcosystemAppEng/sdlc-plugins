## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Analysis

The implementation does not validate the threshold parameter value. When an unrecognized value is provided, the code silently falls back to index 0 via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

If `threshold=invalid`, `position()` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`. The `unwrap_or(0)` converts this to index 0, which corresponds to "critical". This means an invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

### What Should Happen

Per the task's implementation notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The code should check if the threshold value is valid and return `AppError::BadRequest` (or equivalent) if it is not. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

### Evidence

The `unwrap_or(0)` on the `position()` call in `get.rs` silently swallows invalid input instead of returning a 400 error response.
