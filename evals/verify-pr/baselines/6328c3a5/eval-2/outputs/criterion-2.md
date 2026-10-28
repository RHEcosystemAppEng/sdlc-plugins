# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds a `SummaryParams` struct with `threshold: Option<String>`. The filtering logic uses a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the `None` arm returns the original `summary` unchanged. This preserves the pre-existing behavior: all four severity counts (critical, high, medium, low) and the total are returned exactly as they were before the change.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which correctly makes the parameter optional in the query string via Axum's `Query` extractor. Omitting the parameter results in `None` without any deserialization error.

Backward compatibility is maintained.
