# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The diff preserves the existing SBOM fetch logic that produces 404 for non-existent IDs. The handler still performs the SBOM lookup before aggregating advisory severities, and this path is unchanged.

### Code Analysis

The existing handler code (visible in diff context lines) shows:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This code is in the unchanged (context) portion of the diff, confirming it was not modified. The `SbomService::fetch` method is expected to return an error (mapped through `AppError`) when the SBOM ID does not exist, producing a 404 response. This follows the established pattern in the repository where handlers return `Result<T, AppError>` with `.context()` wrapping.

The new threshold filtering code is added **after** the SBOM fetch, so if the SBOM does not exist, the handler will error out before reaching the threshold logic. The 404 behavior is preserved.

### Caveat

While the existing 404 behavior is preserved in the handler code, no integration test was added to verify this behavior (the required test file `tests/api/advisory_summary.rs` is entirely absent from the diff). The Test Requirements include "Test non-existent SBOM ID returns 404" but no test was created. The criterion itself (about the endpoint behavior) is satisfied, but the test coverage for it is not.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- SBOM fetch logic is in unchanged context lines
- The threshold filtering logic is positioned after the SBOM fetch, preserving the early-exit 404 path
- No modifications to the error handling chain for non-existent SBOMs
