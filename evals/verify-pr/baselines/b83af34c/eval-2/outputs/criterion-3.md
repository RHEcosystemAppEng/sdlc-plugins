## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Verdict: FAIL

### Analysis

The acceptance criterion requires that invalid threshold values (values other than "critical", "high", "medium", "low") produce a 400 Bad Request response. The implementation does not validate the threshold value. Instead, it uses `unwrap_or(0)` to silently handle unrecognized values:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided:
1. `position()` returns `None` because "invalid" does not match any entry in `severity_order`
2. `unwrap_or(0)` converts the `None` to index `0` (the "critical" position)
3. The endpoint proceeds with filtering as if `threshold=critical` were specified
4. No error response is returned

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

The correct implementation would check whether `position()` returned `None` and, if so, return an `AppError::BadRequest` (or equivalent 400 error) before proceeding with filtering.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, line 46 in the diff
- **Bug:** `unwrap_or(0)` silently accepts any string as a valid threshold
- **Expected:** Return `Err(AppError::BadRequest("Invalid threshold value"))` or similar for unrecognized values
- **Implementation Notes reference:** "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
