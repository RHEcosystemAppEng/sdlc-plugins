# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The implementation does not validate the threshold parameter value. When an invalid value like `"invalid"` is provided, the code silently accepts it instead of returning a 400 Bad Request error.

### Code trace for `threshold="invalid"`

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call searches for `"invalid"` in the array `["critical", "high", "medium", "low"]`. Since `"invalid"` does not match any element, `.position()` returns `None`. The `.unwrap_or(0)` then defaults to index `0`, which is the index for `"critical"`.

This means `?threshold=invalid` silently behaves the same as `?threshold=critical`. The user receives a 200 OK response with filtered data instead of a 400 Bad Request error indicating the threshold value is not recognized.

### What the correct implementation should do

The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct approach would be to check whether `.position()` returns `None` and, if so, return an `AppError` that maps to HTTP 400 Bad Request. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line: `.unwrap_or(0)` silently converts unrecognized threshold values to index 0
- No validation error is returned for invalid input
- The task explicitly requires 400 Bad Request for invalid threshold values
