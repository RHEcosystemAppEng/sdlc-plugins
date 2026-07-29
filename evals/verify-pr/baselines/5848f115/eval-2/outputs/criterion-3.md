# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The implementation does not validate the `threshold` query parameter value. When an invalid threshold string is provided (e.g., `?threshold=banana`), the code silently accepts it instead of returning a 400 Bad Request error.

### How invalid values are handled

The code uses `.position()` to find the threshold string in the severity array, and falls back to `.unwrap_or(0)` when the value is not found:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold` is an invalid value like "banana":
1. `.position()` returns `None` (no match in the array)
2. `.unwrap_or(0)` converts `None` to `0`
3. The code proceeds as if `threshold=critical` was passed (index 0)
4. No error is returned to the client

### What should happen

The task description specifies: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation should:
1. Attempt to match the threshold value against valid severities
2. If no match is found, return `Err(AppError::BadRequest(...))` or equivalent 400 response
3. Only proceed with filtering if the threshold value is valid

### Impact

Any arbitrary string passed as the `threshold` parameter is silently treated as "critical", which could confuse API consumers who misspell a valid threshold value or pass unexpected input. They would receive a valid-looking response with no indication that their input was invalid.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, the `unwrap_or(0)` call
- The task explicitly requires using `common/src/error.rs::AppError` for validation errors
- No `Err(...)` return exists anywhere in the threshold handling code path
