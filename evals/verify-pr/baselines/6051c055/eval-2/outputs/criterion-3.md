# Criterion 3 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The code does not validate the threshold parameter value. When an invalid threshold value is provided (e.g., "invalid", "xyz", "extreme"), the code silently accepts it and falls back to index 0 via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Behavior for threshold="invalid"

1. `severity_order.iter().position(|&s| s == "invalid")` returns `None` (no match found)
2. `.unwrap_or(0)` converts `None` to `0`
3. `threshold_idx = 0` (same as threshold="critical")
4. The endpoint returns a filtered response as if threshold="critical" was specified

### What Should Happen

According to the acceptance criterion and the Implementation Notes (which specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"), the endpoint should:

1. Validate the threshold value against the known severity levels
2. If the value is not one of ["critical", "high", "medium", "low"], return `400 Bad Request` with an appropriate error message using `AppError`

### Gap

No validation logic exists. The `unwrap_or(0)` pattern silently swallows invalid input, making it impossible for API consumers to detect typos or incorrect threshold values. The `AppError` type is imported (`use common::error::AppError`) but never used for threshold validation.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line containing `.unwrap_or(0)`
- No `return Err(AppError::...)` or equivalent validation error path exists for invalid threshold values
- The `AppError` import is present but unused for this purpose
