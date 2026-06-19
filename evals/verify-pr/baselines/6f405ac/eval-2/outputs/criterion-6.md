# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved. The SBOM fetch logic is unchanged in this diff:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The `.fetch()` call and its error handling (which returns 404 via `AppError` when the SBOM is not found) are untouched by this PR. The new threshold filtering logic is added after the SBOM fetch succeeds, so it does not interfere with the existing 404 path.

The handler signature still returns `Result<Json<AdvisorySummary>, AppError>`, and the `.context()` error wrapping is preserved, ensuring that fetch failures propagate as the expected HTTP error responses.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The SBOM fetch code (`SbomService::new(&db).fetch(sbom_id.id)`) is in the unchanged context lines of the diff
- The error propagation chain (`.context("Failed to aggregate advisory severities")?`) is preserved
- The return type `Result<Json<AdvisorySummary>, AppError>` is unchanged
- The new threshold filtering logic is added only after the successful SBOM fetch
