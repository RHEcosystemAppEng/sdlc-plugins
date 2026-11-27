# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: MET (PASS)**

## Evidence (get.rs)

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
...
    Query(params): Query<SummaryParams>,
...
    None => summary,
```

## Reasoning

- `threshold` is `Option<String>`, so `Query<SummaryParams>` accepts requests with no query string.
- With no threshold, the `None` arm returns the original aggregated `summary` unchanged, including all four severity counts and the original `total`.
- The response struct shape is unchanged, so existing clients are unaffected.

Caveat: no test was added for this case ("Test no threshold returns all four severity counts" is missing). Once AC5 is fixed, the response shape changes by gaining `threshold_applied`. That is additive and should stay backward compatible.
