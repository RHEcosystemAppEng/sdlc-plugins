## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Analysis

The diff does NOT validate the threshold parameter value. When an invalid threshold string is provided, the code uses `.unwrap_or(0)` to silently default to index 0:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the threshold value is not found in the `severity_order` array. Instead of returning a 400 Bad Request error using `AppError::BadRequest` (as specified in the implementation notes referencing `common/src/error.rs::AppError`), the code silently falls back to index 0 (which corresponds to "critical").

This means `?threshold=invalid` would behave identically to `?threshold=critical`, silently accepting any arbitrary string without informing the client of the invalid input.

### Expected Implementation

The task explicitly states: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The correct implementation would be:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Evidence

Line 45-46 of the diff in `get.rs`: `.unwrap_or(0)` instead of returning an error. No `AppError::BadRequest` or equivalent 400 response is generated anywhere in the diff for invalid threshold values.

### Verdict

FAIL -- Invalid threshold values are silently accepted and treated as "critical" instead of returning 400 Bad Request.
