# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

In the diff for `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct defines `threshold` as `Option<String>`. The match expression handles the `None` case explicitly:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code returns the unmodified `summary` directly. This preserves the original behavior -- all severity counts (critical, high, medium, low) are returned as-is.

The `advisory.rs` service file shows no functional changes in the diff, meaning the `aggregate_severities` method continues to return all counts as before.

## Evidence

- `Option<String>` makes the parameter optional -- requests without `?threshold=...` will have `None`
- The `None => summary` branch returns the full, unfiltered summary
- No changes to the underlying service query in `advisory.rs`
- Backward compatibility is preserved
