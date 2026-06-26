# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Result: PASS

## Evidence

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` retains the existing SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... existing error handling ...
```

This code was present before the PR and is not modified by the diff (it appears in the unchanged context lines). The existing pattern in the codebase uses `AppError::NotFound` (from `common/src/error.rs`) for missing resources, which returns a 404 response. Since the PR does not alter the SBOM fetching or error handling path, the existing 404 behavior for non-existent SBOM IDs is preserved.

The PR's changes only affect the post-fetch processing (filtering the aggregated severity counts), leaving the pre-existing 404 behavior intact. PASS.
