# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The criterion requires that passing an invalid threshold value (e.g., `?threshold=invalid`) returns an HTTP 400 Bad Request error. The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The PR's filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is passed:
1. `severity_order.iter().position(...)` returns `None` because "invalid" does not match any of ["critical", "high", "medium", "low"].
2. `.unwrap_or(0)` silently converts the `None` to `0`, which is the index for "critical".

This means an invalid threshold value is **silently treated as `threshold=critical`** rather than returning a 400 error. No validation error is produced. The `AppError` type from `common/src/error.rs` is already imported but is never used for threshold validation.

### What the correct implementation should do

The implementation should:
1. Attempt to parse the threshold value against valid severity names.
2. If the value is not one of ["critical", "high", "medium", "low"], return an `AppError` that maps to HTTP 400 Bad Request.
3. Only proceed with filtering if the threshold value is valid.

For example:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```
