# Criterion 6: Returns 404 for non-existent SBOM IDs

## Verdict: PASS

## Criterion Text
Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved by the PR. The handler still calls `SbomService::new(&db).fetch(sbom_id.id)` early in the function, which returns a 404 error via `AppError` when the SBOM ID does not exist. This call was present before the PR and remains unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

The `?` operator propagates the error, returning it before the threshold filtering logic is reached. The new threshold filtering code is added after the SBOM fetch, so a non-existent SBOM ID still results in a 404 response before any advisory aggregation occurs.

The error handling chain is:
1. `SbomService::fetch()` returns `Err(AppError::NotFound)` for unknown IDs
2. `.context()` wraps the error for debugging
3. `?` propagates the error, short-circuiting the handler
4. `AppError` implements `IntoResponse` and produces a 404 HTTP response

No code in the diff modifies this flow. The new `Query(params)` extraction and filtering logic are positioned after the SBOM fetch, so they cannot interfere with the 404 behavior.

## Evidence
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 30-33 (SBOM fetch)
- The SBOM fetch and 404 error path is unchanged from the pre-PR code
- Threshold filtering code begins at line 41, after the SBOM fetch completes
- The handler signature still returns `Result<Json<AdvisorySummary>, AppError>`
