# Criterion 3 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Reasoning

The PR does not implement any validation for invalid threshold values. Instead of returning a 400 Bad Request error, invalid values are silently accepted.

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call searches the severity_order array for the provided threshold value. If the value is not found (e.g., "invalid", "foo", "xyz"), `.position()` returns `None`, and `.unwrap_or(0)` converts that to index 0 (which corresponds to "critical").

### Expected behavior

According to the acceptance criteria, an invalid threshold value like `?threshold=invalid` must return HTTP 400 Bad Request. The Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### What is missing

1. No validation check that the threshold value matches one of the valid severity levels ("critical", "high", "medium", "low")
2. No error return path using `AppError` for invalid input
3. No `Severity` enum with parsed validation (as suggested in Implementation Notes)

### Impact

Invalid threshold values like `?threshold=xyz` are silently treated as `threshold=critical`, returning incorrect filtered results without any error indication to the caller. This violates the principle of failing fast on bad input and could lead to confusing behavior for API consumers who misspell a severity level.

### Correct implementation pattern

The implementation should check whether the threshold value is valid before proceeding, for example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```
