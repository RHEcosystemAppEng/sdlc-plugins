# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The task requires that the existing 404 behavior for non-existent SBOM IDs be preserved. This is about ensuring the new changes do not break existing error handling.

### What the diff shows

The handler includes existing SBOM fetch logic that is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This existing code path (the `?` operator with `.context()`) propagates the error when an SBOM is not found. The `AppError` type (from `common/src/error.rs`) handles converting not-found errors to 404 responses. The diff does not modify this code path -- the SBOM fetch and error handling remain unchanged.

The threshold filtering logic is added after the SBOM is successfully fetched, so it cannot interfere with the 404 behavior.

### Conclusion

This criterion is satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved because the SBOM fetch code path is not modified by this diff.
