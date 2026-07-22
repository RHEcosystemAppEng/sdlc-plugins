## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Verdict: FAIL

### What was checked

The PR diff was inspected for validation logic that detects invalid threshold values (values other than "critical", "high", "medium", "low") and returns an HTTP 400 Bad Request error. The task explicitly requires returning 400 for invalid values and the Implementation Notes reference `common/src/error.rs::AppError` for validation errors.

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold lookup uses:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.unwrap_or(0)` call silently converts any unrecognized threshold value to index `0` (which corresponds to "critical"). This means:

- `?threshold=invalid` is treated as `?threshold=critical`
- `?threshold=xyz` is treated as `?threshold=critical`
- `?threshold=` (empty string) is treated as `?threshold=critical`

There is no code path that returns an `AppError` or any HTTP 400 response for invalid threshold values. The implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### Gap

The implementation silently accepts invalid threshold values instead of returning 400 Bad Request. The correct approach would be to match on the `.position()` result and return an `AppError::BadRequest` (or equivalent) when `None` is returned, e.g.:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request("Invalid threshold value"))?;
```

This is a functional correctness bug -- clients cannot distinguish between a valid `threshold=critical` request and a typo like `threshold=hgih`.
