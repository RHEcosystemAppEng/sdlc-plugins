# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task requires that invalid threshold values (values other than "critical", "high", "medium", "low") return a 400 Bad Request response. The implementation notes specifically state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Defect: Silent Fallback Instead of Validation Error

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `severity_order.iter().position(...)` returns `None` because "invalid" does not match any entry in the array. The code then uses `.unwrap_or(0)` to silently default to index 0 (which corresponds to "critical").

This means:
- `?threshold=invalid` is silently treated as `?threshold=critical`
- `?threshold=foo` is silently treated as `?threshold=critical`
- `?threshold=` (empty string) is silently treated as `?threshold=critical`

No validation error is raised. No 400 Bad Request is returned. The `AppError` type from `common/src/error.rs` is available in scope (imported at the top of the file) but is never used for threshold validation.

### Expected Implementation

The code should validate the threshold value before using it and return a 400 Bad Request error for unrecognized values. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(
        format!("Invalid threshold value: '{}'. Must be one of: critical, high, medium, low", threshold)
    ))?;
```

### Conclusion

Invalid threshold values are silently accepted and treated as "critical" instead of returning 400 Bad Request. This criterion is not satisfied.
