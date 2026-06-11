## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Reasoning

When `params.threshold` is `None`, the code falls through to the `None => summary` branch in the match expression, returning the unmodified `summary` object directly. This preserves the original behavior of the endpoint -- no filtering is applied and all severity counts (critical, high, medium, low) are returned as they were before this change.

The relevant code path:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,  // Returns unmodified summary
};
Ok(Json(filtered))
```

The `SummaryParams` struct uses `Option<String>` for the threshold field, which means Axum's query deserialization will parse the absence of the `threshold` parameter as `None`. This is the standard pattern for optional query parameters in Axum and correctly preserves backward compatibility.
