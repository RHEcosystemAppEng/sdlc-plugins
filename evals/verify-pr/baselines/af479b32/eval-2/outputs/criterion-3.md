# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The code does not validate the threshold parameter value. Instead of returning a 400 Bad Request error for invalid threshold values, it silently accepts them and defaults to index 0 (critical).

### Code Analysis

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is provided:
1. `threshold.to_lowercase()` produces `"invalid"`
2. `.position(|&s| s == "invalid")` searches `["critical", "high", "medium", "low"]` and finds no match, returning `None`
3. `.unwrap_or(0)` converts the `None` to `0` (the index for "critical")

The result is that an invalid threshold value is silently treated as `threshold=critical`. No error is returned to the client.

### Expected Behavior

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation should:
1. Check if the threshold value matches one of the valid severities
2. If not, return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent
3. Only proceed with filtering if the value is valid

### Missing Code

There is no validation logic anywhere in the diff. No `AppError::BadRequest` is used. No 400 status code path exists for invalid input.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- `.unwrap_or(0)` on the position lookup silently converts invalid input to index 0
- No use of `AppError` for validation anywhere in the filtering logic
- The task's Implementation Notes require using `common/src/error.rs::AppError` for validation errors, but this is not done
