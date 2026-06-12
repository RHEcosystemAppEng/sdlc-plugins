## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Verdict: PASS

### Analysis

The PR diff adds the `SummaryParams` struct with `threshold` as `Option<String>`. In the handler, the filtering logic is wrapped in a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` parameter is provided, `params.threshold` is `None`, and the handler falls through to the `None` arm, which returns the original `summary` unmodified. This preserves backward compatibility -- the endpoint returns all severity counts exactly as before when no threshold is specified.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so when the query parameter is absent, Axum's `Query` extractor will deserialize it as `None`.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` branch of the match returns the unmodified `summary`
- `Option<String>` correctly makes the parameter optional
