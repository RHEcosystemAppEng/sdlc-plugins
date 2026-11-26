# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: NOT MET**

## Reasoning
For an unrecognized value such as `invalid`, `severity_order.iter().position(...)` returns `None`. `.unwrap_or(0)` then converts that to index 0 without any error, which is the same as `threshold=critical`. The endpoint returns **200 OK** with only the critical count populated, not 400 Bad Request.

The diff never constructs an `AppError` for validation. The implementation notes say to reuse `common/src/error.rs::AppError` and return 400 for invalid threshold values. The threshold is also not parsed into a typed value: the required `Severity` enum was not defined, so typed deserialization could not reject bad input either.

## Evidence
- `get.rs` (added): `.position(|&s| s == threshold.to_lowercase())`
- `get.rs` (added): `.unwrap_or(0);`. This silently falls back to "critical".
- No `AppError::BadRequest` (or any `AppError` construction) anywhere in the diff.
- No test for an invalid threshold returning 400.
