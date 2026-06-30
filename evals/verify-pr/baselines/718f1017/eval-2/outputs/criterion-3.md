## Criterion 3

**Text**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict**: FAIL

**Evidence**: The diff does NOT implement validation for invalid threshold values. In `modules/fundamental/src/advisory/endpoints/get.rs`, lines 44-46 show:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., "invalid") is provided, `.position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). Instead of returning a 400 Bad Request error, the endpoint treats the invalid value as if `threshold=critical` was specified.

The task implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The correct implementation would check if the position lookup returns `None` and return `AppError::BadRequest` (or equivalent) in that case. This validation is entirely absent.
