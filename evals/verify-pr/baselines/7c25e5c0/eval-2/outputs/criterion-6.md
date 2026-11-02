# Criterion 6 — PASS

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

**Analysis:**

The existing SBOM fetch logic is preserved in the handler:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` method returns a `Result` that propagates through the `?` operator. If the SBOM ID does not exist, the service returns an error that is wrapped with `.context()` and propagated as an `AppError`, which the existing error handling infrastructure converts to a 404 response. This behavior is unchanged by the diff — the threshold filtering logic only runs after the SBOM is successfully fetched.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 30–33
- The SBOM fetch occurs before any threshold filtering logic
- The `?` operator propagates the error before the filtering code is reached
- No changes were made to the fetch or error handling paths
