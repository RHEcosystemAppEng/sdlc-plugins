## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `threshold` parameter is declared as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no threshold query parameter is provided, `params.threshold` is `None`. The match arm for `None` returns the summary unmodified:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

This means that when the endpoint is called without a `threshold` parameter, the original `summary` from `AdvisoryService::aggregate_severities()` is returned as-is, preserving all severity counts. The existing behavior is maintained -- backward compatibility is preserved.

### Conclusion

The `None` branch correctly passes through the unmodified summary, maintaining backward compatibility when no threshold is specified.
