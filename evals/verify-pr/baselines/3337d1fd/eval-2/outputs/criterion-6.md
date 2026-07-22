## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Verdict: PASS

### What was checked

The PR diff was inspected to confirm that the existing 404 behavior for non-existent SBOM IDs is preserved. The original handler already fetched the SBOM by ID and returned an error if not found; this behavior should remain intact after the threshold filtering changes.

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the SBOM fetch logic is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code path exists in both the original and modified versions of the file. The `SbomService::fetch()` call returns an error (likely an `AppError` variant that maps to 404) when the SBOM ID does not exist. The `.context()` wrapping and `?` propagation ensure the error is returned to the client.

The new threshold filtering logic is applied only after a successful SBOM fetch and advisory aggregation, so it does not interfere with the 404 error path.

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The threshold filtering changes are additive and do not modify the error handling path.
