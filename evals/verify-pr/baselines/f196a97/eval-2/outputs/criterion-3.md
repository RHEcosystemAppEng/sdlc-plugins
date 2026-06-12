## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Verdict: FAIL

### Analysis

The task requires that invalid threshold values (e.g., `?threshold=invalid`) return a 400 Bad Request error. The implementation notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

Examining the PR diff's filtering logic:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., "invalid"), `position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). This means:

1. The endpoint does NOT return a 400 error for invalid threshold values.
2. Instead, it silently treats any invalid value as `threshold=critical`, which is incorrect and potentially misleading behavior.
3. There is no validation step that checks whether the provided threshold string matches one of the valid severity levels.

The correct implementation should:
- Validate the threshold string against the valid values ("critical", "high", "medium", "low")
- Return `AppError::BadRequest` (or equivalent 400 response) if the value is not recognized
- The task explicitly mentions using `common/src/error.rs::AppError` for this purpose

No validation or error handling code exists anywhere in the diff for invalid threshold values.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- `.unwrap_or(0)` on the position lookup silently accepts invalid input
- No `AppError` or 400 response is returned for invalid threshold values
- The task's Implementation Notes explicitly require using `AppError` for validation errors
