## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Analysis

This criterion requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the threshold filtering changes.

### Code Inspection

The SBOM lookup logic in `modules/fundamental/src/advisory/endpoints/get.rs` remains unchanged in the diff:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... existing error handling ...
```

The context lines in the diff show that the existing `SbomService::fetch()` call and its error handling chain are preserved. The SBOM lookup occurs before any threshold filtering logic, so non-existent SBOM IDs continue to produce a 404 response through the existing `AppError::NotFound` pattern before the threshold filtering code is reached.

The new threshold filtering logic is added after the SBOM is successfully fetched and after the advisory severity aggregation, so it cannot interfere with the 404 behavior.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **SBOM fetch:** Unchanged context lines show the existing `SbomService::new(&db).fetch(sbom_id.id)` pattern is preserved
- **Error handling:** The `.ok_or(AppError::NotFound(...))` or equivalent error propagation chain remains intact
- **Execution order:** SBOM lookup precedes threshold filtering, so 404 is returned before filtering logic is reached
