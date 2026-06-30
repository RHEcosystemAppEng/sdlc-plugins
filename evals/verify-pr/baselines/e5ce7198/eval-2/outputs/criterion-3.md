## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Evidence

The code in `get.rs` handles unknown threshold values using `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `threshold=invalid`), `position()` returns `None` because "invalid" is not found in `["critical", "high", "medium", "low"]`. The `unwrap_or(0)` then silently converts this to index 0, which corresponds to `"critical"`.

This means the endpoint treats any unrecognized threshold value as `threshold=critical` rather than returning a 400 Bad Request error. There is no validation logic, no error path, and no use of `AppError` for invalid input.

### Expected Behavior

Per the task description and implementation notes:
- The endpoint should return 400 Bad Request for invalid threshold values
- The implementation should "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

### Correct Implementation

The code should validate the threshold value and return an error for invalid inputs:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Conclusion

This criterion fails. Invalid threshold values are silently accepted and treated as `threshold=critical` instead of producing a 400 Bad Request response. The `unwrap_or(0)` is incorrect; it should propagate an error via `AppError`.
