# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The acceptance criterion requires that the endpoint continues to return 404 for non-existent SBOM IDs. This is existing behavior that should not be broken by the threshold filtering changes.

The relevant code in the handler:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... error handling with .context() ...
```

The SBOM fetch occurs before any threshold filtering logic. If the SBOM ID does not exist, `SbomService::fetch` returns an error, which is propagated through the `?` operator as an `AppError`. Based on the repository conventions (all handlers return `Result<T, AppError>` with `.context()` wrapping, and `AppError` implements `IntoResponse`), a non-existent SBOM would result in a 404 response.

The PR does not modify the SBOM fetch logic or its error handling. The threshold filtering code is positioned after the successful SBOM fetch, so it cannot interfere with the 404 behavior.

Note: while the existing 404 behavior is preserved in the code, the task also required creating a test for this case in `tests/api/advisory_summary.rs`, which was not done (the test file is missing from the PR entirely).

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- SBOM fetch with error propagation is unchanged
- The threshold filtering logic only executes after a successful SBOM fetch
- No modifications to `SbomService::fetch` or `AppError` error handling
- Test for this behavior was required but not created (see Scope Containment finding)
