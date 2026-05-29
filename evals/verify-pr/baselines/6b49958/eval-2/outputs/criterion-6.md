# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

## Analysis

The PR diff preserves the existing 404 behavior for non-existent SBOM IDs. The handler code still includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This `fetch` call returns an error (via the `?` operator) when the SBOM ID does not exist, which propagates through `AppError` and results in a 404 response. The PR does not modify this existing logic -- the SBOM lookup occurs before the new threshold filtering logic is applied.

The threshold filtering code is added AFTER the SBOM fetch, so the existing 404 path remains intact and unaffected by the changes.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the SBOM fetch and 404 path remain unchanged
- The new threshold filtering code is placed after the SBOM and advisory aggregation, so it cannot interfere with the 404 behavior

**Conclusion:** This criterion PASSES. The existing 404 behavior for non-existent SBOM IDs is preserved.

**Note:** While the existing behavior is preserved, the task also requires integration tests for the 404 case (`Test non-existent SBOM ID returns 404`), and no test file was created at all (see the scope/test analysis for details).
