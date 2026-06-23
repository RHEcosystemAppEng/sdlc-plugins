# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing SBOM fetch logic is preserved in the diff. The handler still calls:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This code path is unchanged from the original. The fetch presumably returns an error (mapped to 404 via `AppError`) when the SBOM ID does not exist, and the `?` operator propagates this error before the threshold filtering logic is reached.

The new threshold filtering code is added after the SBOM fetch succeeds, so it does not interfere with the 404 behavior. The overall error handling flow for non-existent SBOM IDs remains intact.

While no test was added to verify this behavior (the test file is missing entirely), the existing code path is demonstrably preserved by the diff.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call and its error propagation are unchanged
- The new threshold filtering logic appears only after the successful SBOM fetch
- No changes to the error handling chain for the fetch operation
