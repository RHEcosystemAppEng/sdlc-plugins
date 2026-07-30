# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

This criterion requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the threshold filtering changes.

### Code Inspection

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` still contains the existing SBOM fetch and error handling:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `?` operator propagates any error from `SbomService::fetch()`. When the SBOM ID does not exist, the service returns an error, which is wrapped with context and propagated as an `AppError`. The `AppError` type (from `common/src/error.rs`) implements `IntoResponse` for Axum, converting the not-found error to a 404 response.

### Preservation Confirmed

- The SBOM fetch logic was not modified in the diff
- The error propagation chain (`?` operator + `.context()`) remains intact
- The `AppError` import is still present
- The threshold filtering code is added AFTER the SBOM fetch, so a non-existent SBOM ID will still trigger the 404 before any threshold logic executes

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call with `?` propagation is unchanged
- The threshold filtering code appears after the SBOM fetch, preserving the early-exit 404 behavior
- No modifications to the error handling path in the diff
