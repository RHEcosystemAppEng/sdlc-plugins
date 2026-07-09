## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Requirement

Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

### Analysis

The handler's SBOM lookup logic is unchanged in the diff:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... (existing error handling with .ok_or or .context pattern)
```

The diff shows only additions around the threshold filtering logic. The SBOM fetch and 404 handling code is part of the existing (unchanged) handler lines visible as context in the diff. The `SbomService::fetch` call and its error handling using `AppError` patterns remain intact.

The `AppError` enum (in `common/src/error.rs`) includes a `NotFound` variant that maps to HTTP 404, as described in the repo conventions. Since the SBOM lookup code is not modified, the 404 behavior for non-existent SBOM IDs is preserved.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 31-33 in the diff context -- SBOM fetch logic is unchanged
- The existing `SbomService::new(&db).fetch(sbom_id.id)` pattern with error handling is not altered
- `common/src/error.rs::AppError` provides the `NotFound` variant used for 404 responses
- No changes affect the SBOM lookup or error handling path

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The criterion is satisfied.
