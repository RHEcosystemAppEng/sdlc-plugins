# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The PR does not validate the threshold parameter value. Invalid values are silently accepted and treated as if the threshold were "critical" (the highest severity).

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Analysis

When `threshold` is set to an invalid value (e.g., `"invalid"`, `"foo"`, `"none"`), the `.position()` call returns `None` because no element in `severity_order` matches the input. The `.unwrap_or(0)` then defaults to index 0 ("critical"), causing the endpoint to silently apply the "critical" threshold filter.

The endpoint returns HTTP 200 with filtered results instead of HTTP 400 Bad Request. There is no error path for invalid threshold values anywhere in the diff.

### What Should Have Been Implemented

Per the task's Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The code should validate the threshold against the valid severity values and return an `AppError` (which implements `IntoResponse` per the repository conventions) to produce a 400 Bad Request response when the value is invalid.

For example:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```
