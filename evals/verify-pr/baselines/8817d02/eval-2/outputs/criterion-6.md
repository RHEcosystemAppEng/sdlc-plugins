# Criterion 6: Existing 404 behavior preserved

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Reasoning

The PR diff preserves the existing SBOM fetch-and-404 logic. The handler still performs:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code (visible in the diff context lines 31-34) fetches the SBOM by ID and propagates any error via the `?` operator. If the SBOM does not exist, `SbomService::fetch()` would return an error that maps to a 404 response through the `AppError` handling.

The PR changes do not modify this fetch logic -- the SBOM lookup occurs before the threshold filtering, and the error propagation chain remains intact. The threshold filtering only runs after a successful SBOM fetch and advisory aggregation.

**Evidence:**
- Lines 31-34 of the diff (context lines) show the unchanged SBOM fetch with error propagation
- The threshold filtering logic (lines 41-56) is placed after the SBOM fetch, so it only executes if the SBOM exists
- No changes to error handling or response status codes for the SBOM lookup path

**Note:** While the existing behavior appears preserved, no test was added to verify 404 behavior (the test file `tests/api/advisory_summary.rs` is entirely absent from the diff). The preservation is inferred from code inspection only.
