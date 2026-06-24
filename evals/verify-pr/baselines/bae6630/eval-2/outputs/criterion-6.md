## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Result: PASS

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the existing SBOM fetch logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code fetches the SBOM by ID. If the SBOM does not exist, `SbomService::fetch()` presumably returns an error (likely `AppError::NotFound`), which is propagated via the `?` operator. The `.context()` call wraps the error with additional context but preserves the error type.

The PR diff does not modify this fetch logic -- it remains identical to the original implementation. The only changes are the addition of query parameter extraction and the filtering logic that occurs *after* the SBOM is successfully fetched.

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The PR does not alter the SBOM fetch or error handling path.
