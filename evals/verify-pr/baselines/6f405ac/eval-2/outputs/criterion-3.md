# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The acceptance criterion requires that an invalid threshold value (e.g., `?threshold=invalid`, `?threshold=foobar`) must return a 400 Bad Request error response. The implementation does not satisfy this requirement.

When an invalid threshold string is provided, the code executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call searches for the provided string in the `severity_order` array `["critical", "high", "medium", "low"]`. When the string is not found (e.g., "invalid", "foobar", "xyz"), `.position()` returns `None`. The `.unwrap_or(0)` then silently converts `None` to index `0`, which corresponds to "critical".

This means **any invalid threshold value is silently treated as `threshold=critical`** rather than returning a 400 Bad Request error. This is a significant correctness and usability bug:

1. Users providing typos (e.g., `?threshold=hgih`) get silently incorrect filtering behavior
2. The API provides no feedback that the input was invalid
3. The behavior contradicts both the acceptance criterion and the implementation notes, which explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The correct implementation should validate the input and return an error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: '{}'. Valid values are: critical, high, medium, low", threshold)))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line containing `.unwrap_or(0)`
- The `unwrap_or(0)` silently accepts any string input without validation
- No `AppError::BadRequest` or any error variant is used in the threshold handling code
- The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
- The `common/src/error.rs` module is imported (`use common::error::AppError;`) but not used for threshold validation
