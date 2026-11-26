# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

## Reasoning

- For an unrecognized value such as `invalid`, `position(...)` returns `None`. `.unwrap_or(0)` then silently maps it to index 0, which is the same as `threshold=critical`.
- The handler returns **200 OK** with only the critical count, plus the wrong unfiltered `total` (see Criterion 1). It does not return 400.
- No `AppError` is constructed or returned for bad input. The Implementation Notes said to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)".
- The parameter is deserialized as a free-form `String`. The Implementation Notes asked for a `Severity` enum, which would let serde/Axum reject unknown values. With a `String`, the `Query` extractor cannot reject invalid input either.
- No test exists. The required "invalid threshold value returns 400" test is missing, and it would fail against this code.

The criterion is not met. Invalid input is silently accepted.
