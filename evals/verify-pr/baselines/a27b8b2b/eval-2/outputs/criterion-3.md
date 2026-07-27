## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Analysis

The PR does not validate the threshold parameter value. When an invalid value is provided (e.g., `?threshold=invalid`), the code uses `unwrap_or(0)` on the result of `position()`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` (because the value does not match any entry in `severity_order`), `unwrap_or(0)` silently defaults to index 0, which corresponds to "critical". This means any invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

The correct implementation should check whether the threshold value is valid and return `AppError::BadRequest` (or equivalent 400 response) when it is not recognized.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- `unwrap_or(0)` silently converts invalid input to a valid index
- No 400 error response path exists for invalid threshold values
- `common/src/error.rs::AppError` is imported but not used for validation errors
