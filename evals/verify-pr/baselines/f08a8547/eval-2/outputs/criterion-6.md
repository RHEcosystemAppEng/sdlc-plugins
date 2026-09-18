## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Verdict: PASS**

### Requirement

Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

### Analysis

The existing 404 behavior is preserved because the diff does not modify the SBOM lookup logic. The handler still performs:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

The `SbomService::fetch()` method returns an error when the SBOM ID does not exist, and the `?` operator propagates this as an `AppError`, which the framework converts to a 404 response. This code path is unchanged by the PR.

The new threshold filtering logic only executes after the SBOM has been successfully fetched, so a non-existent SBOM ID will still result in a 404 before any threshold processing occurs.

### Note

While the existing 404 behavior is preserved, the task's "Files to Create" section specifies creating `tests/api/advisory_summary.rs` with a test for non-existent SBOM IDs returning 404. This test file is absent from the diff (see Scope Containment finding). The runtime behavior is correct, but the test coverage is missing.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs` -- the SBOM fetch and error handling code is unchanged
- **Behavior:** Non-existent SBOM IDs trigger an error in `SbomService::fetch()` before threshold filtering runs
- **Existing pattern:** Uses the same `Result<T, AppError>` with `.context()` wrapping documented in the repository conventions
