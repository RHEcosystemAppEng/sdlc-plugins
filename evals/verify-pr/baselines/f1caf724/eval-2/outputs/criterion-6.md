# Criterion 6 Analysis

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved because the SBOM fetch logic was not modified by the PR.

### Code Under Review

The handler still includes the SBOM fetch call:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code fetches the SBOM by ID and propagates any error via the `?` operator. If the SBOM does not exist, the `fetch` method returns an error which is wrapped with `.context()` and propagated through `AppError`. The `AppError` enum (defined in `common/src/error.rs` per the repository structure) implements `IntoResponse` and maps not-found errors to HTTP 404.

### Verification

The PR diff does not modify the SBOM fetch path or the error handling for non-existent SBOMs. The threshold filtering logic is applied AFTER the SBOM is successfully fetched, so a non-existent SBOM ID will still result in a 404 before any threshold processing occurs.

### Test gap

While the existing behavior is preserved in the code, the task's Test Requirements include "Test non-existent SBOM ID returns 404" and the required test file `tests/api/advisory_summary.rs` was not created. The behavioral preservation is confirmed through code inspection, but the required test coverage is absent. This is accounted for in the Scope Containment check (missing test file).
