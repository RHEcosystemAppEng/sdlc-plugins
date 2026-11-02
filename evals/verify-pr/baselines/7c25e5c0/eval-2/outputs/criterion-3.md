# Criterion 3 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

**Analysis:**

The code does not validate the threshold parameter value. When an invalid value is provided (e.g., `threshold=invalid`), the `position()` call returns `None`, and `unwrap_or(0)` silently treats it as index 0 (equivalent to `threshold=critical`):

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

Instead of returning a 400 Bad Request error using `AppError::BadRequest` (as referenced in the Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors"), invalid threshold values are silently accepted and mapped to the "critical" threshold level.

The expected behavior per the acceptance criteria is to return 400 Bad Request for invalid threshold values. The implementation should validate the threshold value and return an error like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 43–45
- `unwrap_or(0)` on line 45 silently accepts any string as the threshold value
- No `AppError::BadRequest` is returned anywhere in the threshold handling logic
- Implementation Notes explicitly reference `common/src/error.rs::AppError` for validation errors
