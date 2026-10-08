## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Result: FAIL

### Analysis

The task requires that an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request error. The implementation does not validate the threshold value at all.

The relevant code is:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid`:
1. `"invalid".to_lowercase()` = `"invalid"`
2. `.position(|&s| s == "invalid")` searches `["critical", "high", "medium", "low"]` and finds no match, returning `None`
3. `.unwrap_or(0)` converts `None` to `0`

The result is `threshold_idx = 0`, which is the same index as "critical". The endpoint silently treats any unrecognized threshold string as if `threshold=critical` was passed. No error is returned to the client.

### Expected Behavior

Per the implementation notes, the code should "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation would:

1. Check if the threshold string matches a known severity value
2. If not, return `Err(AppError::BadRequest("Invalid threshold value".into()))` or equivalent
3. Only proceed with filtering if the threshold is valid

Example of correct validation:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(
        format!("Invalid threshold value: '{}'. Must be one of: critical, high, medium, low", threshold)
    ))?;
```

This is a significant gap because clients sending typos or unsupported values receive a successful but incorrectly filtered response instead of a clear error.
