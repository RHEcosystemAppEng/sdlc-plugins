# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved by this PR. The code path that handles SBOM lookup is unchanged.

### Code Under Review

```rust
pub async fn advisory_summary(
    db: DatabaseConnection,
    Path(sbom_id): Path<SbomId>,
    Query(params): Query<SummaryParams>,
) -> Result<Json<AdvisorySummary>, AppError> {
    let sbom = SbomService::new(&db)
        .fetch(sbom_id.id)
        // ... error handling with .context() ...
```

### Detailed Reasoning

The `SbomService::new(&db).fetch(sbom_id.id)` call is the existing code path that looks up an SBOM by its ID. When the SBOM does not exist, this service method returns an error that is converted into a 404 response through the `AppError` error handling chain. The `.context()` wrapper provides a descriptive error message.

The PR adds the `Query(params): Query<SummaryParams>` extractor and the threshold filtering logic, but these changes occur AFTER the SBOM fetch. The SBOM lookup and its error handling are not modified by this PR:

1. The `fetch` call remains unchanged
2. The error propagation via `?` operator remains unchanged
3. The `AppError` conversion (which produces 404 for not-found errors) remains unchanged

Since the PR only adds new code after the existing SBOM fetch, the 404 behavior for non-existent SBOM IDs is preserved.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call is unchanged in the diff
- The error handling chain producing 404 is not modified
- New threshold filtering logic is added after the SBOM fetch, not affecting the lookup behavior
- The repository convention of `Result<T, AppError>` with `.context()` wrapping is maintained
