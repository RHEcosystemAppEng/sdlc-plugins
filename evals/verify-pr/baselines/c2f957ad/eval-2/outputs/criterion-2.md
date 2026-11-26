# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
...
Query(params): Query<SummaryParams>,
...
let filtered = match &params.threshold {
    Some(threshold) => { ... }
    None => summary,
};
Ok(Json(filtered))
```

## Reasoning

- `threshold` is an `Option<String>`. When the query string is missing, Axum's `Query` extractor deserializes it to `None` without error, so existing clients that send no parameters are not rejected.
- The `None` branch returns the original aggregated `AdvisorySummary` unchanged. The response has the same fields and values as before the PR.
- Caveat: there is no test for this. The "no threshold returns all four severity counts" test is missing because `tests/api/advisory_summary.rs` was not created. The code path itself is correct.

The criterion is met at the code level.
