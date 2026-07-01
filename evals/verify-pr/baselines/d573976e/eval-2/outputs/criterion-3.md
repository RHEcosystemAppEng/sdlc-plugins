# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The code does not validate the threshold parameter against valid values. Instead of returning a 400 Bad Request error for invalid threshold values, the code silently falls back to a default using `.unwrap_or(0)`.

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Detailed Reasoning

When a client sends `?threshold=invalid`, the following happens:

1. `threshold.to_lowercase()` produces `"invalid"`
2. `severity_order.iter().position(|&s| s == "invalid")` searches `["critical", "high", "medium", "low"]` for `"invalid"` -- no match is found, returning `None`
3. `.unwrap_or(0)` converts the `None` to index `0`
4. The code proceeds as if `threshold=critical` was specified

This means any invalid input string (e.g., "invalid", "foo", "xyz", "123") is silently treated as equivalent to `threshold=critical`. No error is returned to the client.

### What Should Happen

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation should:

1. Check if `threshold.to_lowercase()` matches one of the valid values in `severity_order`
2. If not, return `Err(AppError::BadRequest("Invalid threshold value".into()))` (or equivalent)
3. Only proceed with filtering if the threshold value is valid

The `AppError` type is already imported (`use common::error::AppError;`) and available for use, but the code never uses it for threshold validation.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line: `.unwrap_or(0)` silently accepts invalid input
- `AppError` is imported but not used for threshold validation
- Task Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
- Acceptance Criterion 3 explicitly requires 400 Bad Request for invalid threshold values
