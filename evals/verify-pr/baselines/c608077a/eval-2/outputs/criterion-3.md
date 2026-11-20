# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Reasoning

The threshold string is resolved like this:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For an unrecognized value such as `invalid`, `position` returns `None` and `.unwrap_or(0)` turns that into index 0, which means "critical". The request succeeds with **200 OK** and returns only the critical count, zeros for the other severities, and the unfiltered `total`. The diff has no code path that returns an `AppError` validation error.

The Implementation Notes require "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)" and a `Severity` enum implementing `Ord`. Neither was implemented. The diff uses a plain string array instead of the enum, and an invalid value silently falls back to the default.

This fails the criterion directly. It also misleads clients: a typo such as `threshold=hgih` returns plausible-looking but wrong data instead of an error. No test exists for this case either. The required "invalid threshold returns 400" test is missing, and it would fail against this code.

## Evidence
- `get.rs`: `.unwrap_or(0)` on the threshold lookup
- No `AppError` construction or `Err(...)` return in the added lines
- No `Severity` enum anywhere in the diff
