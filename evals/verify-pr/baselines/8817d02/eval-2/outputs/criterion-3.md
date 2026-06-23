# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Reasoning

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is looked up in the `severity_order` array using `.position()`, and the result is handled with `.unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `.position()` returns `None`, and `.unwrap_or(0)` silently falls back to index 0 ("critical"). This means an invalid threshold value is treated as `threshold=critical` rather than returning a 400 Bad Request error.

**What should happen:** The task's Implementation Notes explicitly state to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The code should check if the threshold value is valid, and if not, return an `AppError` that maps to HTTP 400 Bad Request.

**What actually happens:** Invalid input is silently accepted and treated as the most restrictive threshold (critical only). No validation error is returned.

**Evidence:**
- Line 45-46 of the diff: `.unwrap_or(0)` replaces what should be error handling
- The `AppError` import exists at line 14 (`use common::error::AppError;`) but is not used for threshold validation
- No `Err(AppError::...)` or `return Err(...)` path exists for invalid threshold values
