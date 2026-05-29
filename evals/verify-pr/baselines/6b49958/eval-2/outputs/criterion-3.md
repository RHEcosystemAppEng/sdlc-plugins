# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Analysis

The PR diff does NOT implement validation for invalid threshold values. When an unrecognized threshold string is provided, the code uses `.unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

If the threshold value does not match any of "critical", "high", "medium", or "low", `position()` returns `None`, and `unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). This means:
- `?threshold=invalid` would silently behave as `?threshold=critical`
- `?threshold=foo` would silently behave as `?threshold=critical`
- No 400 Bad Request error is ever returned

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The code completely ignores this requirement.

The correct implementation should check whether the threshold string is a valid severity value and return an `AppError` (which maps to 400 Bad Request) if it is not. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold: {}", threshold)))?;
```

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 45-46 in the diff
- `.unwrap_or(0)` silently accepts invalid values instead of returning an error
- No `AppError` or 400 response is returned anywhere in the handler for invalid thresholds
- The `common/src/error.rs::AppError` import exists at the top of the file but is never used for threshold validation

**Conclusion:** This criterion FAILS. Invalid threshold values are silently accepted rather than returning 400 Bad Request.
