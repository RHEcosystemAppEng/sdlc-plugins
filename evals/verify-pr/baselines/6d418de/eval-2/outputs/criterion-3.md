## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Reasoning

There is no validation of the threshold value whatsoever. When an unrecognized string (e.g., "invalid", "foo", "xyz") is provided as the threshold parameter, the code path is:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` for any string not in `["critical", "high", "medium", "low"]`, and `.unwrap_or(0)` silently converts this to index 0 (which corresponds to "critical"). The endpoint then returns 200 OK with the filtered data as if `threshold=critical` had been specified.

The task explicitly requires that invalid threshold values return a 400 Bad Request error. To satisfy this criterion, the code should:
1. Check whether the threshold value is a valid severity level
2. If not, return an `AppError` that maps to HTTP 400 (the task notes mention reusing `common/src/error.rs::AppError` for validation errors)

No `AppError` rejection or validation logic exists in the diff. The endpoint silently accepts any arbitrary string as a threshold value.
