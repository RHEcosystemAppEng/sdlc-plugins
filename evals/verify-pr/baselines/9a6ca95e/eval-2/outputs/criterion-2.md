# Criterion 2

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { ... }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` is returned unmodified. This preserves backward compatibility — all severity counts (critical, high, medium, low) and the total are returned as before.

The `SummaryParams` struct uses `Option<String>` for the threshold field, and the `Query` extractor in Axum will correctly set it to `None` when the query parameter is absent.

## Verdict: PASS

The `None` branch correctly returns the original unmodified summary, preserving backward compatibility.
