# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The `None` branch of the match expression in `modules/fundamental/src/advisory/endpoints/get.rs` correctly returns the unmodified `summary` object:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` (containing all severity counts: critical, high, medium, low, and total) is returned unchanged.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` arm of the match returns `summary` directly without modification
- The `SummaryParams` struct defines `threshold` as `Option<String>`, so absence of the query parameter correctly maps to `None`
- Backward compatibility is preserved -- existing clients that do not pass `?threshold=` will receive the same response as before this change
