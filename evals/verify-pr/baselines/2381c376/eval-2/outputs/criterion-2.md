## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Analysis

The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`. The match expression handles this case by returning the unmodified summary:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

The `None` arm passes the original `summary` through without modification, preserving all severity counts (critical, high, medium, low, total). This maintains full backward compatibility with the existing behavior.

### Evidence

The `None => summary` arm in the match expression in `get.rs` ensures the original response is returned unchanged when no threshold parameter is specified.
