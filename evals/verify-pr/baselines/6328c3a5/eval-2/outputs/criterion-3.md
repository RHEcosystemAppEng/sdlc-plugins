# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles unknown threshold values with `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is passed, `position()` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` call silently defaults to index `0`, which corresponds to "critical". This means the endpoint treats any unrecognized threshold value as if `?threshold=critical` were specified, returning a 200 OK response with filtered data.

The task explicitly requires returning a 400 Bad Request for invalid threshold values. The implementation notes reference `common/src/error.rs::AppError` for validation errors, but no validation is performed. The correct implementation should:

1. Check if the threshold value matches a known severity level
2. If not, return an `AppError` variant that maps to HTTP 400
3. For example: `return Err(AppError::BadRequest(format!("Invalid threshold: {}", threshold)));`

No such validation exists anywhere in the diff. The `advisory.rs` diff adds only a blank line and contains no validation logic either. This is a significant gap: invalid input is silently accepted rather than rejected.
