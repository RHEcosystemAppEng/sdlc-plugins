# Criterion 3 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## What was checked
- How `params.threshold` is handled in `modules/fundamental/src/advisory/endpoints/get.rs`.
- Whether `AppError` (`common/src/error.rs`) is used to raise a validation error, as the Implementation Notes require.

## What was found
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```
- For an unknown value such as `invalid`, `.position(...)` returns `None`, and `.unwrap_or(0)` quietly turns that into index 0 (`critical`). Nothing is validated and no `AppError` is returned. The request continues and the handler returns **200 OK** with a summary body.
- Because the filter comparisons are inverted (see criterion 1), index 0 means no filtering at all. An invalid threshold therefore gives the same response as having no threshold, and the caller gets no sign that the input was rejected.
- The task asked for a `Severity` enum. One would naturally reject unknown values when deserializing (for example `Option<Severity>` with serde), which would give a 400. No such enum was added; `threshold` stays a free-form `Option<String>`.
- No test for the invalid case was added (Test Requirement "Test invalid threshold value returns 400" is not met).

## Conclusion
Invalid threshold values are accepted and return 200 instead of 400 Bad Request.

**Verdict: FAIL**
