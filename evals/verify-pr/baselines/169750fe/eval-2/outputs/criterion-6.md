# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

## Verdict: PASS

## Analysis

The acceptance criterion requires:
> Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Evidence from the diff

In `modules/fundamental/src/advisory/endpoints/get.rs`, the existing SBOM lookup is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch` method returns an error when the SBOM ID does not exist. The `?` operator propagates this error, which `AppError` converts to a 404 response (following the existing pattern in `common/src/error.rs`). The diff does not modify the SBOM lookup flow — it only adds filtering logic after a successful SBOM fetch.

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The threshold filtering changes occur after the SBOM is successfully fetched, so the error path remains unchanged.
