# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The existing 404 behavior is preserved in the PR. The endpoint handler contains this logic (unchanged from the original code):

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call returns an error when the SBOM ID does not exist, which is propagated through the `?` operator. Given that the handler returns `Result<Json<AdvisorySummary>, AppError>`, the error will be converted to an appropriate HTTP error response via the `AppError` implementation (which, per the repository conventions, implements `IntoResponse`).

The PR does not modify or remove this existing fetch-and-check pattern. The threshold filtering logic is applied only after the SBOM has been successfully fetched, so non-existent SBOM IDs will continue to produce an error before reaching the filtering code.

While the task also requires a test for this behavior (`tests/api/advisory_summary.rs`), this criterion is specifically about the endpoint behavior, not the test. The behavior itself is preserved.

## Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The PR does not alter the SBOM lookup logic that produces the 404 response.
