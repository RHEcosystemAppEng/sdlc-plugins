# Criterion 3

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Analysis

The code in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like `"invalid"` is provided:
1. `severity_order.iter().position(...)` returns `None` because `"invalid"` does not match any entry in `["critical", "high", "medium", "low"]`.
2. `.unwrap_or(0)` silently converts `None` to `0`, treating the invalid value as `threshold=critical`.

No `AppError::BadRequest` or 400 status code is ever returned. The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation should detect that the `position()` call returned `None` and return an error, e.g.:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

## Verdict: FAIL

Invalid threshold values are silently accepted and treated as `threshold=critical` instead of returning a 400 Bad Request response. There is no input validation whatsoever.
