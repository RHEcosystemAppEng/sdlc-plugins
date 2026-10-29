# Criterion 2: No threshold returns all severity counts (backward compatible)

## Criterion
`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

In the diff at `get.rs`, the filtering logic uses a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code returns the unmodified `summary` directly. This preserves the original behavior — all severity counts (critical, high, medium, low) are returned unchanged.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so omitting it from the query string results in `None`. This is the standard Axum/serde deserialization behavior for optional query parameters.

**Evidence:** The `None => summary` arm in the match expression passes through the full aggregated summary without any filtering, maintaining backward compatibility.
