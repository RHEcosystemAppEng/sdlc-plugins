# Criterion 2 — PASS

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

**Analysis:**

The `SummaryParams` struct defines `threshold` as `Option<String>`. In the handler, the `None` branch of the match statement returns the original `summary` unmodified:

```rust
None => summary,
```

This preserves backward compatibility — when no `threshold` parameter is provided, the endpoint returns the full aggregated severity counts as before.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 55
- The `None` arm passes the unmodified `summary` through to `Ok(Json(filtered))`.
- The `SummaryParams.threshold` field is `Option<String>`, so omitting the parameter results in `None`.
