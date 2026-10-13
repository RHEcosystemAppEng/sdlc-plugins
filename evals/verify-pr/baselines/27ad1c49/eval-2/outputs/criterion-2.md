# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` uses an `Option<String>` for the `threshold` parameter:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`. The filtering logic handles this case correctly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

The `None` branch returns the `summary` unchanged, preserving all severity counts exactly as they were aggregated. This maintains full backward compatibility -- existing clients that do not pass a `threshold` parameter continue to receive the complete advisory summary with all severity levels.

The service layer in `advisory.rs` is also unchanged for the aggregation logic, confirming that the base query behavior is preserved.
