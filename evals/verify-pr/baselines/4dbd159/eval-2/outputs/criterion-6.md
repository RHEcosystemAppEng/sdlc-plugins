## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result: PASS**

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the existing SBOM fetch logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call retrieves the SBOM by ID. If the SBOM does not exist, this would return an error that propagates through the `?` operator as an `AppError`. Based on the repository conventions (all handlers return `Result<T, AppError>` with `AppError` implementing `IntoResponse`), a non-existent SBOM ID would result in a 404 response.

The diff does not modify this SBOM lookup logic -- it only adds code after the successful SBOM fetch. The existing 404 behavior for non-existent SBOM IDs is preserved.

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is unchanged by this PR. The SBOM lookup and error handling remain intact.
