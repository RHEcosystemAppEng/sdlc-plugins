# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

**Verdict:** PASS

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing SBOM lookup logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the PR changes (it appears in the unchanged context lines of the diff) and remains intact. The `SbomService::fetch()` method returns a `Result`, and if the SBOM ID does not exist, it would return an error that gets propagated via the `?` operator. Given the repository's error handling convention (all handlers return `Result<T, AppError>` with `.context()` wrapping), a non-existent SBOM ID would result in an `AppError` that maps to a 404 response.

The PR does not modify, remove, or bypass this lookup. The new threshold filtering logic is added **after** the SBOM fetch, meaning the 404 path is still exercised before any threshold processing occurs.

**Note regarding tests:** While the existing behavior is preserved in the code, the task's "Files to Create" section specifies `tests/api/advisory_summary.rs` for integration tests, which should include a test for non-existent SBOM IDs returning 404. This test file is entirely absent from the PR diff. However, this criterion is about the endpoint behavior being preserved, not about test coverage. The behavior itself appears intact.

**Conclusion:** The 404 behavior for non-existent SBOM IDs is preserved. The SBOM existence check precedes the new filtering logic and remains unchanged.
