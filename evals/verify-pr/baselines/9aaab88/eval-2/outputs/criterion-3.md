# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles threshold lookup with:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `?threshold=invalid`) is provided, `severity_order.iter().position(...)` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` silently converts this to index 0 (the "critical" position).

This means an invalid threshold value is silently treated as if the user passed `threshold=critical`. The endpoint returns a 200 OK response with filtered data instead of the required 400 Bad Request error.

The task explicitly required returning 400 Bad Request for invalid threshold values and specified using `common/src/error.rs::AppError` for validation errors. None of this validation is implemented. There is no check for invalid values, no `AppError` usage, and no 400 response path.

## Conclusion

**FAIL** -- Invalid threshold values are silently accepted (defaulting to index 0) instead of returning 400 Bad Request. No input validation is implemented.
