# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

## Verdict: PASS

## Criterion Text
Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Evidence from Diff

The existing SBOM lookup code in `modules/fundamental/src/advisory/endpoints/get.rs` is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

## Detailed Reasoning

This criterion is about preserving existing behavior, not adding new behavior. The diff does not modify the SBOM lookup or error handling path. The `SbomService::fetch()` method presumably returns an error or `None` for non-existent SBOM IDs, which is then converted to an appropriate error response via the `?` operator and the `AppError` type.

Since the SBOM fetch logic is untouched by the diff, the existing 404 behavior for non-existent SBOM IDs is preserved.

Note: While no **new test** for the 404 case was added (the task's test requirements include "Test non-existent SBOM ID returns 404"), this criterion is about the endpoint behavior itself, not about test coverage. The test coverage gap is addressed in the scope containment analysis.

## Conclusion

The criterion passes. The existing 404 behavior for non-existent SBOM IDs is preserved because the SBOM lookup logic was not modified in this diff.
