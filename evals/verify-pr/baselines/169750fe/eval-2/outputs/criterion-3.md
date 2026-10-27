# Criterion 3: Invalid threshold returns 400 Bad Request

## Verdict: FAIL

## Analysis

The acceptance criterion requires:
> `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Evidence from the diff

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is resolved via:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `?threshold=invalid`) is provided:
1. `severity_order.iter().position(...)` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` silently falls back to index 0 (critical)
3. The endpoint returns a 200 OK with filtered results as if `threshold=critical` was specified

### What should happen

The task's Implementation Notes specify:
> Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)

The correct implementation should validate the threshold parameter and return `AppError::BadRequest` when the value is not one of the recognized severity levels. Instead, the code uses `unwrap_or(0)` which silently accepts any string — including typos, numeric values, or gibberish — and treats them as `threshold=critical`.

### Conclusion

Invalid threshold values are silently accepted and treated as "critical" instead of producing a 400 Bad Request error. The endpoint provides no feedback to API consumers that their threshold value was not recognized. This criterion is **not satisfied**.
