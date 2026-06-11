## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Analysis

The implementation does NOT validate the threshold parameter value. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the code silently accepts it via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` fails to find a match for an invalid value like "invalid", it returns `None`. The `.unwrap_or(0)` then defaults to index 0 (which corresponds to "critical"). This means:

- An invalid threshold value is silently treated as `threshold=critical`
- No 400 Bad Request error is returned
- The caller receives no indication that their input was invalid

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". This instruction was not followed.

The correct implementation should return an `AppError` (which implements `IntoResponse` and maps to a 400 status) when the threshold value is not one of the valid severity levels.

### Evidence

Lines 44-46 of the diff in `get.rs`:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);  // <-- silently defaults instead of returning 400
```

There is no `Err(AppError::...)` return path anywhere in the threshold handling code, and `common::error::AppError` is imported but never used for validation.
