## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, when the threshold value does not match any entry in the severity_order array, the code uses `.unwrap_or(0)` to silently default to index 0 (critical):

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` method returns `None` when the threshold string (e.g., "invalid") is not found in the array. Instead of returning a 400 Bad Request error, `.unwrap_or(0)` silently treats the invalid value as if `threshold=critical` was specified.

### Expected Behavior

Per the task's implementation notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The code should validate the threshold parameter and return an `AppError` (which implements `IntoResponse` to produce 400 Bad Request) when the value is not one of "critical", "high", "medium", or "low".

A correct implementation would look something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

### Conclusion

Invalid threshold values are silently accepted and treated as "critical" instead of returning a 400 Bad Request response. There is no input validation whatsoever for the threshold parameter. This is a correctness and security issue -- users receive no feedback that their query parameter was invalid.
