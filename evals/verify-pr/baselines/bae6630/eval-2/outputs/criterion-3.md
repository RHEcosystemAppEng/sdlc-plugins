## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Result: FAIL

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is resolved using:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `position()` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently defaults the index to 0, treating the invalid input as equivalent to `threshold=critical`.

The task description explicitly requires:
> `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

The implementation notes also specify:
> Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)

No validation is performed. No `AppError` is returned. The code never produces a 400 Bad Request response for invalid threshold values.

### What the code should do

The code should validate the threshold parameter and return a 400 error when the value is not one of the recognized severities. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```

### Conclusion

This criterion is not met. Invalid threshold values are silently accepted and treated as "critical" due to `unwrap_or(0)`, instead of returning a 400 Bad Request error as required.
