# Criterion 6

**Criterion**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Analysis

The handler function in `modules/fundamental/src/advisory/endpoints/get.rs` fetches the SBOM before aggregating advisories:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This existing code is unchanged by the PR. The fetch call with its error handling (visible as `.ok_or()` or `.context()` pattern that returns `AppError` including `NotFound` variants) remains intact. The PR only adds code after the SBOM fetch succeeds, adding the threshold filtering logic before the final `Ok(Json(filtered))` response.

Since the SBOM fetch and its 404 error path are not modified by this PR, the existing behavior of returning 404 for non-existent SBOM IDs is preserved.

Note: While the behavior is preserved, no integration test was added to verify this (as required by the Test Requirements section of the task). The test file `tests/api/advisory_summary.rs` is entirely absent from the diff.

## Verdict: PASS

The existing 404 behavior for non-existent SBOM IDs is preserved because the SBOM fetch logic and its error handling are unchanged by this PR.
