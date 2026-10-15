# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The code does not validate the threshold query parameter value. When `position()` fails to find a match for an invalid threshold string, the code silently falls back to index 0 via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

This means `?threshold=invalid`, `?threshold=foo`, `?threshold=xyz`, or any other unrecognized value is silently treated as `?threshold=critical` (index 0 in the severity order). No 400 Bad Request is ever returned.

### What was required

The task's implementation notes explicitly state:
> "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The expected behavior is to check whether the threshold value is one of `["critical", "high", "medium", "low"]` and return an `AppError::BadRequest` (or equivalent 400 response) if it is not. The `AppError` enum is available in the module via `use common::error::AppError;` (already imported on line 4).

### Correct implementation pattern

A correct implementation would replace the `unwrap_or(0)` with explicit validation:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest(format!(
        "Invalid threshold value: '{}'. Must be one of: critical, high, medium, low",
        threshold
    )))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 45-46 in the diff
- `unwrap_or(0)` converts any unrecognized threshold to index 0 instead of returning an error
- `AppError` is imported but never used for threshold validation
- No code path returns HTTP 400 for invalid threshold values
