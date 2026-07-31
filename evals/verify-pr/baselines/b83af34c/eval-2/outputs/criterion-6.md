## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Verdict: PASS

### Analysis

The acceptance criterion requires that the existing 404 behavior for non-existent SBOM IDs is preserved. The diff shows the existing SBOM lookup pattern is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The context lines in the diff show that the SBOM fetch-and-check pattern (which returns `AppError::NotFound` when the SBOM does not exist) remains intact. The PR's changes only add threshold filtering logic after the SBOM lookup succeeds -- they do not modify the error handling path for missing SBOMs.

This existing behavior is preserved by the PR changes.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, context lines in the diff
- **Preservation:** The SBOM lookup and 404 error path are not modified by the PR
- **Note:** While the existing behavior is preserved, no integration test was added to verify this (the task's Test Requirements include testing 404 for non-existent SBOM IDs, but the test file `tests/api/advisory_summary.rs` is missing from the diff entirely)
