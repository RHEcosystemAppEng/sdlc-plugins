# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

This criterion requires that providing an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request error response.

### Code Inspection

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Defect: No Validation -- Silent Fallback via `unwrap_or(0)`

When the threshold value does not match any entry in the `severity_order` array, `position()` returns `None`. Instead of returning a 400 Bad Request error, the code uses `unwrap_or(0)` to silently fall back to index 0 (the "critical" position).

This means:
- `?threshold=invalid` is silently treated as `?threshold=critical`
- `?threshold=foo` is silently treated as `?threshold=critical`
- `?threshold=` (empty string) is silently treated as `?threshold=critical`

No error response is ever generated for invalid threshold values. The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

### Expected Implementation

The code should validate the threshold value and return an error when it does not match a known severity:

```rust
// Expected approach (not implemented):
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

The `AppError` enum from `common/src/error.rs` is already imported in this file and would be the correct mechanism for returning 400 errors, consistent with the error handling pattern used elsewhere in the codebase.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `unwrap_or(0)` call on the position lookup silently accepts any string value
- No `AppError::BadRequest` or equivalent 400 error is returned anywhere in the threshold handling code
- The `AppError` type is imported (`use common::error::AppError`) but not used for threshold validation
- Task Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
