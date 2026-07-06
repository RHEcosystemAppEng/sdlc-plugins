## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Analysis

This criterion requires that providing an unrecognized threshold value (e.g., `?threshold=invalid`) returns an HTTP 400 Bad Request error response. The task implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### Code Inspection

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` handles threshold lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold` contains an unrecognized value (e.g., `"invalid"`), `severity_order.iter().position(...)` returns `None` because `"invalid"` does not match any element in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently defaults to index 0 (the position of "critical").

This means invalid threshold values are silently treated as if `threshold=critical` were specified, and no error is returned to the client.

### What Should Happen

The code should validate the threshold parameter before proceeding with filtering. When an invalid value is provided, it should return a 400 Bad Request error using the project's existing error handling pattern. The task implementation notes specify using `common/src/error.rs::AppError` for this validation:

```rust
// Expected pattern (not implemented):
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Defect:** `.unwrap_or(0)` silently accepts invalid threshold values instead of returning a 400 error
- **Expected behavior:** `?threshold=invalid` returns HTTP 400 Bad Request
- **Actual behavior:** `?threshold=invalid` silently defaults to threshold index 0 and returns a 200 response with (incorrectly filtered) counts
- **Task reference:** Implementation Notes specify "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
