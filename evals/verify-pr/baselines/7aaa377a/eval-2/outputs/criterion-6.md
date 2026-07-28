# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved by the diff. The code that fetches the SBOM by ID and returns a 404 error when not found is untouched by the changes.

## Evidence

From the diff in `modules/fundamental/src/advisory/endpoints/get.rs`, the SBOM fetch logic remains unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

The context lines show this existing code is preserved. The `SbomService::fetch()` method returns a `Result` that produces an `AppError` (which maps to 404) when the SBOM ID does not exist. The new threshold filtering logic is added after the SBOM fetch, so it only executes when the SBOM exists.

The diff adds the threshold parameter and filtering logic downstream of the SBOM lookup, without altering the error path for non-existent SBOMs. The `.ok_or` or error-returning pattern on the fetch result (visible from the unchanged context) continues to produce 404 responses for missing SBOMs.

## Conclusion

This criterion is satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved. The new code is added downstream of the SBOM existence check and does not interfere with the error path.
