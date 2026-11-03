# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: NOT MET (FAIL)**

## Reasoning

An unrecognized threshold value is accepted without any error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=invalid`, `position` returns `None`, and `.unwrap_or(0)` turns that into index 0 (`critical`). The handler then returns **200 OK** with the response filtered as if `threshold=critical` had been sent. `threshold=` (an empty string) is handled the same way.

Nothing in the diff validates the value or returns an error:
- There is no `Severity` enum with a `FromStr`/`Deserialize` impl that could reject unknown values. The Implementation Notes ask for one.
- No `AppError` is built for a bad threshold. The notes say to reuse `common/src/error.rs::AppError` and return 400 for invalid values.
- No `Err(...)` path is added to the handler at all.

## Test coverage
None. The required test "invalid threshold value returns 400" is missing. It would fail against this implementation.
