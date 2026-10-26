# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The code does not validate the threshold parameter against known severity values. When an invalid threshold value is provided, the code silently falls back to index 0 via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

If `threshold=invalid`, `position()` returns `None`, and `unwrap_or(0)` treats it as if `threshold=critical` was specified (index 0). No `400 Bad Request` error is returned.

The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation should check whether `position()` returns `None` and, if so, return an `AppError::BadRequest` (or equivalent 400 variant) instead of silently defaulting.

This is a correctness bug: invalid input is accepted and produces a misleading response rather than a clear validation error.
