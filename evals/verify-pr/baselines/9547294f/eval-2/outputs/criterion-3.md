# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task explicitly requires that invalid threshold values return a 400 Bad Request response. The implementation notes state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

However, the code uses `unwrap_or(0)` to silently handle invalid threshold values:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., "invalid", "foo", "extreme") is provided:

1. `severity_order.iter().position(|&s| s == "invalid")` returns `None` because "invalid" is not in the array `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` converts `None` to index `0`
3. The code proceeds as if `threshold=critical` was specified
4. No error is returned to the client

## Expected Behavior

The code should validate the threshold parameter and return a 400 Bad Request error using the existing `AppError` infrastructure. The correct implementation would look something like:

```rust
Some(threshold) => {
    let severity_order = ["critical", "high", "medium", "low"];
    let threshold_idx = severity_order.iter()
        .position(|&s| s == threshold.to_lowercase())
        .ok_or(AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
    // ... filtering ...
}
```

## Evidence

- Line in diff: `.unwrap_or(0)` -- silently converts invalid input to index 0
- No `AppError::BadRequest` or similar error return anywhere in the threshold handling code
- The task's Implementation Notes explicitly say: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
- The `AppError` type is imported (`use common::error::AppError;`) but never used for threshold validation

## Verdict Rationale

This criterion is clearly not satisfied. Invalid threshold values are silently accepted and treated as "critical" due to `unwrap_or(0)`, instead of returning HTTP 400 as required by the acceptance criteria.
