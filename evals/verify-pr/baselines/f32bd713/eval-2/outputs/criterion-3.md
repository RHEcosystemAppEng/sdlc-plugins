# Criterion 3: Invalid threshold returns 400 Bad Request

## Verdict: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Analysis

The code does NOT validate the threshold parameter value. When an invalid threshold string is provided (e.g., "invalid", "foo", "xyz"), the `position()` call returns `None`, and `unwrap_or(0)` silently maps the invalid value to index 0 (corresponding to "critical"):

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Expected Behavior

Per the task description and acceptance criteria, an invalid threshold value should return an HTTP 400 Bad Request response. The implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation would:
1. Check if `position()` returns `None`
2. Return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent
3. The `AppError` type from `common/src/error.rs` implements `IntoResponse` and would produce a proper 400 response

### Actual Behavior

Instead of returning an error, `unwrap_or(0)` silently treats any unrecognized threshold string as if "critical" were specified. This means:
- `?threshold=invalid` silently behaves like `?threshold=critical`
- `?threshold=foo` silently behaves like `?threshold=critical`
- `?threshold=` (empty string) silently behaves like `?threshold=critical`

No 400 response is ever returned regardless of input, which is a correctness gap and a potential usability issue (callers with typos get unexpected results with no error signal).

## Evidence
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 45-46
- `unwrap_or(0)` silently maps invalid values to index 0 instead of returning an error
- The `AppError` type is imported (`use common::error::AppError`) but never used for threshold validation
- No validation logic exists anywhere in the diff for the threshold parameter value
