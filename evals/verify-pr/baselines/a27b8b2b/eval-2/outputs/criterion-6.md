## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved in the PR. The handler fetches the SBOM before performing any threshold filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await?
    .ok_or(AppError::NotFound(...))?;
```

This pattern uses `.ok_or(AppError::NotFound(...))` to return a 404 response when the SBOM is not found. The PR does not modify this existing code path -- the threshold filtering logic is added after the SBOM fetch, so the 404 behavior is unaffected.

However, while the existing behavior is preserved in the endpoint handler, no integration test was added to verify this behavior (the test file `tests/api/advisory_summary.rs` is entirely absent from the diff). The acceptance criterion specifically asks about "existing behavior preserved," which the code satisfies, but the Test Requirements also call for a 404 test that was not implemented.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The SBOM fetch with `.ok_or(AppError::NotFound(...))` is unchanged
- The threshold filtering logic is added after the SBOM existence check
- No test file was created to verify this behavior
