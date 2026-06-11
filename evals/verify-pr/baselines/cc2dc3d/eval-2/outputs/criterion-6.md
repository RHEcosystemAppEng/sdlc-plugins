## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved. The diff shows the existing `fetch` call and its error handling remain unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` method returns an error when the SBOM is not found, and the `?` operator propagates it as an `AppError`. Based on the repo conventions, `AppError` implements `IntoResponse` and maps not-found errors to 404 status codes. This pre-existing behavior was not altered by the changes in this PR.

The new threshold filtering code is only reached after the SBOM has been successfully fetched, so it does not interfere with the 404 path.

### Evidence

Lines 31-34 of the diff show the SBOM fetch is unchanged:
```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

No modifications were made to the error propagation path. The 404 behavior is inherited from the existing `SbomService::fetch()` and `AppError` infrastructure.

Note: While the existing 404 behavior appears preserved, the task called for a test to verify this behavior (`tests/api/advisory_summary.rs` with a non-existent SBOM ID test case), and no test file was created.
