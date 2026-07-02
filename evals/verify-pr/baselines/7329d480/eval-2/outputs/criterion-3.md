# Criterion 3: Invalid threshold returns 400 Bad Request

## Result: FAIL

## Criterion Text
`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Analysis

The code looks up the threshold value in the severity ordering array and uses `.unwrap_or(0)` for the fallback:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `.position()` returns `None` because "invalid" is not found in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then maps this to index 0, silently treating the invalid value as if it were "critical".

### Expected Behavior

The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation should detect the unrecognized threshold string and return an `AppError` that maps to HTTP 400 Bad Request.

### What Should Happen

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold: {}", threshold)))?;
```

### What Actually Happens

Invalid values are silently accepted and treated as "critical" (index 0). No 400 error is returned. The caller receives a 200 response with (incorrectly) filtered data instead of an error.

## Verdict

FAIL -- The code uses `.unwrap_or(0)` instead of returning a 400 Bad Request error for invalid threshold values. This violates both the acceptance criterion and the implementation notes.
