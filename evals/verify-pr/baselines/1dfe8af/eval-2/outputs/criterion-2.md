# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## Evidence

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` includes a match on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None` (since it is declared as `Option<String>` in the `SummaryParams` struct). The `None` branch returns the original `summary` unchanged, which contains all four severity counts (critical, high, medium, low) plus total.

The `SummaryParams` struct uses `Option<String>` for threshold, so omitting the parameter is valid and does not cause a deserialization error. The existing aggregation logic in `advisory.rs` is untouched and continues to produce all counts.

This preserves full backward compatibility with the existing endpoint behavior.
