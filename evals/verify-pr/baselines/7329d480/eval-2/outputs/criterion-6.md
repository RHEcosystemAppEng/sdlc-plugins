# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

## Result: PASS

## Criterion Text
Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Analysis

The handler's SBOM fetch logic is unchanged from the original code:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call retrieves the SBOM by ID from the database. If the SBOM does not exist, the service returns an error that propagates through the `?` operator and the `.context()` wrapper. Based on the repository's error handling conventions (all handlers return `Result<T, AppError>` with `.context()` wrapping, and `AppError` implements `IntoResponse`), a missing SBOM produces a 404 Not Found response.

The PR's changes (adding `Query(params)` parameter and threshold filtering logic) do not modify the SBOM fetch or error handling path. The 404 behavior for non-existent SBOM IDs is preserved.

## Verdict

PASS -- The existing SBOM fetch and error handling logic is unchanged. Non-existent SBOM IDs continue to produce 404 responses.
