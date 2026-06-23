# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The diff does not validate the threshold parameter value. When an invalid string is provided (e.g., `threshold=invalid`), the code attempts to find it in the `severity_order` array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

Since `"invalid"` is not in `["critical", "high", "medium", "low"]`, `.position()` returns `None`. The `.unwrap_or(0)` then silently falls back to index `0`, which corresponds to `"critical"`. This means an invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task description explicitly states that invalid threshold values should use `common/src/error.rs::AppError` for validation errors and return 400. No such validation exists in the diff. There is no code path that returns an error response for unrecognized threshold values.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `.unwrap_or(0)` on the position lookup silently accepts any string
- No `AppError::BadRequest` or equivalent 400 response anywhere in the diff
- Task implementation notes explicitly mention: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
