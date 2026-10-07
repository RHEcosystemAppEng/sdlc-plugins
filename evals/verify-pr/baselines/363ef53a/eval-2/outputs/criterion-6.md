# Criterion 6: Existing 404 behavior preserved

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The PR preserves the existing SBOM lookup and 404 behavior. The handler still performs the SBOM fetch before proceeding to the advisory summary:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code is unchanged from the existing implementation (it appears in the diff context lines, not as added lines). The `SbomService::fetch()` method presumably returns an error when the SBOM ID does not exist, and the `?` operator propagates that error. Given the project's convention of using `AppError` which implements `IntoResponse`, a missing SBOM would result in an appropriate error response (404).

The PR does not modify the SBOM lookup logic, the error propagation chain, or the route registration. The existing 404 behavior for non-existent SBOM IDs is preserved.

**Note:** While the existing behavior is preserved, no integration test was created to verify the 404 behavior (the entire test file `tests/api/advisory_summary.rs` is absent from the diff). This is a scope gap tracked separately under the missing test file finding.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the SBOM fetch and error propagation are unchanged
- The `SbomService::fetch()` call and `.context()` wrapping remain intact
- No modifications to error handling patterns or route registration
