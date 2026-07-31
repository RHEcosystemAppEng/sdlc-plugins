## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Verdict: PASS

### Analysis

The `threshold` parameter is defined as `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no threshold query parameter is provided, `params.threshold` is `None`. The match expression handles this case:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

The `None` branch returns the `summary` value unchanged, which is the full aggregated severity counts from `AdvisoryService::aggregate_severities()`. This preserves backward compatibility -- callers that do not supply a `threshold` parameter receive the same response as before this change.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Code path:** `None => summary` returns unmodified aggregation result
- **Backward compatibility:** Preserved -- existing API callers without the threshold parameter are unaffected
