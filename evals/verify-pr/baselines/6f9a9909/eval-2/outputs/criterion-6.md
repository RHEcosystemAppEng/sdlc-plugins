## Criterion 6

**Text:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**What I checked:** The SBOM fetch logic in `modules/fundamental/src/advisory/endpoints/get.rs` and whether the error handling for non-existent SBOMs is preserved in the diff.

**Code evidence:**

The diff shows the following unchanged context lines in the handler:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
    .context("Failed to aggregate advisory severities")?;
```

The SBOM fetch with error propagation via `?` is preserved from the original code. The `SbomService::fetch` method returns an error (or `None` converted to `AppError::NotFound` via the existing pattern) when the SBOM ID does not exist, and this is propagated to the caller as a 404 response. The new threshold filtering code is placed after the SBOM fetch, so it does not interfere with the 404 behavior.

The diff only adds code after the existing SBOM validation and advisory aggregation, preserving the original error handling flow.

**Verdict: PASS** -- The existing 404 behavior for non-existent SBOM IDs is preserved. The SBOM fetch and error propagation code is unchanged.
