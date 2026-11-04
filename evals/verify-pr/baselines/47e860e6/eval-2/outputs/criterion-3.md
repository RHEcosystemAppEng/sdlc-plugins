# Criterion 3 — FAIL

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## What was checked
How the handler parses the threshold value, and whether it returns `AppError` anywhere on the threshold path.

## What was found
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```
An unknown value such as `invalid` makes `position` return `None`. `.unwrap_or(0)` then silently replaces it with index 0, which is treated as `critical`. The request goes on to return `200 OK` with a body. Nothing on this path returns an error.

The Implementation Notes asked to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)" and to define a `Severity` enum. Neither was done. `threshold` stays a free-form `String` with no validation, either by serde enum deserialization (which would reject bad values through the `Query` extractor) or by an explicit `AppError` bad-request variant.

No test for the invalid-threshold case was added.

**Verdict: FAIL.** Invalid threshold values are accepted and return 200, not 400.
