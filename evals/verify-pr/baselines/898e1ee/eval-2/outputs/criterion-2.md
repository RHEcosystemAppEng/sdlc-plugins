# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

When no `threshold` query parameter is provided, the `params.threshold` field is `None`. The match expression handles this case:

```rust
None => summary,
```

This returns the unmodified `summary` object from `AdvisoryService::aggregate_severities()`, which contains all four severity counts (critical, high, medium, low) and the total. This is identical to the previous behavior before the threshold feature was added.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which correctly makes it optional in the query string deserialization. Axum's `Query` extractor will set `threshold` to `None` when the parameter is absent.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` arm of the match expression returns the unmodified summary
- The original handler returned `Ok(Json(summary))`; the new handler returns `Ok(Json(filtered))` where `filtered` equals `summary` when no threshold is provided
- Backward compatibility is preserved
