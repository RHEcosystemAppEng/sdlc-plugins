# Criterion 6: 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is handled by the `SbomService::fetch()` call, which precedes the new threshold filtering logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    // ... error handling
```

This code was present before the change and remains unchanged in the diff. The `fetch()` method returns an error (mapped to 404 via `AppError`) when the SBOM ID does not exist in the database. Since the threshold filtering logic is added after the SBOM fetch, a non-existent SBOM ID will still trigger a 404 response before any threshold processing occurs.

The diff does not modify the SBOM fetch logic, the error handling chain, or the early return path. The existing 404 behavior is preserved.

## Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **SBOM fetch:** `SbomService::new(&db).fetch(sbom_id.id).await` -- unchanged in the diff
- **Ordering:** SBOM fetch occurs before threshold filtering, so 404 is returned before any new code executes
- **Error handling:** The `.context()` wrapping and `AppError` return type are preserved
