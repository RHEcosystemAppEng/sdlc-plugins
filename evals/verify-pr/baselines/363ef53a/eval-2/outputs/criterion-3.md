# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The PR does NOT implement validation for invalid threshold values. When an invalid threshold string is provided (e.g., `?threshold=invalid`), the code uses `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` method returns `None` when the threshold string does not match any entry in the `severity_order` array. Instead of returning a 400 Bad Request error, the code silently falls back to index `0`, which corresponds to "critical". This means:

- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=foobar` silently behaves as `?threshold=critical`
- `?threshold=` silently behaves as `?threshold=critical`

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The PR ignores this requirement entirely.

## What should have been implemented

The code should validate the threshold value and return an `AppError` (which maps to 400 Bad Request) for unrecognized values. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 46 of the diff
- `.unwrap_or(0)` silently accepts any input string without validation
- No `AppError::BadRequest` or 400 response anywhere in the diff
- No use of `common/src/error.rs::AppError` for validation despite the implementation notes requiring it
- The task explicitly requires 400 Bad Request for invalid threshold values in both the Acceptance Criteria and the Implementation Notes
