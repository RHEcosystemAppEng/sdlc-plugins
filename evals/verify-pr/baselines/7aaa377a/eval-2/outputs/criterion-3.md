# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The diff does not implement any validation for invalid threshold values. When an unrecognized threshold string is provided (e.g., `?threshold=invalid`), the code silently falls back to a default index using `unwrap_or(0)` instead of returning a 400 Bad Request error.

The task description explicitly requires: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance is not followed.

## Evidence

From the diff in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the threshold string does not match any value in the severity array. Instead of treating this as a validation error and returning a 400 Bad Request response via `AppError`, the code uses `.unwrap_or(0)` which silently treats any invalid input as index 0 (equivalent to `threshold=critical`).

This means a request like `?threshold=foobar` would silently behave as if `?threshold=critical` was specified, with no error reported to the client.

The expected implementation would use `AppError` to produce a 400 response:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

## Conclusion

This criterion is not satisfied. Invalid threshold values are silently accepted and treated as "critical" instead of producing a 400 Bad Request error. The task's implementation notes explicitly called for using `AppError` for validation errors, and this guidance was not followed.
