# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The acceptance criterion requires that an invalid threshold value (e.g., `?threshold=invalid`) returns an HTTP 400 Bad Request response. The implementation does not validate the threshold value and instead silently accepts any input.

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When the threshold string is not found in `severity_order` (e.g., "invalid", "banana", "xyz"), `position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). The endpoint returns a 200 OK response with data filtered as if `threshold=critical` were specified.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

The correct implementation should detect the invalid value and return an error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 38 in the diff
- `.unwrap_or(0)` silently converts invalid input to index 0 instead of returning an error
- No `AppError::BadRequest` or similar error variant is used for validation
- The task's Implementation Notes specified using `AppError` for validation errors
