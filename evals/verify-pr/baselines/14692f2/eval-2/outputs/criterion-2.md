# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The diff implements backward compatibility through the `Option<String>` type on the `threshold` field in `SummaryParams`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, the `None` case falls through to returning the unfiltered summary:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` will be `None`, and the original `summary` (containing all severity counts: critical, high, medium, low, and total) is returned unchanged.

This preserves full backward compatibility -- existing callers that do not pass a `threshold` parameter will receive the same response as before. The `Query(params): Query<SummaryParams>` extractor in Axum will accept requests without any query parameters, defaulting `threshold` to `None`.

### Conclusion

This criterion is satisfied. The endpoint without a threshold parameter returns all severity counts unchanged.
