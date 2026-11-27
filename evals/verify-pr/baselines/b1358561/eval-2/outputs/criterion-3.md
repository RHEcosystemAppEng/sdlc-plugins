# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: NOT MET (FAIL)**

## Evidence (get.rs)

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

## Reasoning

- `.position(...)` returns `None` for an unrecognised value such as `invalid`, or for an empty `threshold=`.
- `.unwrap_or(0)` silently turns that into index 0 (`critical`) instead of rejecting the request.
- The handler goes on and returns `200 OK`. Because of the inverted comparison (see Criterion 1), the response contains all counts unfiltered.
- No `AppError` bad-request variant is produced anywhere in the diff. The Implementation Notes required reusing `common/src/error.rs::AppError` to return 400.
- The required test ("Test invalid threshold value returns 400") is missing.

## Expected fix

Parse the parameter into a `Severity` enum, for example with `FromStr` or serde deserialization, and map a parse failure to a 400 `AppError`.
