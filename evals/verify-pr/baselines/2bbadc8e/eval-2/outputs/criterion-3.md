# Criterion 3: Invalid threshold returns 400 Bad Request

## Criterion
`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The diff shows that invalid threshold values are NOT validated. The relevant code in `get.rs`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `"invalid"`) is provided:
1. `.position()` returns `None` because `"invalid"` is not found in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical")

This means an invalid threshold value is treated the same as `?threshold=critical` — no error is returned. The function continues to produce a filtered response instead of returning a 400 Bad Request.

**What should happen:** The code should check whether the threshold value is valid and return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent when the value is not one of the recognized severity levels. The implementation notes reference `common/src/error.rs::AppError` for validation errors.

**What actually happens:** The `unwrap_or(0)` silently swallows the invalid input and defaults to the most restrictive filter (critical only), which is incorrect behavior and fails the acceptance criterion.

**Evidence:** No `Err(...)`, `return Err(...)`, `AppError::BadRequest`, or any 400-related code exists in the diff. The `unwrap_or(0)` on line approximately matching the threshold lookup is the sole handling of unrecognized values.
