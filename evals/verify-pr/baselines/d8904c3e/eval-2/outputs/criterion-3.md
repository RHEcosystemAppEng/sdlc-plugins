# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles threshold lookup with:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` call searches for the threshold value in the `severity_order` array. When the threshold is "invalid" (or any string not in `["critical", "high", "medium", "low"]`), `position()` returns `None`. The code then uses `unwrap_or(0)` to silently default to index 0 ("critical").

This means an invalid threshold like `?threshold=invalid` or `?threshold=foobar` is silently treated as `?threshold=critical` instead of returning a 400 Bad Request error. The user receives a 200 OK response with filtered data, never knowing their input was invalid.

## What is missing

The implementation should validate the threshold value and return a 400 Bad Request when it does not match a valid severity. The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

A correct implementation would look something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```

Instead, `unwrap_or(0)` silently swallows the validation error, violating the acceptance criterion.

## Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Line:** `.unwrap_or(0)` on the `position()` call
- **Expected behavior:** Return `400 Bad Request` with an error message for unrecognized threshold values
- **Actual behavior:** Silently defaults to index 0, treating invalid input as "critical"
