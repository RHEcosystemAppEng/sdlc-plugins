# Criterion 2: Without threshold, returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

**Verdict:** PASS

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the no-threshold case in the `None` branch of the match expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None` (since the field is declared as `Option<String>`), and the code returns the unmodified `summary` directly. This preserves the original behavior exactly -- the `summary` variable contains the result of `AdvisoryService::new(&db).aggregate_severities(sbom.id)`, which is the same value that was returned in the original code before this PR.

The `SummaryParams` struct is defined with `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

Axum's `Query` extractor will deserialize missing query parameters as `None` for `Option` fields, so calling the endpoint without `?threshold=...` will correctly set `params.threshold = None`.

The original code path (`Ok(Json(summary))`) is functionally preserved via `Ok(Json(filtered))` where `filtered = summary` in the `None` case.

**Conclusion:** Backward compatibility is maintained. The endpoint without a threshold parameter returns all severity counts as before.
