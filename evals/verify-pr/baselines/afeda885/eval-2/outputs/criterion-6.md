# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The diff shows that the existing SBOM fetch logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code was present before the diff (shown as context lines, not added lines) and remains unchanged. The `SbomService::fetch()` method returns a 404 error (via `AppError`) when the SBOM ID does not exist, following the standard pattern described in the repo conventions.

The diff only adds the threshold filtering logic AFTER the SBOM fetch succeeds. The order of operations is:
1. Fetch SBOM by ID (returns 404 if not found -- existing behavior)
2. Aggregate advisory severities
3. Apply threshold filtering (new code)
4. Return response

Since the SBOM fetch happens before any new code, the 404 behavior for non-existent SBOM IDs is preserved.

## Evidence

- The SBOM fetch code is unchanged (context lines in the diff)
- The new threshold filtering logic is added after the SBOM fetch
- The handler still returns `Result<Json<AdvisorySummary>, AppError>`, preserving the error handling chain
- Existing 404 behavior is not affected by the additions
