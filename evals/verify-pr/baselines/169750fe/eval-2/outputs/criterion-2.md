# Criterion 2: Without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The acceptance criterion requires:
> `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Evidence from the diff

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `threshold` parameter is declared as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The handler matches on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original unfiltered `summary` is returned directly. This preserves backward compatibility — the response shape and content are identical to the pre-change behavior.

### Conclusion

The `None` branch returns the complete, unfiltered `AdvisorySummary` with all severity counts. Backward compatibility is preserved.
