# Acceptance Criterion 6

**Criterion**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result**: PASS

## Evidence

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing SBOM lookup pattern:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This existing code path (unchanged by the PR) fetches the SBOM by ID. Based on the repository conventions documented in the codebase, all handlers return `Result<T, AppError>` with `.context()` wrapping, and the `AppError` enum (in `common/src/error.rs`) includes a `NotFound` variant that maps to HTTP 404.

The PR does not alter the SBOM fetch logic or the error handling path. The existing behavior of returning 404 for non-existent SBOM IDs is preserved by the unchanged code preceding the new threshold filtering logic.

**Verdict**: PASS -- existing 404 behavior for non-existent SBOM IDs is preserved (no changes to the fetch/error path).
