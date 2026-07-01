# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

**Verdict:** FAIL

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold lookup as follows:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The critical issue is the `.unwrap_or(0)` call. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `position()` method returns `None` because "invalid" does not match any entry in `severity_order`. Instead of returning a 400 Bad Request error, `.unwrap_or(0)` silently maps the `None` to index `0`, which corresponds to "critical".

This means:
- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=foo` silently behaves as `?threshold=critical`
- `?threshold=` (empty string) silently behaves as `?threshold=critical`
- Any unrecognized value is accepted without error

The task description explicitly states: "return 400 for invalid threshold values" and references reusing `common/src/error.rs::AppError` for validation errors. The implementation notes say: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)".

The correct implementation should:
1. Check if `position()` returns `None`
2. If so, return an `Err(AppError::BadRequest(...))` or similar 400-status error
3. Only proceed with the index if `position()` returns `Some(idx)`

For example, the correct pattern would be:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request("Invalid threshold value"))?;
```

**Conclusion:** The implementation silently accepts invalid threshold values instead of returning 400 Bad Request. This is a clear violation of the acceptance criterion. The `unwrap_or(0)` pattern masks input validation errors, which is both a correctness issue and could be considered a security concern (unexpected behavior on malformed input).
