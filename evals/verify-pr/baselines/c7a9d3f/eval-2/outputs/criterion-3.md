# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

This criterion requires that when an invalid threshold value is provided (e.g., `?threshold=invalid`), the endpoint returns an HTTP 400 Bad Request error response.

### Code Inspection

The threshold validation logic in `get.rs`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is provided:
1. `.position(|&s| s == threshold.to_lowercase())` returns `None` because "invalid" does not match any of the severity strings
2. `.unwrap_or(0)` silently converts the `None` to index `0`
3. The function proceeds as if `threshold=critical` was specified

### What Should Happen

The implementation should detect invalid threshold values and return an error. The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation would be something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

### Evidence

- `unwrap_or(0)` silently defaults to index 0 instead of returning an error
- No `AppError` or `BadRequest` handling anywhere in the threshold validation path
- The function signature returns `Result<Json<AdvisorySummary>, AppError>`, so returning an `AppError` for invalid input is structurally supported but not used

## Conclusion

This criterion FAILS. Invalid threshold values are silently accepted and treated as `threshold=critical` instead of returning a 400 Bad Request error. The `unwrap_or(0)` pattern masks validation errors entirely.
