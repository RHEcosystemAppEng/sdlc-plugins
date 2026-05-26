# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task requires that invalid threshold values (values other than "critical", "high", "medium", "low") return a 400 Bad Request error. The implementation does not validate the threshold parameter; instead, it silently falls back to a default behavior.

The code uses `severity_order.iter().position(|&s| s == threshold.to_lowercase()).unwrap_or(0)` to find the threshold's index. When the threshold value is not found in the `severity_order` array, `position()` returns `None`, and `unwrap_or(0)` converts this to index `0` (which corresponds to "critical"). This means an invalid threshold like `?threshold=invalid` is silently treated as `?threshold=critical`, returning only critical counts without any error indication.

The task explicitly requires returning 400 Bad Request for invalid values, and the implementation notes state to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation should:
1. Check if the threshold value is in the allowed set
2. If not, return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent

## Evidence

From the PR diff in `get.rs`, lines 43-46:
```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.unwrap_or(0)` silently accepts any input. No validation error is returned. The `AppError` type is imported but never used for threshold validation.
