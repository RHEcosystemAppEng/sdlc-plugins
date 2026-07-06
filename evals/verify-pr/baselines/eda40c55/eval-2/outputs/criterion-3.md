## Criterion 3 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

### Reasoning

The code does not validate the threshold parameter value. When an invalid value is provided (e.g., `?threshold=invalid`), the `position()` method returns `None` because "invalid" is not found in the `severity_order` array. Instead of returning a 400 Bad Request error, the code silently falls back to index 0 via `unwrap_or(0)`:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);  // Silent fallback to 0 (critical) for ANY invalid input
```

This means any invalid threshold value (e.g., "invalid", "foo", "123", empty string) is silently treated as `threshold=critical`. The endpoint returns a 200 OK response with filtered data instead of a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation should:

1. Check if the threshold value is a valid severity name
2. If not, return `Err(AppError::BadRequest("Invalid threshold value: ..."))` or equivalent
3. Only proceed with filtering if the threshold is valid

The `AppError` enum is already available in the codebase at `common/src/error.rs` and is imported in the handler (`use common::error::AppError`), so the infrastructure for returning 400 errors exists but is not used for threshold validation.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, diff line containing `.unwrap_or(0)`
- The `AppError` import exists but is not used for threshold validation
- Task Implementation Notes require: "return 400 for invalid threshold values"
- No test exists to verify this behavior (test file `tests/api/advisory_summary.rs` is missing from the diff)
