# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The handler function includes a `None` branch for the optional `threshold` parameter:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When the `threshold` query parameter is not provided, `params.threshold` is `None`, and the code returns the original `summary` object unchanged. This preserves the existing response shape and includes all severity counts (critical, high, medium, low, and total).

The `SummaryParams` struct correctly defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

Axum's `Query` extractor will deserialize missing query parameters as `None` for `Option` fields, so requests without `?threshold=...` will correctly fall through to the `None` branch.

### Conclusion

Backward compatibility is preserved. Existing callers that do not supply the `threshold` parameter will receive the same response as before the change. This criterion is satisfied.
