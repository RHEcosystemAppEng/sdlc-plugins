## Criterion 3: Invalid threshold returns 400 Bad Request

**Verdict: FAIL**

### Requirement

`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

### Analysis

The code does not validate the threshold value. Instead, it uses `.unwrap_or(0)` to silently fall back to index 0 when the threshold string does not match any entry in the severity array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided:
1. `severity_order.iter().position(...)` returns `None` because "invalid" does not match any of "critical", "high", "medium", "low"
2. `.unwrap_or(0)` converts `None` to `0`
3. The code proceeds as if `threshold=critical` was specified
4. No error response is generated -- the request succeeds with HTTP 200

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The expected behavior would be something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value"))?;
```

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 46 in the diff
- `.unwrap_or(0)` silently accepts any string without validation
- No usage of `AppError` for threshold validation anywhere in the diff
- The `common/src/error.rs::AppError` enum is available (referenced in imports) but not used for this purpose
- An invalid threshold like "invalid", "foo", or "" would be silently treated as threshold=critical

### Conclusion

Invalid threshold values are silently accepted instead of producing a 400 Bad Request error. The criterion is not satisfied.
