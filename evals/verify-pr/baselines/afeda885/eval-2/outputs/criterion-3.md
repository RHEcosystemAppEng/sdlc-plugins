# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task's acceptance criteria explicitly require that an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request response. The implementation notes reinforce this: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

However, the diff does NOT implement this validation. The relevant code is:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` call searches for the threshold string in the severity order array `["critical", "high", "medium", "low"]`. When the threshold value is not found (e.g., "invalid"), `position()` returns `None`. Instead of returning a 400 error, the code calls `.unwrap_or(0)`, which silently maps ANY invalid threshold value to index 0 (the "critical" position).

## Evidence

- **Expected behavior:** `?threshold=invalid` should return HTTP 400 Bad Request
- **Actual behavior:** `?threshold=invalid` silently maps to `threshold_idx = 0`, treating the invalid value as if it were "critical"
- **Missing code:** No validation check, no `AppError::BadRequest` return, no use of `common/src/error.rs::AppError` for input validation
- The `unwrap_or(0)` pattern suppresses the error case entirely

## What Should Be Implemented

The code should check whether `position()` returns `None` and return an `AppError` that maps to HTTP 400:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```
