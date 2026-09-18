## Criterion 3: Invalid threshold returns 400 Bad Request

**Verdict: FAIL**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

### Analysis

The implementation does NOT validate the threshold parameter value. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the code silently accepts it and applies a default behavior instead of returning a 400 Bad Request error.

The relevant code in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the threshold value does not match any entry in the `severity_order` array. Instead of returning a 400 error, `.unwrap_or(0)` silently converts the missing match to index 0, which corresponds to "critical". This means any invalid threshold value (e.g., "invalid", "foo", "extreme", "123") is silently treated as `threshold=critical`.

### What should happen

Per the task's implementation notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation should:
1. Check if the threshold value matches a known severity level
2. If not, return `Err(AppError::BadRequest("Invalid threshold value: ..."))` or equivalent
3. Only proceed with filtering when the threshold value is valid

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, diff line containing `.unwrap_or(0)`
- **Missing:** No validation check, no `AppError::BadRequest` usage, no 400 response path
- **Impact:** Invalid input is silently accepted, violating the API contract and making debugging difficult for API consumers who misspell threshold values
- **Task reference:** Implementation Notes explicitly state to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
