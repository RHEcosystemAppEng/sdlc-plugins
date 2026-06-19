# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

When no `threshold` query parameter is provided, the `params.threshold` field is `None` (since it is typed as `Option<String>` in the `SummaryParams` struct). The match expression handles this case with the `None` branch:

```rust
None => summary,
```

This returns the original `summary` object unchanged, preserving the existing behavior where all four severity counts (critical, high, medium, low) and the total are returned as-is from the `AdvisoryService::aggregate_severities()` call.

The existing SBOM fetch and aggregation logic is untouched:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
let summary = AdvisoryService::new(&db)
    .aggregate_severities(sbom.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This confirms backward compatibility is preserved for the no-threshold case.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch in the match expression returns the unmodified aggregation result
- The `SummaryParams.threshold` is `Option<String>`, so absent query parameters yield `None`
- No changes to the service layer or aggregation logic affect the default behavior
