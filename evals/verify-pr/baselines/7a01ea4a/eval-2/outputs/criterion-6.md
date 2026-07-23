# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The task requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the changes.

### Code Under Review

The handler function fetches the SBOM before any threshold filtering:

```rust
pub async fn advisory_summary(
    db: DatabaseConnection,
    Path(sbom_id): Path<SbomId>,
    Query(params): Query<SummaryParams>,
) -> Result<Json<AdvisorySummary>, AppError> {
    let sbom = SbomService::new(&db)
        .fetch(sbom_id.id)
        .await
        .context("Failed to fetch SBOM")?;
```

### Existing Behavior Preserved

The SBOM lookup happens at lines 28-32 (in the original flow), before the new threshold filtering logic. If the SBOM does not exist, `SbomService::fetch()` will return an error, which propagates through the `?` operator as an `AppError`. Based on the repository conventions (where `AppError` implements `IntoResponse` per `common/src/error.rs`), this would produce a 404 Not Found response.

The PR changes do not modify the SBOM fetch logic. The new threshold filtering code is placed after the SBOM lookup, so it only executes when the SBOM exists. The control flow for non-existent SBOMs is unchanged.

### Note on Testing

While the existing 404 behavior is preserved in the code, the task's Test Requirements specify "Test non-existent SBOM ID returns 404," and no test file was created in this PR. However, this acceptance criterion asks only about the endpoint behavior, not about test coverage. The behavior itself is preserved.

### Conclusion

The 404 response for non-existent SBOM IDs is preserved because the SBOM lookup occurs before the new filtering logic and is unchanged by this PR. This criterion is satisfied.
