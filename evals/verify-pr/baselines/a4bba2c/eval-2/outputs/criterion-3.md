# Criterion 3: Invalid threshold returns 400 Bad Request

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The implementation does NOT return a 400 Bad Request for invalid threshold values. Instead, it silently accepts any string and falls back to index 0 (critical) when the value is not found in the severity_order array.

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like `"invalid"` is provided:
1. `.position(...)` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` converts `None` to `0`
3. The function proceeds with `threshold_idx = 0`, effectively treating the invalid input as `threshold=critical`

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The implementation ignores this guidance entirely.

The correct implementation should validate the threshold value and return an error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

## Evidence

- `unwrap_or(0)` on line 46 of the diff silently converts invalid input to index 0
- No `AppError::BadRequest` or any 400 response is generated for invalid values
- The `common::error::AppError` import exists at the top of the file but is never used for threshold validation
- The task's Implementation Notes specifically require using `AppError` for validation errors
