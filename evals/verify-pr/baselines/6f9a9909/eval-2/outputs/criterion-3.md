## Criterion 3

**Text:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**What I checked:** How the code handles threshold values that are not valid severity names (not one of "critical", "high", "medium", "low").

**Code evidence:**

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid`, `severity_order.iter().position(...)` returns `None` because "invalid" does not match any element in the array. The `.unwrap_or(0)` then silently converts this to index `0`, which corresponds to "critical". The request succeeds with a 200 response, treating the invalid input as if `threshold=critical` were specified.

The task explicitly requires that invalid threshold values return a 400 Bad Request response. The implementation notes reference `common/src/error.rs::AppError` for validation errors, but the code never invokes any error path for unrecognized threshold values. The correct implementation should check whether `.position()` returns `None` and, if so, return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent.

**Verdict: FAIL** -- Invalid threshold values are silently accepted and treated as "critical" via `unwrap_or(0)` instead of returning 400 Bad Request. No validation error is raised.
