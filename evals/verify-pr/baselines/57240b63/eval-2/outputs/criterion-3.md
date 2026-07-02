# Acceptance Criterion 3

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result**: FAIL

## Evidence

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses `unwrap_or(0)` when looking up the threshold value in the severity ordering:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `position()` returns `None` because "invalid" is not found in `["critical", "high", "medium", "low"]`. The `unwrap_or(0)` then silently converts this to index 0, which corresponds to "critical". This means:

- `?threshold=invalid` is silently treated as `?threshold=critical`
- No 400 Bad Request error is returned
- No validation error is raised
- The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The correct implementation should validate the threshold value and return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent when the value is not one of the recognized severity levels.

**Verdict**: FAIL -- invalid threshold values are silently accepted and treated as "critical" instead of returning 400 Bad Request.
