# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## Evidence

The code in `modules/fundamental/src/advisory/endpoints/get.rs` handles an unrecognized threshold value with `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided:
1. `threshold.to_lowercase()` yields `"invalid"`
2. `.position(|&s| s == "invalid")` returns `None` since "invalid" is not in the `["critical", "high", "medium", "low"]` array
3. `.unwrap_or(0)` silently converts `None` to `0`, treating "invalid" as if the user had specified `threshold=critical`

The task explicitly requires returning a **400 Bad Request** error for invalid threshold values. The implementation notes reference `common/src/error.rs::AppError` for validation errors. The correct implementation would be to check for `None` from `.position()` and return `Err(AppError::BadRequest("Invalid threshold value"))` or similar.

Instead, the code silently accepts any string and defaults to the most restrictive filter (critical only, index 0). This is a security and usability concern -- the user receives no feedback that their input was invalid. This is a clear FAIL.
